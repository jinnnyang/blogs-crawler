# -*- coding: utf-8 -*-
"""
中间件模块
包含缓存中间件和随机User-Agent中间件
"""

import logging
import os
import random
import re
from pathlib import Path
from typing import Dict, Optional

import yaml
from scrapy import signals
from scrapy.exceptions import IgnoreRequest
from scrapy.http import HtmlResponse, Response

logger = logging.getLogger(__name__)


class CacheMiddleware:
    """
    缓存中间件
    支持从output/**/*.md预加载缓存，避免重复请求
    """

    def __init__(self, cache_dir: str = "cache", output_dir: str = "output"):
        """
        初始化缓存中间件

        Args:
            cache_dir: 缓存目录
            output_dir: 输出目录
        """
        self.cache_dir = Path(cache_dir)
        self.output_dir = Path(output_dir)
        self.url_cache: Dict[str, Dict] = {}  # url -> {content, metadata}
        self.logger = logger
        self._preload_from_output()

    @classmethod
    def from_crawler(cls, crawler):
        """
        从crawler创建中间件实例

        Args:
            crawler: Scrapy crawler对象

        Returns:
            CacheMiddleware实例
        """
        cache_dir = crawler.settings.get("CACHE_DIR", "cache")
        output_dir = crawler.settings.get("OUTPUT_DIR", "output")
        middleware = cls(cache_dir, output_dir)
        crawler.signals.connect(middleware.spider_opened, signal=signals.spider_opened)
        crawler.signals.connect(middleware.spider_closed, signal=signals.spider_closed)
        return middleware

    def _preload_from_output(self):
        """
        从output/**/*.md预加载缓存
        解析YAML metadata，提取URL并添加到缓存
        """
        if not self.output_dir.exists():
            return

        # 递归查找所有.md文件
        md_files = self.output_dir.rglob("*.md")

        for md_file in md_files:
            try:
                with open(md_file, "r", encoding="utf-8") as f:
                    content = f.read()

                # 解析YAML metadata
                metadata = self._parse_yaml_metadata(content)
                if metadata and "url" in metadata:
                    url = metadata["url"]
                    self.url_cache[url] = {
                        "content": content,
                        "metadata": metadata,
                        "file_path": str(md_file),
                    }
            except Exception as e:
                # 忽略解析错误的文件
                pass

    def _parse_yaml_metadata(self, content: str) -> Optional[Dict]:
        """
        解析Markdown文件中的YAML metadata

        Args:
            content: Markdown文件内容

        Returns:
            metadata字典或None
        """
        # 检查是否以---开头
        if not content.startswith("---"):
            return None

        # 查找第二个---
        end_pos = content.find("\n---\n", 4)
        if end_pos == -1:
            return None

        # 提取YAML部分
        yaml_content = content[4:end_pos]

        try:
            return yaml.safe_load(yaml_content)
        except yaml.YAMLError:
            return None

    def process_request(self, request):
        """
        处理请求，检查缓存

        Args:
            request: Scrapy Request对象

        Returns:
            Response对象或None
        """
        url = request.url
        self.logger.debug(f"[CacheMiddleware] Processing request: {url}")

        # 检查缓存
        if url in self.url_cache:
            cached = self.url_cache[url]
            self.logger.info(f"[CacheMiddleware] Cache hit: {url}")

            # 从缓存创建Response
            # 提取content部分（去除YAML metadata）
            content = cached["content"]
            metadata = cached["metadata"]

            # 查找第二个---，获取正文内容
            end_pos = content.find("\n---\n", 4)
            if end_pos != -1:
                body_content = content[end_pos + 5 :]
            else:
                body_content = content

            self.logger.debug(
                f"[CacheMiddleware] Creating response with request={request}, url={url}"
            )
            # 创建HtmlResponse
            response = HtmlResponse(
                url=url,
                status=200,
                headers={"Content-Type": "text/html; charset=utf-8"},
                body=body_content.encode("utf-8"),
                request=request,  # 传递 request 参数以绑定响应到请求
            )

            self.logger.debug(
                f"[CacheMiddleware] Response created, has meta={hasattr(response, 'meta')}"
            )
            # 添加缓存标记
            response.meta["cached"] = True
            response.meta["cache_metadata"] = metadata

            self.logger.debug(f"[CacheMiddleware] Returning cached response for: {url}")
            return response

        self.logger.debug(f"[CacheMiddleware] Cache miss for: {url}")
        return None

    def process_response(self, request, response):
        """
        处理响应，保存到缓存

        Args:
            request: Scrapy Request对象
            response: Scrapy Response对象

        Returns:
            Response对象
        """
        # 如果响应来自缓存，直接返回
        try:
            if response.meta.get("cached"):
                return response
        except AttributeError:
            # response.meta不可用，继续处理
            pass

        # 保存响应到缓存目录
        if self.cache_dir:
            self.cache_dir.mkdir(exist_ok=True)

            # 生成缓存文件名
            from urllib.parse import urlparse

            parsed = urlparse(request.url)
            cache_key = f"{parsed.netloc}{parsed.path.replace('/', '_')}"
            cache_file = self.cache_dir / f"{cache_key}.html"

            try:
                with open(cache_file, "w", encoding="utf-8") as f:
                    f.write(response.text)
            except Exception as e:
                self.logger.warning(f"[CacheMiddleware] Failed to save cache: {e}")

        return response

    def spider_opened(self, spider):
        """
        Spider打开时的回调

        Args:
            spider: Spider实例
        """
        self.logger.info(
            f"[CacheMiddleware] Opened, loaded {len(self.url_cache)} URLs from cache"
        )

    def spider_closed(self, spider, reason):
        """
        Spider关闭时的回调

        Args:
            spider: Spider实例
            reason: 关闭原因
        """
        self.logger.info(f"[CacheMiddleware] Closed, reason: {reason}")


class RandomUserAgentMiddleware:
    """
    随机User-Agent中间件
    """

    def __init__(self, user_agent_list=None):
        self.user_agent_list = user_agent_list or [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2 Safari/605.1.15",
        ]
        self.logger = logger

    @classmethod
    def from_crawler(cls, crawler):
        user_agent_list = crawler.settings.get("USER_AGENT_LIST")
        return cls(user_agent_list)

    def process_request(self, request):
        request.headers["User-Agent"] = random.choice(self.user_agent_list)
        self.logger.debug(
            f"[RandomUserAgent] Using User-Agent: {request.headers['User-Agent']}"
        )

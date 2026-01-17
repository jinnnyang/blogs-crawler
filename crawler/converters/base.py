# -*- coding: utf-8 -*-
"""
HTML到Markdown转换器基类
提供基础的HTML到Markdown转换功能
"""

import logging
import time
from typing import List, Optional

from markdownify import markdownify as md

from crawler.config_loader import get_config_loader
from crawler.utils import HtmlCleaner

logger = logging.getLogger(__name__)


class BaseConverter:
    """
    HTML到Markdown转换器基类
    根据框架配置自动选择合适的选择器进行转换
    """

    def __init__(self, framework: str = "unknown"):
        """
        初始化转换器

        Args:
            framework: 框架名称
        """
        self.framework = framework
        self.config_loader = get_config_loader()
        self.strip_tags = self._get_strip_tags()

    def _get_strip_tags(self) -> List[str]:
        """
        从配置获取需要移除的标签列表

        Returns:
            标签列表
        """
        try:
            return self.config_loader.get_strip_tags(self.framework)
        except Exception as e:
            logger.error(
                f"[BaseConverter] Failed to get strip_tags for {self.framework}: {e}",
                exc_info=True,
            )
            return ["script", "style", "nav", "footer", "header"]

    def _get_selectors(self) -> dict:
        """
        从配置获取选择器

        Returns:
            选择器字典
        """
        try:
            return self.config_loader.get_selectors(self.framework)
        except Exception as e:
            logger.error(
                f"[BaseConverter] Failed to get selectors for {self.framework}: {e}",
                exc_info=True,
            )
            return {"title": ["h1", "title"], "content": ["body"], "tags": []}

    def convert(self, html: str) -> str:
        """
        将HTML转换为Markdown

        Args:
            html: HTML字符串

        Returns:
            Markdown字符串
        """
        start_time = time.time()
        logger.debug(
            f"[BaseConverter] Converting HTML to Markdown, length: {len(html)}"
        )

        try:
            from bs4 import BeautifulSoup

            soup = BeautifulSoup(html, "lxml")

            # 移除不需要的标签
            HtmlCleaner.strip_tags(soup, self.strip_tags)

            # 使用markdownify函数转换
            result = md(str(soup), heading_style="ATX", bullets="*")

            elapsed = time.time() - start_time
            logger.debug(
                f"[BaseConverter] Conversion completed in {elapsed:.3f}s, "
                f"output length: {len(result)}"
            )

            return result
        except Exception as e:
            logger.error(f"[BaseConverter] Failed to convert HTML: {e}", exc_info=True)
            return ""

    def extract_title(self, response) -> Optional[str]:
        """
        提取页面标题

        Args:
            response: Scrapy Response对象

        Returns:
            标题字符串或None
        """
        try:
            selectors = self._get_selectors()
            title_selectors = selectors.get("title", ["h1", "title"])

            from crawler.utils import SelectorHelper

            title = SelectorHelper.extract_first_text(response, title_selectors)
            if title:
                return title

            # 尝试 og:title meta标签
            title = response.css('meta[property="og:title"]::attr(content)').get()
            if title:
                return title.strip()

            return None
        except Exception as e:
            logger.error(
                f"[BaseConverter] Failed to extract title from {response.url}: {e}",
                exc_info=True,
            )
            return None

    def extract_tags(self, response) -> List[str]:
        """
        提取页面标签

        Args:
            response: Scrapy Response对象

        Returns:
            标签列表
        """
        try:
            selectors = self._get_selectors()
            tags_selectors = selectors.get("tags", [])

            from crawler.utils import SelectorHelper

            tags = SelectorHelper.extract_all_texts(response, tags_selectors)

            # 尝试从meta keywords提取
            keywords = response.css('meta[name="keywords"]::attr(content)').get()
            if keywords:
                tags.extend([k.strip() for k in keywords.split(",")])

            # 尝试从og:article:tag提取
            tag_elements = response.css(
                'meta[property="og:article:tag"]::attr(content)'
            ).getall()
            tags.extend([t.strip() for t in tag_elements])

            # 去重并过滤空值
            tags = list(set(tag for tag in tags if tag))

            return tags
        except Exception as e:
            logger.error(
                f"[BaseConverter] Failed to extract tags from {response.url}: {e}",
                exc_info=True,
            )
            return []

    def extract_content(self, response) -> str:
        """
        提取页面正文内容

        Args:
            response: Scrapy Response对象

        Returns:
            Markdown格式的正文内容
        """
        start_time = time.time()
        try:
            selectors = self._get_selectors()
            content_selectors = selectors.get("content", ["body"])

            from crawler.utils import SelectorHelper

            content_html = SelectorHelper.extract_first_html(
                response, content_selectors
            )

            if content_html:
                result = self.convert(content_html)
                elapsed = time.time() - start_time
                logger.debug(
                    f"[BaseConverter] Content extraction completed in {elapsed:.3f}s"
                )
                return result

            return ""
        except Exception as e:
            logger.error(
                f"[BaseConverter] Failed to extract content from {response.url}: {e}",
                exc_info=True,
            )
            return ""

    def process(self, response):
        """
        处理响应，提取标题、标签和内容

        Args:
            response: Scrapy Response对象

        Returns:
            dict: 包含title, tags, content的字典
        """
        start_time = time.time()
        logger.debug(f"[BaseConverter] Processing response: {response.url}")

        try:
            result = {
                "title": self.extract_title(response),
                "tags": self.extract_tags(response),
                "content": self.extract_content(response),
            }

            elapsed = time.time() - start_time
            logger.info(
                f"[BaseConverter] Extracted - Title: {result.get('title')}, "
                f"Tags: {result.get('tags')}, Time: {elapsed:.3f}s"
            )

            return result
        except Exception as e:
            logger.error(
                f"[BaseConverter] Failed to process response {response.url}: {e}",
                exc_info=True,
            )
            return {"title": None, "tags": [], "content": ""}

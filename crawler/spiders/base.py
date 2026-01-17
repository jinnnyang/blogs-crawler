# -*- coding: utf-8 -*-
"""
博客爬虫基类
提供通用的博客文档爬取功能
"""

import re
from datetime import datetime
from urllib.parse import urljoin, urlparse

import scrapy
from bs4 import BeautifulSoup
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from scrapy.utils.response import get_base_url

from crawler.converters import create_converter
from crawler.framework_detector import FrameworkDetector
from crawler.items import BlogItem
from crawler.utils import UrlNormalizer


class BlogSpider(CrawlSpider):
    """
    博客爬虫基类
    支持递归爬取文档站点，自动检测框架并转换为Markdown
    """

    name = "blog"

    # 自定义配置
    custom_settings = {
        "LOG_LEVEL": "INFO",
    }

    # 链接提取规则（动态生成）
    rules = ()

    def __init__(self, *args, **kwargs):
        """
        初始化爬虫

        支持从命令行传入起始URL:
        scrapy crawl blog -a url=https://example.com
        """
        super().__init__(*args, **kwargs)

        # 从命令行参数获取起始URL
        self.start_url = kwargs.get("url")
        if self.start_url:
            self.start_urls = [self.start_url]
            # 设置allowed_domains
            parsed = urlparse(self.start_url)
            self.allowed_domains = [parsed.netloc]

        # 框架检测器
        self.framework_detector = FrameworkDetector()

        # 当前检测到的框架
        self.current_framework = "unknown"

        # 是否已初始化规则
        self._rules_initialized = False

        # 统计信息
        self.stats = {
            "pages_crawled": 0,
            "pages_succeeded": 0,
            "pages_failed": 0,
            "framework_distribution": {},
        }

    def _initialize_rules(self, response):
        """
        根据检测到的框架初始化链接提取规则

        Args:
            response: Scrapy Response对象
        """
        if self._rules_initialized:
            return

        try:
            # 检测框架
            self.current_framework = self.framework_detector.detect(response)
            self.logger.info(
                f"[Framework Detection] Detected framework: {self.current_framework} for {response.url}"
            )

            # 更新框架分布统计
            if self.current_framework not in self.stats["framework_distribution"]:
                self.stats["framework_distribution"][self.current_framework] = 0
            self.stats["framework_distribution"][self.current_framework] += 1

            # 获取框架的链接提取器配置
            link_extractor_config = self.framework_detector.get_link_extractor_config(
                self.current_framework
            )
            allow = link_extractor_config.get("allow", [])
            deny = link_extractor_config.get("deny", [])

            # 创建规则
            self._rules = (
                Rule(
                    LinkExtractor(allow=allow, deny=deny),
                    callback="parse_page",
                    follow=True,
                ),
            )

            self._rules_initialized = True
            self.logger.info(f"[Rules] Initialized with allow={allow}, deny={deny}")
        except Exception as e:
            self.logger.error(f"[Rules] Failed to initialize rules: {e}", exc_info=True)
            # 使用默认规则
            self._rules = (
                Rule(
                    LinkExtractor(allow=(), deny=()),
                    callback="parse_page",
                    follow=True,
                ),
            )
            self._rules_initialized = True

    @property
    def rules(self):
        """动态返回规则"""
        return getattr(self, "_rules", ())

    @rules.setter
    def rules(self, value):
        """设置规则"""
        self._rules = value

    def _process_response(self, response):
        """
        在解析前处理响应，将相对路径转换为绝对路径

        Args:
            response: Scrapy Response对象

        Returns:
            处理后的 Response 对象
        """
        try:
            # 使用 BeautifulSoup 解析 HTML
            soup = BeautifulSoup(response.text, "lxml")

            # 转换相对路径为绝对路径
            base_url = get_base_url(response)
            UrlNormalizer.convert_relative_urls(soup, base_url)

            # 替换响应的文本
            response._set_body(str(soup).encode("utf-8"))

            return response
        except Exception as e:
            self.logger.error(
                f"[Process Response] Failed to process response {response.url}: {e}",
                exc_info=True,
            )
            return response

    def parse_page(self, response):
        """
        解析页面

        Args:
            response: Scrapy Response对象

        Yields:
            BlogItem对象
        """
        self.stats["pages_crawled"] += 1

        try:
            # 如果规则未初始化，先初始化
            if not self._rules_initialized:
                self._initialize_rules(response)

            # 处理响应，转换相对路径
            response = self._process_response(response)

            # 获取对应的转换器
            converter = create_converter(self.current_framework)
            self.logger.debug(
                f"[Converter] Using converter for framework: {self.current_framework}"
            )

            # 提取数据
            data = converter.process(response)
            self.logger.debug(
                f"[Data Extraction] Extracted title: {data.get('title')}, tags: {data.get('tags')}"
            )

            # 创建Item
            item = BlogItem()
            item["url"] = response.url
            item["title"] = data.get("title")
            # 将 Markdown 内容中的相对路径转换为绝对路径
            content = data.get("content", "")
            item["content"] = self._convert_markdown_urls(content, response.url)
            item["tags"] = data.get("tags", [])
            item["framework"] = self.current_framework
            item["crawl_time"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            self.stats["pages_succeeded"] += 1
            self.logger.info(
                f"[Item Created] Title: {item.get('title')}, URL: {response.url}"
            )

            yield item
        except Exception as e:
            self.stats["pages_failed"] += 1
            self.logger.error(
                f"[Parse Page] Failed to parse page {response.url}: {e}", exc_info=True
            )

    def start_requests(self):
        """
        生成初始请求（同步）
        对于CrawlSpider，不需要指定callback，让CrawlSpider的默认处理流程处理
        """
        self.logger.info(
            f"[BlogSpider] Starting crawl with {len(self.start_urls)} start URLs"
        )
        for url in self.start_urls:
            self.logger.debug(f"[BlogSpider] Starting request to: {url}")
            yield scrapy.Request(
                url,
                dont_filter=True,
                callback=self._initial_parse,
                errback=self._errback,
            )

    def _initial_parse(self, response):
        """
        初始解析，用于检测框架并初始化规则

        Args:
            response: Scrapy Response对象

        Yields:
            解析结果
        """
        self.logger.debug(f"[Initial Parse] Received response for: {response.url}")
        self.logger.debug(
            f"[Initial Parse] Response has meta: {hasattr(response, 'meta')}"
        )
        if hasattr(response, "meta"):
            self.logger.debug(f"[Initial Parse] Response meta: {response.meta}")

        try:
            # 初始化规则
            self._initialize_rules(response)

            # 处理响应，转换相对路径
            response = self._process_response(response)

            # 解析页面
            yield from self.parse_page(response)

            # 继续爬取其他页面
            for link in self._rules[0].link_extractor.extract_links(response):
                # 将相对 URL 转换为绝对 URL
                absolute_url = urljoin(response.url, link.url)
                self.logger.debug(
                    f"[Initial Parse] Yielding request to: {absolute_url}"
                )
                yield scrapy.Request(
                    absolute_url, callback=self.parse_page, errback=self._errback
                )
        except Exception as e:
            self.logger.error(
                f"[Initial Parse] Failed to parse initial page {response.url}: {e}",
                exc_info=True,
            )

    def _convert_markdown_urls(self, content: str, base_url: str) -> str:
        """
        将 Markdown 内容中的相对路径转换为绝对路径

        Args:
            content: Markdown 内容
            base_url: 基础 URL

        Returns:
            转换后的 Markdown 内容
        """
        if not content:
            return content

        # 转换 Markdown 图片链接：![alt](/path/to/image.png)
        def replace_image_url(match):
            alt_text = match.group(1)
            url = match.group(2)
            # 跳过已经是绝对 URL 的链接
            if url.startswith(("http://", "https://", "data:", "#")):
                return match.group(0)
            # 转换相对路径为绝对路径
            absolute_url = urljoin(base_url, url)
            return f"![{alt_text}]({absolute_url})"

        content = re.sub(r"!\[([^\]]*)\]\(([^)]+)\)", replace_image_url, content)

        # 转换 Markdown 链接：[text](/path/to/page.html)
        def replace_link_url(match):
            text = match.group(1)
            url = match.group(2)
            # 跳过已经是绝对 URL 的链接和锚点链接
            if url.startswith(("http://", "https://", "mailto:", "tel:", "#")):
                return match.group(0)
            # 转换相对路径为绝对路径
            absolute_url = urljoin(base_url, url)
            return f"[{text}]({absolute_url})"

        content = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", replace_link_url, content)

        # 转换 Markdown 引用链接：[ref]: /path/to/page.html
        def replace_ref_url(match):
            ref = match.group(1)
            url = match.group(2)
            # 跳过已经是绝对 URL 的链接
            if url.startswith(("http://", "https://", "#")):
                return match.group(0)
            # 转换相对路径为绝对路径
            absolute_url = urljoin(base_url, url)
            return f"[{ref}]: {absolute_url}"

        content = re.sub(r"\[([^\]]+)\]:\s*([^\s]+)", replace_ref_url, content)

        return content

    def _errback(self, failure):
        """
        错误回调处理

        Args:
            failure: Twisted Failure对象
        """
        self.stats["pages_failed"] += 1
        # 安全地获取请求 URL
        request_url = failure.request.url if failure.request else "unknown"
        self.logger.error(
            f"[Request Failed] {request_url}: {failure.value}", exc_info=True
        )
        # 添加更详细的错误信息
        self.logger.debug(f"[Request Failed] Failure type: {type(failure.value)}")
        self.logger.debug(
            f"[Request Failed] Failure traceback: {failure.getTraceback()}"
        )

    def closed(self, reason):
        """
        爬虫关闭时的回调

        Args:
            reason: 关闭原因
        """
        self.logger.info("=" * 60)
        self.logger.info("[BlogSpider] Crawl Statistics:")
        self.logger.info(f"  Total Pages Crawled: {self.stats['pages_crawled']}")
        self.logger.info(f"  Pages Succeeded: {self.stats['pages_succeeded']}")
        self.logger.info(f"  Pages Failed: {self.stats['pages_failed']}")
        self.logger.info("  Framework Distribution:")
        for framework, count in self.stats["framework_distribution"].items():
            self.logger.info(f"    {framework}: {count}")
        self.logger.info(f"  Close Reason: {reason}")
        self.logger.info("=" * 60)

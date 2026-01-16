# -*- coding: utf-8 -*-
"""
博客爬虫基类
提供通用的博客文档爬取功能
"""

from datetime import datetime
from urllib.parse import urljoin, urlparse

import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from crawler.converters import get_converter
from crawler.framework_detector import FrameworkDetector
from crawler.items import BlogItem


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

    # 链接提取规则
    rules = (
        Rule(
            LinkExtractor(
                allow=(),  # 由子类定义
                deny=(),  # 由子类定义
            ),
            callback="parse_page",
            follow=True,
        ),
    )

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

    def parse_page(self, response):
        """
        解析页面

        Args:
            response: Scrapy Response对象

        Yields:
            BlogItem对象
        """
        # 检测框架
        framework = self.framework_detector.detect(response)
        self.logger.debug(f"Detected framework: {framework} for {response.url}")

        # 获取对应的转换器
        converter = get_converter(framework)()
        converter_instance = converter()

        # 提取数据
        data = converter_instance.process(response)

        # 创建Item
        item = BlogItem()
        item["url"] = response.url
        item["title"] = data.get("title")
        item["content"] = data.get("content")
        item["tags"] = data.get("tags", [])
        item["framework"] = framework
        item["crawl_time"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        self.logger.info(f"Extracted: {item.get('title')} from {response.url}")

        yield item

    async def start(self):
        """
        异步启动爬虫（Scrapy 2.13+ 推荐方法）
        """
        for url in self.start_urls:
            yield scrapy.Request(url, callback=self.parse)

    def start_requests(self):
        """
        生成初始请求（兼容旧版本 Scrapy）
        """
        for url in self.start_urls:
            yield scrapy.Request(url, callback=self.parse)

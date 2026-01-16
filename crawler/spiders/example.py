# -*- coding: utf-8 -*-
"""
Example Spider
爬取 https://example.com 的示例爬虫
"""

from datetime import datetime

import scrapy
from crawler.items import CrawlerItem


class ExampleSpider(scrapy.Spider):
    """
    示例爬虫
    爬取 example.com 的简单页面
    """

    name = "example"
    allowed_domains = ["example.com"]
    start_urls = ["https://example.com"]

    custom_settings = {
        "LOG_LEVEL": "INFO",
    }

    def parse(self, response):
        """
        解析响应数据
        """
        # 创建 Item
        item = CrawlerItem()

        # 提取 URL
        item["url"] = response.url

        # 提取标题
        item["title"] = (
            response.css("h1::text").get() or response.xpath("//h1/text()").get()
        )

        # 提取内容
        # 获取页面所有文本内容
        content_parts = response.css("p::text").getall()
        if content_parts:
            item["content"] = "\n".join(content_parts)
        else:
            # 如果没有 p 标签，获取 body 中的所有文本
            item["content"] = response.css("body::text").getall()

        # 记录爬取时间
        item["crawl_time"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # 打印调试信息
        self.logger.info(f"Extracted item from: {response.url}")
        self.logger.info(f"Title: {item.get('title')}")

        yield item

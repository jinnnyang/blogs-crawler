# -*- coding: utf-8 -*-
"""
异步爬虫示例
使用 Scrapy 的异步功能进行高效爬取
"""

import scrapy
from crawler.items import CrawlerItem


class AsyncSpider(scrapy.Spider):
    """
    异步爬虫示例
    """

    name = "async_spider"
    allowed_domains = ["example.com"]
    start_urls = ["https://example.com"]

    custom_settings = {
        "LOG_LEVEL": "INFO",
        "CONCURRENT_REQUESTS": 32,
        "DOWNLOAD_DELAY": 0.5,
    }

    def parse(self, response):
        """
        解析响应数据
        """
        item = CrawlerItem()
        item["url"] = response.url
        item["title"] = response.css("h1::text").get()
        item["content"] = response.css("p::text").getall()
        yield item

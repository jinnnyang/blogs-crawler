# -*- coding: utf-8 -*-
# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html

import random

from itemadapter import ItemAdapter
from scrapy import signals


class CrawlerSpiderMiddleware:
    """
    爬虫中间件
    处理爬虫输入和输出
    """

    @classmethod
    def from_crawler(cls, crawler):
        s = cls(crawler)
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def __init__(self, crawler):
        self.crawler = crawler

    def process_spider_input(self, response):
        return None

    async def process_spider_output(self, response, result):
        async for i in result:
            yield i

    def process_spider_exception(self, response, exception):
        pass

    async def process_start(self, start):
        async for item_or_request in start:
            yield item_or_request

    def spider_opened(self):
        self.crawler.spider.logger.info("Spider opened: %s" % self.crawler.spider.name)


class CrawlerDownloaderMiddleware:
    """
    下载中间件
    处理请求和响应
    """

    @classmethod
    def from_crawler(cls, crawler):
        s = cls(crawler)
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def __init__(self, crawler):
        self.crawler = crawler

    def process_request(self, request):
        return None

    def process_response(self, request, response):
        return response

    def process_exception(self, request, exception):
        pass

    def spider_opened(self):
        self.crawler.spider.logger.info("Spider opened: %s" % self.crawler.spider.name)


class RandomUserAgentMiddleware:
    """
    随机 User-Agent 中间件
    """

    def __init__(self, user_agent_list=None):
        self.user_agent_list = user_agent_list or [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0",
        ]

    @classmethod
    def from_crawler(cls, crawler):
        user_agent_list = crawler.settings.get("USER_AGENT_LIST")
        return cls(user_agent_list)

    def process_request(self, request):
        request.headers["User-Agent"] = random.choice(self.user_agent_list)


class ProxyMiddleware:
    """
    代理中间件
    """

    def __init__(self, crawler, proxy_list=None):
        self.crawler = crawler
        self.proxy_list = proxy_list or []
        self.current_index = 0

    @classmethod
    def from_crawler(cls, crawler):
        proxy_list = crawler.settings.get("PROXY_LIST", [])
        return cls(crawler, proxy_list)

    def process_request(self, request):
        if self.proxy_list:
            proxy = self.proxy_list[self.current_index % len(self.proxy_list)]
            request.meta["proxy"] = proxy
            self.current_index += 1
            self.crawler.spider.logger.debug(f"Using proxy: {proxy}")

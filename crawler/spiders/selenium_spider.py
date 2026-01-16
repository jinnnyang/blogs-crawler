# -*- coding: utf-8 -*-
"""
Selenium 爬虫示例
使用 Selenium 处理 JavaScript 渲染页面
"""

# 注意：在实际使用中，建议在中间件（middleware）中拦截请求并使用 Selenium 处理，
# 而不是直接在爬虫核心代码中操作。本示例仅用于演示目的。

import scrapy
from crawler.items import CrawlerItem
from scrapy.http import HtmlResponse
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service


class SeleniumSpider(scrapy.Spider):
    """
    Selenium 爬虫示例
    需要安装 selenium 和 ChromeDriver
    """

    name = "selenium_spider"
    allowed_domains = ["example.com"]
    start_urls = ["https://example.com"]

    custom_settings = {
        "LOG_LEVEL": "INFO",
        "DOWNLOAD_DELAY": 2,
    }

    def __init__(self, *args, **kwargs):
        super(SeleniumSpider, self).__init__(*args, **kwargs)
        self.driver = None

    async def start(self):
        """
        使用 Selenium 发送请求（Scrapy 2.13+ 异步方法）
        start_requests() has been deprecated in favor of start()
        """
        chrome_options = Options()
        chrome_options.add_argument("--headless")  # 无头模式
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--no-sandbox")

        # 初始化 WebDriver
        self.driver = webdriver.Chrome(options=chrome_options)

        # 调用父类的 start() 方法来生成请求
        await super().start()

    def start_requests(self):
        """
        使用 Selenium 发送请求（向后兼容 Scrapy <2.13）
        此方法保留用于兼容 Scrapy 2.11-2.12 版本
        """
        chrome_options = Options()
        chrome_options.add_argument("--headless")  # 无头模式
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--no-sandbox")

        # 初始化 WebDriver
        self.driver = webdriver.Chrome(options=chrome_options)

        for url in self.start_urls:
            yield scrapy.Request(url, callback=self.parse, dont_filter=True)

    def parse(self, response):
        """
        使用 Selenium 渲染页面后解析
        """
        # 使用 Selenium 加载页面
        self.driver.get(response.url)

        # 等待页面加载
        self.driver.implicitly_wait(10)

        # 获取渲染后的 HTML
        body = self.driver.page_source

        # 创建 Scrapy Response 对象
        response = HtmlResponse(
            url=self.driver.current_url, body=body.encode("utf-8"), encoding="utf-8"
        )

        # 解析数据
        item = CrawlerItem()
        item["url"] = response.url
        item["title"] = response.css("h1::text").get()
        item["content"] = response.css("p::text").getall()
        yield item

    def closed(self, reason):
        """关闭爬虫时清理资源"""
        if self.driver:
            self.driver.quit()

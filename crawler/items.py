# -*- coding: utf-8 -*-
# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class CrawlerItem(scrapy.Item):
    """
    简单爬虫数据模型
    适用于基础网页爬取
    """

    # URL
    url = scrapy.Field()

    # 标题
    title = scrapy.Field()

    # 内容
    content = scrapy.Field()

    # 爬取时间
    crawl_time = scrapy.Field()

    # 验证状态
    status = scrapy.Field()

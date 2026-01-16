# -*- coding: utf-8 -*-
"""
博客爬虫数据模型
用于存储博客文档的元数据和内容
"""

import scrapy


class BlogItem(scrapy.Item):
    """
    博客文档数据模型
    包含URL、标题、内容、标签、框架类型等信息
    """

    # 页面URL
    url = scrapy.Field()

    # 页面标题
    title = scrapy.Field()

    # Markdown内容（正文，不含metadata）
    content = scrapy.Field()

    # 标签列表
    tags = scrapy.Field()

    # 文档框架类型 (readthedocs, rbook, mkdocs, sphinx, teadocs, docsify, unknown)
    framework = scrapy.Field()

    # 爬取时间
    crawl_time = scrapy.Field()

    # 输出文件路径（如 output/example.com/path/to/page.md）
    output_path = scrapy.Field()

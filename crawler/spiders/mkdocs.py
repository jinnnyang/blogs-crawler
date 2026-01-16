# -*- coding: utf-8 -*-
"""
MkDocs专用爬虫
针对MkDocs文档框架优化的爬虫
"""

from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule

from .base import BlogSpider


class MkDocsSpider(BlogSpider):
    """
    MkDocs专用爬虫
    针对MkDocs文档站点的链接提取规则进行优化
    """

    name = "mkdocs"

    # MkDocs链接提取规则
    rules = (
        Rule(
            LinkExtractor(
                allow=(
                    r".*/.*\.html",  # HTML页面
                    r".*/.*",  # 其他页面
                ),
                deny=(
                    r".*/static/.*",  # 静态资源
                    r".*/assets/.*",  # 资源文件
                    r".*/img/.*",  # 图片
                    r".*/fonts/.*",  # 字体
                ),
            ),
            callback="parse_page",
            follow=True,
        ),
    )

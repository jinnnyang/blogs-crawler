# -*- coding: utf-8 -*-
"""
RBook专用爬虫
针对RBook文档框架优化的爬虫
"""

from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule

from .base import BlogSpider


class RBookSpider(BlogSpider):
    """
    RBook专用爬虫
    针对RBook文档站点的链接提取规则进行优化
    """

    name = "rbook"

    # RBook链接提取规则
    rules = (
        Rule(
            LinkExtractor(
                allow=(
                    r".*/.*\.html",  # HTML页面
                ),
                deny=(
                    r".*/static/.*",  # 静态资源
                    r".*/assets/.*",  # 资源文件
                ),
            ),
            callback="parse_page",
            follow=True,
        ),
    )

# -*- coding: utf-8 -*-
"""
Docsify专用爬虫
针对Docsify文档框架优化的爬虫
"""

from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule

from .base import BlogSpider


class DocsifySpider(BlogSpider):
    """
    Docsify专用爬虫
    针对Docsify文档站点的链接提取规则进行优化
    """

    name = "docsify"

    # Docsify链接提取规则
    rules = (
        Rule(
            LinkExtractor(
                allow=(
                    r".*/.*\.html",  # HTML页面
                    r".*/#.*",  # 锚点链接（需要特殊处理）
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

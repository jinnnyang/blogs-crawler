# -*- coding: utf-8 -*-
"""
Sphinx专用爬虫
针对Sphinx文档框架优化的爬虫
"""

from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule

from .base import BlogSpider


class SphinxSpider(BlogSpider):
    """
    Sphinx专用爬虫
    针对Sphinx文档站点的链接提取规则进行优化
    """

    name = "sphinx"

    # Sphinx链接提取规则
    rules = (
        Rule(
            LinkExtractor(
                allow=(
                    r".*/.*\.html",  # HTML页面
                ),
                deny=(
                    r".*/_static/.*",  # 静态资源
                    r".*/_sources/.*",  # 源文件
                    r".*/genindex\.html",  # 索引页
                    r".*/search\.html",  # 搜索页
                    r".*/py-modindex\.html",  # 模块索引
                ),
            ),
            callback="parse_page",
            follow=True,
        ),
    )

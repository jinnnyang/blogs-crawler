# -*- coding: utf-8 -*-
"""
ReadTheDocs专用爬虫
针对ReadTheDocs文档框架优化的爬虫
"""

from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule

from .base import BlogSpider


class ReadTheDocsSpider(BlogSpider):
    """
    ReadTheDocs专用爬虫
    针对ReadTheDocs文档站点的链接提取规则进行优化
    """

    name = "readthedocs"

    # ReadTheDocs链接提取规则
    rules = (
        Rule(
            LinkExtractor(
                allow=(
                    r".*/en/stable/.*",  # 稳定版文档
                    r".*/en/latest/.*",  # 最新版文档
                    r".*/en/.*",  # 英文文档
                    r".*/zh_CN/.*",  # 中文文档
                    r".*/.*\.html",  # HTML页面
                ),
                deny=(
                    r".*/_static/.*",  # 静态资源
                    r".*/_downloads/.*",  # 下载文件
                    r".*/genindex\.html",  # 索引页
                    r".*/search\.html",  # 搜索页
                    r".*/py-modindex\.html",  # 模块索引
                ),
            ),
            callback="parse_page",
            follow=True,
        ),
    )

# -*- coding: utf-8 -*-
"""
博客爬虫模块
"""

from .base import BlogSpider
from .docsify import DocsifySpider
from .mkdocs import MkDocsSpider
from .rbook import RBookSpider
from .readthedocs import ReadTheDocsSpider
from .sphinx import SphinxSpider
from .teadocs import TeadocsSpider

__all__ = [
    "BlogSpider",
    "ReadTheDocsSpider",
    "RBookSpider",
    "MkDocsSpider",
    "SphinxSpider",
    "TeadocsSpider",
    "DocsifySpider",
]

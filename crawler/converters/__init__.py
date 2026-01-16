# -*- coding: utf-8 -*-
"""
HTML到Markdown转换器模块
提供针对不同文档框架的专用转换器
"""

from .base import BaseConverter
from .docsify import DocsifyConverter
from .mkdocs import MkDocsConverter
from .rbook import RBookConverter
from .readthedocs import ReadTheDocsConverter
from .sphinx import SphinxConverter
from .teadocs import TeadocsConverter

__all__ = [
    "BaseConverter",
    "ReadTheDocsConverter",
    "RBookConverter",
    "MkDocsConverter",
    "SphinxConverter",
    "TeadocsConverter",
    "DocsifyConverter",
]


def get_converter(framework: str) -> type:
    """
    根据框架类型获取对应的转换器

    Args:
        framework: 框架类型

    Returns:
        转换器类
    """
    converters = {
        "readthedocs": ReadTheDocsConverter,
        "rbook": RBookConverter,
        "mkdocs": MkDocsConverter,
        "sphinx": SphinxConverter,
        "teadocs": TeadocsConverter,
        "docsify": DocsifyConverter,
    }
    return converters.get(framework, BaseConverter)

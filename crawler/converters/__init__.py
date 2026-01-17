# -*- coding: utf-8 -*-
"""
HTML到Markdown转换器模块
提供统一的转换器，根据框架配置自动适配
"""

from .base import BaseConverter

__all__ = ["BaseConverter"]


def get_converter(framework: str) -> type:
    """
    获取转换器类（统一使用 BaseConverter）

    Args:
        framework: 框架类型

    Returns:
        BaseConverter 类
    """
    # 现在所有框架都使用统一的 BaseConverter
    # 通过传入 framework 参数来加载对应的配置
    return BaseConverter


def create_converter(framework: str = "unknown") -> BaseConverter:
    """
    创建转换器实例

    Args:
        framework: 框架类型

    Returns:
        BaseConverter 实例
    """
    return BaseConverter(framework)

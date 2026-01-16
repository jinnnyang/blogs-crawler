# -*- coding: utf-8 -*-
"""
工具函数模块
"""

from datetime import datetime


def format_timestamp(timestamp=None):
    """格式化时间戳"""
    if timestamp is None:
        timestamp = datetime.now()
    return timestamp.strftime('%Y-%m-%d %H:%M:%S')


def clean_text(text):
    """清理文本内容"""
    if not isinstance(text, str):
        return text
    return text.strip()

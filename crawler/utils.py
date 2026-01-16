# -*- coding: utf-8 -*-
"""
工具函数模块
"""

from datetime import datetime
from pathlib import Path
from typing import Optional
from urllib.parse import urlparse


def format_timestamp(timestamp=None):
    """格式化时间戳"""
    if timestamp is None:
        timestamp = datetime.now()
    return timestamp.strftime("%Y-%m-%d %H:%M:%S")


def clean_text(text):
    """清理文本内容"""
    if not isinstance(text, str):
        return text
    return text.strip()


def url_to_filename(url: str) -> str:
    """
    将URL转换为文件名

    Args:
        url: 页面URL

    Returns:
        文件名
    """
    parsed = urlparse(url)
    path = parsed.path

    # 移除.html扩展名
    if path.endswith(".html"):
        path = path[:-5]
    elif path.endswith(".htm"):
        path = path[:-4]

    # 如果路径以/结尾，添加index
    if path.endswith("/") or path == "":
        path = path + "index"

    # 确保路径不以/开头
    if path.startswith("/"):
        path = path[1:]

    return path


def ensure_directory(path: Path) -> Path:
    """
    确保目录存在

    Args:
        path: 目录路径

    Returns:
        目录路径
    """
    path.mkdir(parents=True, exist_ok=True)
    return path

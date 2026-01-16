# -*- coding: utf-8 -*-
"""
Teadocs专用转换器
针对Teadocs文档框架优化的HTML到Markdown转换
"""

from typing import List, Optional

from .base import BaseConverter


class TeadocsConverter(BaseConverter):
    """
    Teadocs专用转换器
    针对Teadocs的HTML结构进行优化
    """

    def extract_title(self, response) -> Optional[str]:
        """
        提取Teadocs页面标题
        """
        # 优先从主内容区提取
        title = response.css(".teadocs-container h1::text").get()
        if title:
            return title.strip()

        # 回退到通用方法
        return super().extract_title(response)

    def extract_content(self, response) -> str:
        """
        提取Teadocs页面正文内容
        """
        # 优先从主内容区提取
        content_html = response.css(".teadocs-container .content").get()
        if not content_html:
            content_html = response.css(".teadocs-container article").get()
        if not content_html:
            content_html = response.css(".teadocs-container main").get()

        if content_html:
            return self.convert(content_html)

        # 回退到通用方法
        return super().extract_content(response)

# -*- coding: utf-8 -*-
"""
RBook专用转换器
针对RBook文档框架优化的HTML到Markdown转换
"""

from typing import List, Optional

from .base import BaseConverter


class RBookConverter(BaseConverter):
    """
    RBook专用转换器
    针对RBook的HTML结构进行优化
    """

    def extract_title(self, response) -> Optional[str]:
        """
        提取RBook页面标题
        """
        # 优先从主内容区提取
        title = response.css(".rbook-container h1::text").get()
        if title:
            return title.strip()

        # 回退到通用方法
        return super().extract_title(response)

    def extract_content(self, response) -> str:
        """
        提取RBook页面正文内容
        """
        # 优先从主内容区提取
        content_html = response.css(".rbook-container .content").get()
        if not content_html:
            content_html = response.css(".rbook-container article").get()
        if not content_html:
            content_html = response.css(".rbook-container main").get()

        if content_html:
            return self.convert(content_html, base_url=response.url)

        # 回退到通用方法
        return super().extract_content(response)

# -*- coding: utf-8 -*-
"""
Sphinx专用转换器
针对Sphinx文档框架优化的HTML到Markdown转换
"""

from typing import List, Optional

from .base import BaseConverter


class SphinxConverter(BaseConverter):
    """
    Sphinx专用转换器
    针对Sphinx的HTML结构进行优化
    """

    def __init__(self):
        super().__init__()
        # Sphinx特定的标签移除
        self.strip_tags.extend(
            [
                "div.sphinxsidebar",
                "div.sphinxsidebarwrapper",
                "div.related",
            ]
        )

    def extract_title(self, response) -> Optional[str]:
        """
        提取Sphinx页面标题

        Sphinx标题通常在:
        - h1 标签
        - .document h1
        - .body h1
        """
        # 优先从主内容区提取
        title = response.css(".document h1::text").get()
        if title:
            return title.strip()

        title = response.css(".body h1::text").get()
        if title:
            return title.strip()

        # 回退到通用方法
        return super().extract_title(response)

    def extract_tags(self, response) -> List[str]:
        """
        提取Sphinx页面标签

        Sphinx标签可能来自:
        - meta keywords
        - 侧边栏导航
        """
        tags = super().extract_tags(response)

        # 尝试从侧边栏导航提取
        nav_items = response.css(".sphinxsidebar a::text").getall()
        if nav_items:
            tags.extend([n.strip() for n in nav_items if n.strip()])

        # 去重
        return list(set(tags))

    def extract_content(self, response) -> str:
        """
        提取Sphinx页面正文内容

        Sphinx主要内容在:
        - .document .body
        - .bodywrapper .body
        """
        # 优先从主内容区提取
        content_html = response.css(".document .body").get()
        if not content_html:
            content_html = response.css(".bodywrapper .body").get()

        if content_html:
            return self.convert(content_html)

        # 回退到通用方法
        return super().extract_content(response)

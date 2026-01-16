# -*- coding: utf-8 -*-
"""
Docsify专用转换器
针对Docsify文档框架优化的HTML到Markdown转换
"""

from typing import List, Optional

from .base import BaseConverter


class DocsifyConverter(BaseConverter):
    """
    Docsify专用转换器
    针对Docsify的HTML结构进行优化
    """

    def __init__(self):
        super().__init__()
        # Docsify特定的标签移除
        self.converter.strip.extend(
            [
                "nav.app-nav",
                "aside.sidebar",
            ]
        )

    def extract_title(self, response) -> Optional[str]:
        """
        提取Docsify页面标题

        Docsify标题通常在:
        - h1 标签
        - .content h1
        - article h1
        """
        # 优先从主内容区提取
        title = response.css(".content h1::text").get()
        if title:
            return title.strip()

        title = response.css("article h1::text").get()
        if title:
            return title.strip()

        # 回退到通用方法
        return super().extract_title(response)

    def extract_tags(self, response) -> List[str]:
        """
        提取Docsify页面标签

        Docsify标签可能来自:
        - meta keywords
        - 侧边栏导航
        """
        tags = super().extract_tags(response)

        # 尝试从侧边栏导航提取
        nav_items = response.css(".sidebar a::text").getall()
        if nav_items:
            tags.extend([n.strip() for n in nav_items if n.strip()])

        # 去重
        return list(set(tags))

    def extract_content(self, response) -> str:
        """
        提取Docsify页面正文内容

        Docsify主要内容在:
        - .content
        - article
        - main
        """
        # 优先从主内容区提取
        content_html = response.css(".content").get()
        if not content_html:
            content_html = response.css("article").get()
        if not content_html:
            content_html = response.css("main").get()

        if content_html:
            return self.convert(content_html)

        # 回退到通用方法
        return super().extract_content(response)

# -*- coding: utf-8 -*-
"""
MkDocs专用转换器
针对MkDocs文档框架优化的HTML到Markdown转换
"""

from typing import List, Optional

from .base import BaseConverter


class MkDocsConverter(BaseConverter):
    """
    MkDocs专用转换器
    针对MkDocs的HTML结构进行优化
    """

    def __init__(self):
        super().__init__()
        # MkDocs特定的标签移除
        self.strip_tags.extend(
            [
                "nav.md-nav",
                "div.md-sidebar",
                "header.md-header",
            ]
        )

    def extract_title(self, response) -> Optional[str]:
        """
        提取MkDocs页面标题

        MkDocs标题通常在:
        - h1 标签
        - .md-content h1
        - article h1
        """
        # 优先从主内容区提取
        title = response.css(".md-content h1::text").get()
        if title:
            return title.strip()

        title = response.css("article h1::text").get()
        if title:
            return title.strip()

        # 回退到通用方法
        return super().extract_title(response)

    def extract_tags(self, response) -> List[str]:
        """
        提取MkDocs页面标签

        MkDocs标签可能来自:
        - meta keywords
        - 侧边栏导航
        """
        tags = super().extract_tags(response)

        # 尝试从侧边栏导航提取
        nav_items = response.css(".md-nav__link::text").getall()
        if nav_items:
            tags.extend([n.strip() for n in nav_items if n.strip()])

        # 去重
        return list(set(tags))

    def extract_content(self, response) -> str:
        """
        提取MkDocs页面正文内容

        MkDocs主要内容在:
        - .md-content main
        - article
        - main
        """
        # 优先从主内容区提取
        content_html = response.css(".md-content main").get()
        if not content_html:
            content_html = response.css("article").get()
        if not content_html:
            content_html = response.css("main").get()

        if content_html:
            return self.convert(content_html)

        # 回退到通用方法
        return super().extract_content(response)

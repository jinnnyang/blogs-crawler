# -*- coding: utf-8 -*-
"""
ReadTheDocs专用转换器
针对ReadTheDocs文档框架优化的HTML到Markdown转换
"""

from typing import List, Optional

from .base import BaseConverter


class ReadTheDocsConverter(BaseConverter):
    """
    ReadTheDocs专用转换器
    针对ReadTheDocs的HTML结构进行优化
    """

    def __init__(self):
        super().__init__()
        # ReadTheDocs特定的标签移除
        self.strip_tags.extend(
            [
                "div.ethical-ad",
                "div.ethical-dark-theme",
                "div.rtd-container",
                "div.wy-nav-top",
            ]
        )

    def extract_title(self, response) -> Optional[str]:
        """
        提取ReadTheDocs页面标题

        ReadTheDocs标题通常在以下位置:
        - h1 标签
        - .wy-nav-content h1
        - .document h1
        """
        # 优先从主内容区提取
        title = response.css(".wy-nav-content h1::text").get()
        if title:
            return title.strip()

        title = response.css(".document h1::text").get()
        if title:
            return title.strip()

        # 回退到通用方法
        return super().extract_title(response)

    def extract_tags(self, response) -> List[str]:
        """
        提取ReadTheDocs页面标签

        ReadTheDocs标签可能来自:
        - meta keywords
        - .wy-nav-content .tags
        - 侧边栏中的分类
        """
        tags = super().extract_tags(response)

        # 尝试从面包屑导航提取
        breadcrumbs = response.css(".wy-breadcrumbs li a::text").getall()
        if breadcrumbs:
            tags.extend([b.strip() for b in breadcrumbs if b.strip()])

        # 去重
        return list(set(tags))

    def extract_content(self, response) -> str:
        """
        提取ReadTheDocs页面正文内容

        ReadTheDocs主要内容在:
        - .wy-nav-content .document
        - .wy-nav-content .rst-content
        - .wy-nav-content section
        """
        # 优先从主内容区提取
        content_html = response.css(".wy-nav-content .document").get()
        if not content_html:
            content_html = response.css(".wy-nav-content .rst-content").get()
        if not content_html:
            content_html = response.css(".wy-nav-content section").get()

        if content_html:
            return self.convert(content_html, base_url=response.url)

        # 回退到通用方法
        return super().extract_content(response)

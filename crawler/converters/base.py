# -*- coding: utf-8 -*-
"""
HTML到Markdown转换器基类
提供基础的HTML到Markdown转换功能
"""

from typing import List, Optional

from markdownify import markdownify as md


class BaseConverter:
    """
    HTML到Markdown转换器基类
    各框架专用转换器继承此类并重写特定方法
    """

    def __init__(self):
        # 配置markdownify选项
        self.converter = md.MarkdownConverter(
            heading_style="ATX",  # 使用 # 标题样式
            bullets="*",  # 使用 * 作为列表符号
            strip=["script", "style", "nav", "footer", "header"],  # 移除的标签
        )

    def convert(self, html: str) -> str:
        """
        将HTML转换为Markdown

        Args:
            html: HTML字符串

        Returns:
            Markdown字符串
        """
        return self.converter.convert(html)

    def extract_title(self, response) -> Optional[str]:
        """
        提取页面标题

        Args:
            response: Scrapy Response对象

        Returns:
            标题字符串或None
        """
        # 优先尝试h1标签
        title = response.css("h1::text").get()
        if title:
            return title.strip()

        # 尝试title标签
        title = response.css("title::text").get()
        if title:
            return title.strip()

        # 尝试og:title meta标签
        title = response.css('meta[property="og:title"]::attr(content)').get()
        if title:
            return title.strip()

        return None

    def extract_tags(self, response) -> List[str]:
        """
        提取页面标签

        Args:
            response: Scrapy Response对象

        Returns:
            标签列表
        """
        tags = []

        # 尝试从meta keywords提取
        keywords = response.css('meta[name="keywords"]::attr(content)').get()
        if keywords:
            tags.extend([k.strip() for k in keywords.split(",")])

        # 尝试从og:article:tag提取
        tag_elements = response.css(
            'meta[property="og:article:tag"]::attr(content)'
        ).getall()
        tags.extend([t.strip() for t in tag_elements])

        # 去重并过滤空值
        tags = list(set(tag for tag in tags if tag))

        return tags

    def extract_content(self, response) -> str:
        """
        提取页面正文内容

        Args:
            response: Scrapy Response对象

        Returns:
            Markdown格式的正文内容
        """
        # 默认提取body内容
        html = response.css("body").get()
        if html:
            return self.convert(html)

        return ""

    def process(self, response):
        """
        处理响应，提取标题、标签和内容

        Args:
            response: Scrapy Response对象

        Returns:
            dict: 包含title, tags, content的字典
        """
        return {
            "title": self.extract_title(response),
            "tags": self.extract_tags(response),
            "content": self.extract_content(response),
        }

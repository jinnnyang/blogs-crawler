# -*- coding: utf-8 -*-
"""
工具类模块
提供 URL 转换、HTML 清理等通用工具函数
"""

import logging
from typing import Optional
from urllib.parse import urljoin

from bs4 import BeautifulSoup

logger = logging.getLogger(__name__)


class UrlNormalizer:
    """
    URL 标准化工具类
    处理相对路径到绝对路径的转换
    """

    @staticmethod
    def convert_relative_urls(soup: BeautifulSoup, base_url: str) -> None:
        """
        将 HTML 中的相对路径转换为绝对路径

        Args:
            soup: BeautifulSoup 对象
            base_url: 基础 URL
        """

        if not base_url:
            return

        # 处理 img 标签的 src 属性
        for img in soup.find_all("img"):
            if img.get("src"):
                img["src"] = urljoin(base_url, img["src"])
                logger.debug(f"[UrlNormalizer] Converted img src: {img['src']}")

        # 处理 a 标签的 href 属性
        for a in soup.find_all("a"):
            if a.get("href"):
                a["href"] = urljoin(base_url, a["href"])
                logger.debug(f"[UrlNormalizer] Converted a href: {a['href']}")

        # 处理 link 标签的 href 属性
        for link in soup.find_all("link"):
            if link.get("href"):
                link["href"] = urljoin(base_url, link["href"])
                logger.debug(f"[UrlNormalizer] Converted link href: {link['href']}")

        # 处理 script 标签的 src 属性
        for script in soup.find_all("script"):
            if script.get("src"):
                script["src"] = urljoin(base_url, script["src"])
                logger.debug(f"[UrlNormalizer] Converted script src: {script['src']}")

        # 处理 source 标签的 src 属性
        for source in soup.find_all("source"):
            if source.get("src"):
                source["src"] = urljoin(base_url, source["src"])
                logger.debug(f"[UrlNormalizer] Converted source src: {source['src']}")

        # 处理 video 标签的 src 和 poster 属性
        for video in soup.find_all("video"):
            if video.get("src"):
                video["src"] = urljoin(base_url, video["src"])
                logger.debug(f"[UrlNormalizer] Converted video src: {video['src']}")
            if video.get("poster"):
                video["poster"] = urljoin(base_url, video["poster"])
                logger.debug(
                    f"[UrlNormalizer] Converted video poster: {video['poster']}"
                )

        # 处理 audio 标签的 src 属性
        for audio in soup.find_all("audio"):
            if audio.get("src"):
                audio["src"] = urljoin(base_url, audio["src"])
                logger.debug(f"[UrlNormalizer] Converted audio src: {audio['src']}")

        # 处理 iframe 标签的 src 属性
        for iframe in soup.find_all("iframe"):
            if iframe.get("src"):
                iframe["src"] = urljoin(base_url, iframe["src"])
                logger.debug(f"[UrlNormalizer] Converted iframe src: {iframe['src']}")

        # 处理 embed 标签的 src 属性
        for embed in soup.find_all("embed"):
            if embed.get("src"):
                embed["src"] = urljoin(base_url, embed["src"])
                logger.debug(f"[UrlNormalizer] Converted embed src: {embed['src']}")

        # 处理 object 标签的 data 属性
        for obj in soup.find_all("object"):
            if obj.get("data"):
                obj["data"] = urljoin(base_url, obj["data"])
                logger.debug(f"[UrlNormalizer] Converted object data: {obj['data']}")


class HtmlCleaner:
    """
    HTML 清理工具类
    处理 HTML 标签的移除和清理
    """

    @staticmethod
    def strip_tags(soup: BeautifulSoup, tags: list) -> None:
        """
        移除指定的 HTML 标签

        Args:
            soup: BeautifulSoup 对象
            tags: 需要移除的标签列表
        """
        for tag in tags:
            for element in soup.find_all(tag):
                element.decompose()
                logger.debug(f"[HtmlCleaner] Removed tag: {tag}")


class SelectorHelper:
    """
    CSS 选择器辅助工具类
    提供便捷的选择器查询方法
    """

    @staticmethod
    def extract_first_text(response, selectors: list) -> Optional[str]:
        """
        使用多个选择器依次尝试提取文本

        Args:
            response: Scrapy Response 对象
            selectors: CSS 选择器列表

        Returns:
            提取到的文本，如果未找到则返回 None
        """
        for selector in selectors:
            text = response.css(f"{selector}::text").get()
            if text:
                text = text.strip()
                if text:
                    logger.debug(
                        f"[SelectorHelper] Found text with selector: {selector}"
                    )
                    return text
        return None

    @staticmethod
    def extract_first_html(response, selectors: list) -> Optional[str]:
        """
        使用多个选择器依次尝试提取 HTML

        Args:
            response: Scrapy Response 对象
            selectors: CSS 选择器列表

        Returns:
            提取到的 HTML，如果未找到则返回 None
        """
        for selector in selectors:
            html = response.css(selector).get()
            if html:
                logger.debug(f"[SelectorHelper] Found HTML with selector: {selector}")
                return html
        return None

    @staticmethod
    def extract_all_texts(response, selectors: list) -> list:
        """
        使用多个选择器提取所有文本

        Args:
            response: Scrapy Response 对象
            selectors: CSS 选择器列表

        Returns:
            提取到的文本列表
        """
        texts = []
        for selector in selectors:
            texts.extend(response.css(f"{selector}::text").getall())
        # 去重并过滤空值
        texts = list(set(t.strip() for t in texts if t and t.strip()))
        return texts

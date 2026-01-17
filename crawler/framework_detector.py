# -*- coding: utf-8 -*-
"""
文档框架检测模块
通过HTML特征检测文档站点使用的框架
"""

import logging
from typing import Optional
from urllib.parse import urlparse

from crawler.config_loader import get_config_loader

logger = logging.getLogger(__name__)


class FrameworkDetector:
    """
    文档框架检测器
    支持检测: ReadTheDocs, RBook, MkDocs, Sphinx, Teadocs, Docsify
    支持框架检测结果缓存
    """

    # 类级别的缓存，用于存储域名到框架的映射
    _domain_cache: dict = {}

    def __init__(self):
        """初始化框架检测器"""
        self.config_loader = get_config_loader()

    @classmethod
    def detect(cls, response) -> str:
        """
        检测文档框架类型

        Args:
            response: Scrapy Response对象

        Returns:
            str: 框架类型 ('readthedocs', 'rbook', 'mkdocs', 'sphinx', 'teadocs', 'docsify', 'unknown')
        """
        detector = cls()
        return detector._detect(response)

    def _detect(self, response) -> str:
        """
        检测文档框架类型（实例方法）

        Args:
            response: Scrapy Response对象

        Returns:
            str: 框架类型
        """
        # 1. 先通过URL域名检测（使用缓存）
        framework = self._detect_by_url(response.url)
        if framework != "unknown":
            logger.debug(f"[FrameworkDetector] Detected by URL: {framework}")
            return framework

        # 2. 通过HTML特征检测
        framework = self._detect_by_html(response)
        if framework != "unknown":
            logger.debug(f"[FrameworkDetector] Detected by HTML: {framework}")
            return framework

        # 3. 通过meta标签检测
        framework = self._detect_by_meta(response)
        if framework != "unknown":
            logger.debug(f"[FrameworkDetector] Detected by meta: {framework}")
            return framework

        logger.debug(f"[FrameworkDetector] Unknown framework for {response.url}")
        return "unknown"

    def _detect_by_url(self, url: str) -> str:
        """
        通过URL检测框架（带缓存）

        Args:
            url: 页面URL

        Returns:
            str: 框架类型
        """
        parsed = urlparse(url)
        domain = parsed.netloc.lower()
        path = parsed.path.lower()

        # 检查缓存
        if domain in self._domain_cache:
            cached_framework = self._domain_cache[domain]
            logger.debug(
                f"[FrameworkDetector] Cache hit for domain: {domain} -> {cached_framework}"
            )
            return cached_framework

        # 从配置获取所有框架的 URL 模式
        frameworks = self.config_loader.get_supported_frameworks()
        for framework in frameworks:
            patterns = self.config_loader.get_patterns(framework)
            url_patterns = patterns.get("url", [])
            for pattern in url_patterns:
                if pattern in domain or pattern in path:
                    # 缓存结果
                    self._domain_cache[domain] = framework
                    logger.debug(
                        f"[FrameworkDetector] Cached framework for domain: {domain} -> {framework}"
                    )
                    return framework

        return "unknown"

    def _detect_by_html(self, response) -> str:
        """
        通过HTML特征检测框架

        Args:
            response: Scrapy Response对象

        Returns:
            str: 框架类型
        """
        html = response.text.lower()

        # 从配置获取所有框架的 HTML 模式
        frameworks = self.config_loader.get_supported_frameworks()
        for framework in frameworks:
            patterns = self.config_loader.get_patterns(framework)
            html_patterns = patterns.get("html", [])
            for pattern in html_patterns:
                if pattern in html:
                    return framework

        return "unknown"

    def _detect_by_meta(self, response) -> str:
        """
        通过meta标签检测框架

        Args:
            response: Scrapy Response对象

        Returns:
            str: 框架类型
        """
        # 检查generator meta标签
        generator = response.css('meta[name="generator"]::attr(content)').get()
        if generator:
            generator = generator.lower()
            if "mkdocs" in generator:
                return "mkdocs"
            elif "sphinx" in generator:
                return "sphinx"

        # 检查theme meta标签
        theme = response.css('meta[name="theme"]::attr(content)').get()
        if theme:
            theme = theme.lower()
            if "docsify" in theme:
                return "docsify"

        return "unknown"

    def get_link_extractor_config(self, framework: str) -> dict:
        """
        获取框架的链接提取器配置

        Args:
            framework: 框架类型

        Returns:
            包含 allow、deny 规则的字典
        """
        return self.config_loader.get_link_extractor_config(framework)

    @classmethod
    def clear_cache(cls):
        """清除框架检测缓存"""
        cls._domain_cache.clear()
        logger.info("[FrameworkDetector] Cache cleared")

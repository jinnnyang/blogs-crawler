# -*- coding: utf-8 -*-
"""
文档框架检测模块
通过HTML特征检测文档站点使用的框架
"""

import logging
from typing import Optional
from urllib.parse import urlparse

logger = logging.getLogger(__name__)


class FrameworkDetector:
    """
    文档框架检测器
    支持检测: ReadTheDocs, RBook, MkDocs, Sphinx, Teadocs, Docsify
    """

    # 各框架的特征标识
    FRAMEWORK_PATTERNS = {
        "readthedocs": [
            "readthedocs.io",
            "readthedocs.org",
            "ethical-ad-client",
            "rtd-container",
            "wy-nav-top",
            "wy-nav-content",
        ],
        "rbook": [
            "rbook",
            "rbook-theme",
            "rbook-container",
        ],
        "mkdocs": [
            "mkdocs",
            "mkdocs-theme",
            "md-container",
            "md-sidebar",
            "md-content",
        ],
        "sphinx": [
            "sphinx",
            "sphinx-theme",
            "sphinxsidebar",
            "sphinxsidebarwrapper",
            "document",
            "bodywrapper",
        ],
        "teadocs": [
            "teadocs",
            "teadocs-theme",
            "teadocs-container",
        ],
        "docsify": [
            "docsify",
            "data-name",
            "data-repo",
            "docsify-themeable",
        ],
    }

    @classmethod
    def detect(cls, response) -> str:
        """
        检测文档框架类型

        Args:
            response: Scrapy Response对象

        Returns:
            str: 框架类型 ('readthedocs', 'rbook', 'mkdocs', 'sphinx', 'teadocs', 'docsify', 'unknown')
        """
        # 1. 先通过URL域名检测
        framework = cls._detect_by_url(response.url)
        if framework != "unknown":
            logger.debug(f"[FrameworkDetector] Detected by URL: {framework}")
            return framework

        # 2. 通过HTML特征检测
        framework = cls._detect_by_html(response)
        if framework != "unknown":
            logger.debug(f"[FrameworkDetector] Detected by HTML: {framework}")
            return framework

        # 3. 通过meta标签检测
        framework = cls._detect_by_meta(response)
        if framework != "unknown":
            logger.debug(f"[FrameworkDetector] Detected by meta: {framework}")
            return framework

        logger.debug(f"[FrameworkDetector] Unknown framework for {response.url}")
        return "unknown"

    @classmethod
    def _detect_by_url(cls, url: str) -> str:
        """
        通过URL检测框架

        Args:
            url: 页面URL

        Returns:
            str: 框架类型
        """
        parsed = urlparse(url)
        domain = parsed.netloc.lower()
        path = parsed.path.lower()

        # ReadTheDocs
        if "readthedocs.io" in domain or "readthedocs.org" in domain:
            return "readthedocs"

        return "unknown"

    @classmethod
    def _detect_by_html(cls, response) -> str:
        """
        通过HTML特征检测框架

        Args:
            response: Scrapy Response对象

        Returns:
            str: 框架类型
        """
        html = response.text.lower()

        for framework, patterns in cls.FRAMEWORK_PATTERNS.items():
            for pattern in patterns:
                if pattern in html:
                    return framework

        return "unknown"

    @classmethod
    def _detect_by_meta(cls, response) -> str:
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

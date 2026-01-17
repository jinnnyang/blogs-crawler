# -*- coding: utf-8 -*-
"""
框架检测器测试
"""

import os
import unittest
from unittest.mock import MagicMock, patch

from crawler.config_loader import FrameworkConfigLoader
from crawler.framework_detector import FrameworkDetector


class TestFrameworkDetector(unittest.TestCase):
    """框架检测器测试类"""

    def setUp(self):
        """测试前准备"""
        # 清除缓存
        FrameworkDetector._domain_cache.clear()
        # 清除单例
        FrameworkConfigLoader._instance = None
        self.detector = FrameworkDetector()
        config_path = os.path.join(
            os.path.dirname(__file__), "..", "crawler", "framework_config.yaml"
        )
        self.detector.config_loader = FrameworkConfigLoader(config_path)

    def tearDown(self):
        """测试后清理"""
        FrameworkDetector._domain_cache.clear()

    def test_detect_by_url_readthedocs(self):
        """测试通过URL检测ReadTheDocs"""
        mock_response = MagicMock()
        mock_response.url = "https://docs.readthedocs.io/en/latest/index.html"
        framework = self.detector._detect_by_url(mock_response.url)
        self.assertEqual(framework, "readthedocs")

    def test_detect_by_url_unknown(self):
        """测试未知URL返回unknown"""
        mock_response = MagicMock()
        mock_response.url = "https://example.com/index.html"
        framework = self.detector._detect_by_url(mock_response.url)
        self.assertEqual(framework, "unknown")

    def test_detect_by_html_readthedocs(self):
        """测试通过HTML特征检测ReadTheDocs"""
        mock_response = MagicMock()
        mock_response.text = '<div class="wy-nav-top">ReadTheDocs</div>'
        framework = self.detector._detect_by_html(mock_response)
        self.assertEqual(framework, "readthedocs")

    def test_detect_by_html_mkdocs(self):
        """测试通过HTML特征检测MkDocs"""
        mock_response = MagicMock()
        mock_response.text = '<div class="md-sidebar">MkDocs</div>'
        framework = self.detector._detect_by_html(mock_response)
        self.assertEqual(framework, "mkdocs")

    def test_detect_by_meta_mkdocs(self):
        """测试通过meta标签检测MkDocs"""
        mock_response = MagicMock()
        mock_response.css.return_value.get.return_value = "MkDocs 1.5"
        framework = self.detector._detect_by_meta(mock_response)
        self.assertEqual(framework, "mkdocs")

    def test_detect_by_meta_sphinx(self):
        """测试通过meta标签检测Sphinx"""
        mock_response = MagicMock()
        mock_response.css.return_value.get.return_value = "Sphinx 4.0"
        framework = self.detector._detect_by_meta(mock_response)
        self.assertEqual(framework, "sphinx")

    def test_detect_by_meta_docsify(self):
        """测试通过meta标签检测Docsify"""
        mock_response = MagicMock()
        mock_response.css.return_value.get.return_value = "docsify"
        framework = self.detector._detect_by_meta(mock_response)
        self.assertEqual(framework, "docsify")

    def test_domain_cache(self):
        """测试域名缓存功能"""
        url = "https://docs.readthedocs.io/test.html"
        # 第一次检测
        framework1 = self.detector._detect_by_url(url)
        # 第二次检测应该从缓存获取
        framework2 = self.detector._detect_by_url(url)
        self.assertEqual(framework1, framework2)
        self.assertIn("docs.readthedocs.io", FrameworkDetector._domain_cache)

    def test_clear_cache(self):
        """测试清除缓存"""
        url = "https://docs.readthedocs.io/test.html"
        self.detector._detect_by_url(url)
        self.assertTrue(len(FrameworkDetector._domain_cache) > 0)
        FrameworkDetector.clear_cache()
        self.assertEqual(len(FrameworkDetector._domain_cache), 0)

    def test_get_link_extractor_config(self):
        """测试获取链接提取器配置"""
        config = self.detector.get_link_extractor_config("readthedocs")
        self.assertIn("allow", config)
        self.assertIn("deny", config)


if __name__ == "__main__":
    unittest.main()

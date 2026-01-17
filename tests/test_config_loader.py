# -*- coding: utf-8 -*-
"""
配置加载器测试
"""

import os
import unittest
from unittest.mock import MagicMock, patch

from crawler.config_loader import FrameworkConfigLoader


class TestFrameworkConfigLoader(unittest.TestCase):
    """配置加载器测试类"""

    def setUp(self):
        """测试前准备"""
        # 清除单例
        FrameworkConfigLoader._instance = None
        self.config_path = os.path.join(
            os.path.dirname(__file__), "..", "crawler", "framework_config.yaml"
        )

    def test_singleton_pattern(self):
        """测试单例模式"""
        loader1 = FrameworkConfigLoader(self.config_path)
        loader2 = FrameworkConfigLoader(self.config_path)
        self.assertIs(loader1, loader2)

    def test_load_config(self):
        """测试加载配置"""
        loader = FrameworkConfigLoader(self.config_path)
        self.assertIsNotNone(loader._config)
        self.assertIn("frameworks", loader._config)

    def test_get_framework_config(self):
        """测试获取框架配置"""
        loader = FrameworkConfigLoader(self.config_path)
        config = loader.get_framework_config("readthedocs")
        self.assertIn("patterns", config)
        self.assertIn("selectors", config)
        self.assertIn("strip_tags", config)
        self.assertIn("link_extractor", config)

    def test_get_selectors(self):
        """测试获取选择器"""
        loader = FrameworkConfigLoader(self.config_path)
        selectors = loader.get_selectors("readthedocs")
        self.assertIn("title", selectors)
        self.assertIn("content", selectors)
        self.assertIn("tags", selectors)

    def test_get_strip_tags(self):
        """测试获取需要移除的标签"""
        loader = FrameworkConfigLoader(self.config_path)
        strip_tags = loader.get_strip_tags("readthedocs")
        self.assertIsInstance(strip_tags, list)
        self.assertIn("script", strip_tags)

    def test_get_link_extractor_config(self):
        """测试获取链接提取器配置"""
        loader = FrameworkConfigLoader(self.config_path)
        config = loader.get_link_extractor_config("readthedocs")
        self.assertIn("allow", config)
        self.assertIn("deny", config)

    def test_get_supported_frameworks(self):
        """测试获取支持的框架列表"""
        loader = FrameworkConfigLoader(self.config_path)
        frameworks = loader.get_supported_frameworks()
        self.assertIn("readthedocs", frameworks)
        self.assertIn("mkdocs", frameworks)
        self.assertIn("sphinx", frameworks)

    def test_unknown_framework(self):
        """测试未知框架返回默认配置"""
        loader = FrameworkConfigLoader(self.config_path)
        config = loader.get_framework_config("nonexistent")
        self.assertIsNotNone(config)


if __name__ == "__main__":
    unittest.main()

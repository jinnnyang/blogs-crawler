# -*- coding: utf-8 -*-
"""
转换器测试
"""

import os
import unittest
from unittest.mock import MagicMock, patch

from crawler.config_loader import FrameworkConfigLoader
from crawler.converters import BaseConverter


class TestBaseConverter(unittest.TestCase):
    """转换器测试类"""

    def setUp(self):
        """测试前准备"""
        # 清除单例
        FrameworkConfigLoader._instance = None
        config_path = os.path.join(
            os.path.dirname(__file__), "..", "crawler", "framework_config.yaml"
        )
        FrameworkConfigLoader._config_path = config_path
        self.converter = BaseConverter("readthedocs")

    def test_init(self):
        """测试初始化"""
        self.assertEqual(self.converter.framework, "readthedocs")
        self.assertIsNotNone(self.converter.strip_tags)

    def test_convert_html(self):
        """测试HTML到Markdown转换"""
        html = "<h1>Title</h1><p>Content</p>"
        result = self.converter.convert(html)
        self.assertIn("# Title", result)
        self.assertIn("Content", result)

    def test_convert_with_strip_tags(self):
        """测试移除指定标签"""
        html = "<h1>Title</h1><script>alert('test');</script><p>Content</p>"
        result = self.converter.convert(html)
        self.assertNotIn("alert('test')", result)
        self.assertIn("Title", result)
        self.assertIn("Content", result)

    def test_extract_title_from_h1(self):
        """测试从h1标签提取标题"""
        mock_response = MagicMock()
        mock_response.css.return_value.get.return_value = "Test Title"
        title = self.converter.extract_title(mock_response)
        self.assertEqual(title, "Test Title")

    def test_extract_title_from_og_meta(self):
        """测试从og:title meta标签提取标题"""
        mock_response = MagicMock()
        mock_response.css.side_effect = lambda x: MagicMock(get=lambda y: None)
        # 第二次调用返回 og:title
        mock_response.css.side_effect = [
            MagicMock(get=lambda y: None),  # h1
            MagicMock(get=lambda y: None),  # title
            MagicMock(get=lambda y: "OG Title"),  # og:title
        ]
        title = self.converter.extract_title(mock_response)
        self.assertEqual(title, "OG Title")

    def test_extract_tags_from_meta(self):
        """测试从meta keywords提取标签"""
        mock_response = MagicMock()
        mock_response.css.side_effect = [
            MagicMock(get=lambda y: "tag1, tag2, tag3"),  # keywords
            MagicMock(getall=lambda: []),  # og:article:tag
        ]
        tags = self.converter.extract_tags(mock_response)
        self.assertIn("tag1", tags)
        self.assertIn("tag2", tags)
        self.assertIn("tag3", tags)

    def test_extract_content_from_body(self):
        """测试从body提取内容"""
        mock_response = MagicMock()
        mock_response.css.return_value.get.return_value = "<h1>Title</h1><p>Content</p>"
        content = self.converter.extract_content(mock_response)
        self.assertIn("# Title", content)
        self.assertIn("Content", content)

    def test_process(self):
        """测试处理响应"""
        mock_response = MagicMock()
        mock_response.url = "https://example.com/test.html"
        mock_response.css.side_effect = [
            MagicMock(get=lambda y: "Test Title"),  # title
            MagicMock(get=lambda y: "tag1, tag2"),  # keywords
            MagicMock(getall=lambda: []),  # og:article:tag
            MagicMock(get=lambda y: "<h1>Title</h1><p>Content</p>"),  # content
        ]
        result = self.converter.process(mock_response)
        self.assertEqual(result["title"], "Test Title")
        self.assertIn("tag1", result["tags"])
        self.assertIn("tag2", result["tags"])
        self.assertIn("# Title", result["content"])

    def test_unknown_framework(self):
        """测试未知框架使用默认配置"""
        converter = BaseConverter("nonexistent")
        self.assertIsNotNone(converter.strip_tags)
        self.assertIn("script", converter.strip_tags)


if __name__ == "__main__":
    unittest.main()

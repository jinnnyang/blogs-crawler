# -*- coding: utf-8 -*-
"""
工具类测试
"""

import unittest
from unittest.mock import MagicMock

from bs4 import BeautifulSoup

from crawler.utils import HtmlCleaner, SelectorHelper, UrlNormalizer


class TestUrlNormalizer(unittest.TestCase):
    """URL标准化工具类测试"""

    def test_convert_img_src(self):
        """测试转换img标签的src属性"""
        html = '<img src="/images/test.png">'
        soup = BeautifulSoup(html, "lxml")
        UrlNormalizer.convert_relative_urls(soup, "https://example.com")
        img = soup.find("img")
        self.assertEqual(img["src"], "https://example.com/images/test.png")

    def test_convert_a_href(self):
        """测试转换a标签的href属性"""
        html = '<a href="/page.html">Link</a>'
        soup = BeautifulSoup(html, "lxml")
        UrlNormalizer.convert_relative_urls(soup, "https://example.com")
        a = soup.find("a")
        self.assertEqual(a["href"], "https://example.com/page.html")

    def test_convert_link_href(self):
        """测试转换link标签的href属性"""
        html = '<link href="/style.css">'
        soup = BeautifulSoup(html, "lxml")
        UrlNormalizer.convert_relative_urls(soup, "https://example.com")
        link = soup.find("link")
        self.assertEqual(link["href"], "https://example.com/style.css")

    def test_convert_script_src(self):
        """测试转换script标签的src属性"""
        html = '<script src="/script.js"></script>'
        soup = BeautifulSoup(html, "lxml")
        UrlNormalizer.convert_relative_urls(soup, "https://example.com")
        script = soup.find("script")
        self.assertEqual(script["src"], "https://example.com/script.js")

    def test_convert_absolute_url(self):
        """测试绝对URL不被修改"""
        html = '<img src="https://cdn.example.com/image.png">'
        soup = BeautifulSoup(html, "lxml")
        UrlNormalizer.convert_relative_urls(soup, "https://example.com")
        img = soup.find("img")
        self.assertEqual(img["src"], "https://cdn.example.com/image.png")

    def test_convert_with_none_base_url(self):
        """测试base_url为None时不转换"""
        html = '<img src="/images/test.png">'
        soup = BeautifulSoup(html, "lxml")
        UrlNormalizer.convert_relative_urls(soup, None)
        img = soup.find("img")
        self.assertEqual(img["src"], "/images/test.png")


class TestHtmlCleaner(unittest.TestCase):
    """HTML清理工具类测试"""

    def test_strip_single_tag(self):
        """测试移除单个标签"""
        html = '<h1>Title</h1><script>alert("test");</script><p>Content</p>'
        soup = BeautifulSoup(html, "lxml")
        HtmlCleaner.strip_tags(soup, ["script"])
        self.assertIsNone(soup.find("script"))
        self.assertIsNotNone(soup.find("h1"))
        self.assertIsNotNone(soup.find("p"))

    def test_strip_multiple_tags(self):
        """测试移除多个标签"""
        html = '<h1>Title</h1><script>alert("test");</script><style>body{}</style><p>Content</p>'
        soup = BeautifulSoup(html, "lxml")
        HtmlCleaner.strip_tags(soup, ["script", "style"])
        self.assertIsNone(soup.find("script"))
        self.assertIsNone(soup.find("style"))
        self.assertIsNotNone(soup.find("h1"))
        self.assertIsNotNone(soup.find("p"))

    def test_strip_all_tags(self):
        """测试移除所有指定标签"""
        html = "<h1>Title</h1><p>Content</p>"
        soup = BeautifulSoup(html, "lxml")
        HtmlCleaner.strip_tags(soup, ["h1", "p"])
        self.assertIsNone(soup.find("h1"))
        self.assertIsNone(soup.find("p"))


class TestSelectorHelper(unittest.TestCase):
    """CSS选择器辅助工具类测试"""

    def test_extract_first_text(self):
        """测试提取第一个文本"""
        mock_response = MagicMock()
        mock_response.css.side_effect = [
            MagicMock(get=lambda y: "First Title"),  # 第一个选择器
            MagicMock(get=lambda y: "Second Title"),  # 第二个选择器
        ]
        text = SelectorHelper.extract_first_text(mock_response, [".title", "h1"])
        self.assertEqual(text, "First Title")

    def test_extract_first_text_fallback(self):
        """测试回退到下一个选择器"""
        mock_response = MagicMock()
        mock_response.css.side_effect = [
            MagicMock(get=lambda y: None),  # 第一个选择器无结果
            MagicMock(get=lambda y: "Fallback Title"),  # 第二个选择器有结果
        ]
        text = SelectorHelper.extract_first_text(mock_response, [".title", "h1"])
        self.assertEqual(text, "Fallback Title")

    def test_extract_first_text_none(self):
        """测试所有选择器都无结果"""
        mock_response = MagicMock()
        mock_response.css.return_value.get.return_value = None
        text = SelectorHelper.extract_first_text(mock_response, [".title", "h1"])
        self.assertIsNone(text)

    def test_extract_first_html(self):
        """测试提取第一个HTML"""
        mock_response = MagicMock()
        mock_response.css.side_effect = [
            MagicMock(get=lambda y: "<div>First</div>"),  # 第一个选择器
            MagicMock(get=lambda y: "<div>Second</div>"),  # 第二个选择器
        ]
        html = SelectorHelper.extract_first_html(mock_response, [".content", "body"])
        self.assertEqual(html, "<div>First</div>")

    def test_extract_all_texts(self):
        """测试提取所有文本"""
        mock_response = MagicMock()
        mock_response.css.side_effect = [
            MagicMock(getall=lambda y: ["Tag1", "Tag2"]),  # 第一个选择器
            MagicMock(getall=lambda y: ["Tag3"]),  # 第二个选择器
        ]
        texts = SelectorHelper.extract_all_texts(
            mock_response, [".tags", ".categories"]
        )
        self.assertIn("Tag1", texts)
        self.assertIn("Tag2", texts)
        self.assertIn("Tag3", texts)

    def test_extract_all_texts_deduplicate(self):
        """测试去重"""
        mock_response = MagicMock()
        mock_response.css.side_effect = [
            MagicMock(getall=lambda y: ["Tag1", "Tag2"]),  # 第一个选择器
            MagicMock(getall=lambda y: ["Tag1", "Tag3"]),  # 第二个选择器（Tag1重复）
        ]
        texts = SelectorHelper.extract_all_texts(
            mock_response, [".tags", ".categories"]
        )
        self.assertEqual(len(texts), 3)  # Tag1只出现一次
        self.assertIn("Tag1", texts)
        self.assertIn("Tag2", texts)
        self.assertIn("Tag3", texts)


if __name__ == "__main__":
    unittest.main()

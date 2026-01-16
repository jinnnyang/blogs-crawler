# -*- coding: utf-8 -*-
"""
数据处理管道
包含Markdown保存管道，支持YAML metadata
"""

from datetime import datetime
from pathlib import Path
from urllib.parse import urlparse

import yaml
from itemadapter import ItemAdapter


class MarkdownSavePipeline:
    """
    Markdown保存管道
    将数据保存为Markdown文件，包含YAML metadata
    """

    def __init__(self, output_dir="output"):
        """
        初始化管道

        Args:
            output_dir: 输出目录
        """
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)

    @classmethod
    def from_crawler(cls, crawler):
        """
        从crawler创建管道实例

        Args:
            crawler: Scrapy crawler对象

        Returns:
            MarkdownSavePipeline实例
        """
        output_dir = crawler.settings.get("OUTPUT_DIR", "output")
        pipeline = cls(output_dir)
        # 保存crawler实例以便后续访问spider
        pipeline.crawler = crawler
        return pipeline

    def open_spider(self):
        """
        Spider打开时的回调
        """
        spider = self.crawler.spider
        spider.logger.info(f"MarkdownSavePipeline opened for spider: {spider.name}")

    def process_item(self, item):
        """
        处理item，保存为Markdown文件

        Args:
            item: BlogItem对象

        Returns:
            处理后的item
        """
        spider = self.crawler.spider
        adapter = ItemAdapter(item)

        # 获取URL
        url = adapter.get("url")
        if not url:
            spider.logger.warning(f"Item missing URL, skipping")
            return item

        # 生成输出路径
        output_path = self._generate_output_path(url)
        adapter["output_path"] = str(output_path)

        # 确保目录存在
        output_path.parent.mkdir(parents=True, exist_ok=True)

        # 构建YAML metadata
        metadata = self._build_metadata(adapter)

        # 获取内容
        content = adapter.get("content", "")

        # 构建完整的Markdown内容
        markdown_content = self._build_markdown(metadata, content)

        # 写入文件
        try:
            with open(output_path, "w", encoding="utf-8") as f:
                f.write(markdown_content)
            spider.logger.info(f"Saved: {output_path}")
        except Exception as e:
            spider.logger.error(f"Failed to save {output_path}: {e}")

        return item

    def _generate_output_path(self, url: str) -> Path:
        """
        根据URL生成输出路径

        Args:
            url: 页面URL

        Returns:
            输出文件路径

        Examples:
            https://example.com/ -> output/example.com/index.md
            https://example.com/path/to/page.html -> output/example.com/path/to/page.md
            https://docs.python.org/3/library/ -> output/docs.python.org/3/library/index.md
        """
        parsed = urlparse(url)

        # 获取域名和路径
        domain = parsed.netloc
        path = parsed.path

        # 处理路径
        if not path or path == "/":
            # 根路径
            output_path = self.output_dir / domain / "index.md"
        else:
            # 移除.html扩展名（如果有）
            if path.endswith(".html"):
                path = path[:-5]
            elif path.endswith(".htm"):
                path = path[:-4]

            # 如果路径以/结尾，添加index
            if path.endswith("/"):
                path = path + "index"

            # 确保路径不以/开头
            if path.startswith("/"):
                path = path[1:]

            output_path = self.output_dir / domain / f"{path}.md"

        return output_path

    def _build_metadata(self, adapter: ItemAdapter) -> dict:
        """
        构建YAML metadata

        Args:
            adapter: ItemAdapter对象

        Returns:
            metadata字典
        """
        metadata = {}

        # 添加URL
        if adapter.get("url"):
            metadata["url"] = adapter["url"]

        # 添加标题
        if adapter.get("title"):
            metadata["title"] = adapter["title"]

        # 添加标签
        if adapter.get("tags"):
            metadata["tags"] = adapter["tags"]

        # 添加框架类型
        if adapter.get("framework"):
            metadata["framework"] = adapter["framework"]

        # 添加爬取时间
        if adapter.get("crawl_time"):
            metadata["crawl_time"] = adapter["crawl_time"]
        else:
            metadata["crawl_time"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        return metadata

    def _build_markdown(self, metadata: dict, content: str) -> str:
        """
        构建完整的Markdown内容

        Args:
            metadata: metadata字典
            content: Markdown内容

        Returns:
            完整的Markdown内容（包含YAML metadata）
        """
        # 转换metadata为YAML
        yaml_str = yaml.dump(metadata, default_flow_style=False, allow_unicode=True)

        # 构建完整的Markdown
        markdown = f"---\n{yaml_str}---\n\n{content}"

        return markdown

    def close_spider(self):
        """
        Spider关闭时的回调
        """
        spider = self.crawler.spider
        spider.logger.info(f"MarkdownSavePipeline closed for spider: {spider.name}")

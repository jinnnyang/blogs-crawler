# -*- coding: utf-8 -*-
# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

import os
from datetime import datetime
from pathlib import Path

from itemadapter import ItemAdapter


class DataCleaningPipeline:
    """
    数据清洗管道
    去除空白字符、清理空值等
    """

    def process_item(self, item):
        adapter = ItemAdapter(item)

        for field in adapter.field_names():
            value = adapter.get(field)

            if value is None:
                continue

            # 处理字符串类型
            if isinstance(value, str):
                # 去除首尾空白
                adapter[field] = value.strip()
            # 处理列表类型
            elif isinstance(value, list):
                # 清理列表中的字符串
                adapter[field] = [
                    v.strip() if isinstance(v, str) else v for v in value if v
                ]

        return item


class ValidationPipeline:
    """
    数据验证管道
    验证必填字段
    """

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler)

    def __init__(self, crawler):
        self.crawler = crawler

    def process_item(self, item):
        adapter = ItemAdapter(item)

        # 检查必填字段
        required_fields = ["url"]

        for field in required_fields:
            if not adapter.get(field):
                self.crawler.spider.logger.warning(f"Missing required field: {field}")
                item["status"] = "invalid"
                return item

        item["status"] = "valid"
        return item


class FileSavePipeline:
    """
    文件保存管道
    将数据保存到 output/ 目录
    """

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler)

    def __init__(self, crawler):
        self.crawler = crawler
        self.output_dir = Path("output")
        self.output_dir.mkdir(exist_ok=True)
        self.files = {}

    def open_spider(self):
        self.crawler.spider.logger.info(
            f"FileSavePipeline opened for spider: {self.crawler.spider.name}"
        )

    def process_item(self, item):
        adapter = ItemAdapter(item)
        spider_name = self.crawler.spider.name

        # 获取输出文件路径
        output_file = self.output_dir / f"{spider_name}.txt"

        # 格式化数据
        timestamp = adapter.get(
            "crawl_time", datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        )
        url = adapter.get("url", "")
        title = adapter.get("title", "")
        content = adapter.get("content", "")

        # 写入文件
        with open(output_file, "a", encoding="utf-8") as f:
            f.write(f"{'=' * 60}\n")
            f.write(f"URL: {url}\n")
            f.write(f"Title: {title}\n")
            f.write(f"Time: {timestamp}\n")
            f.write(f"{'=' * 60}\n")
            f.write(f"{content}\n")
            f.write(f"\n{'=' * 60}\n\n")

        self.crawler.spider.logger.debug(f"Saved item to: {output_file}")
        return item

    def close_spider(self):
        self.crawler.spider.logger.info(
            f"FileSavePipeline closed for spider: {self.crawler.spider.name}"
        )


class JsonSavePipeline:
    """
    JSON 文件保存管道
    将数据保存为 JSON 格式
    """

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler)

    def __init__(self, crawler):
        self.crawler = crawler
        self.output_dir = Path("output")
        self.output_dir.mkdir(exist_ok=True)
        self.items = []

    def open_spider(self):
        self.crawler.spider.logger.info(
            f"JsonSavePipeline opened for spider: {self.crawler.spider.name}"
        )

    def process_item(self, item):
        adapter = ItemAdapter(item)
        self.items.append(dict(adapter))
        return item

    def close_spider(self):
        import json

        output_file = self.output_dir / f"{self.crawler.spider.name}.json"
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(self.items, f, ensure_ascii=False, indent=2)

        self.crawler.spider.logger.info(
            f"Saved {len(self.items)} items to: {output_file}"
        )

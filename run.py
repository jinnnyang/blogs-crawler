#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
便捷运行脚本
用于快速运行博客爬虫
"""

import subprocess
import sys
from pathlib import Path


def run_spider(spider_name, url=None, args=None):
    """
    运行Scrapy爬虫

    Args:
        spider_name: 爬虫名称
        url: 起始URL
        args: 额外参数
    """
    cmd = ["scrapy", "crawl", spider_name]

    if url:
        cmd.extend(["-a", f"url={url}"])

    if args:
        cmd.extend(args)

    print(f"Running: {' '.join(cmd)}")
    subprocess.run(cmd)


def main():
    """主函数"""
    if len(sys.argv) < 2:
        print("Usage: python run.py <spider_name> [url] [args...]")
        print("\nAvailable commands:")
        print("  python run.py blog <url>           - Run generic blog spider")
        print("  python run.py readthedocs <url>    - Run ReadTheDocs spider")
        print("  python run.py mkdocs <url>        - Run MkDocs spider")
        print("  python run.py sphinx <url>        - Run Sphinx spider")
        print("  python run.py list                - List all spiders")
        print("  python run.py shell <url>         - Open Scrapy shell")
        sys.exit(1)

    command = sys.argv[1]

    if command == "list":
        # 列出所有爬虫
        subprocess.run(["scrapy", "list"])
    elif command == "shell":
        # Scrapy shell
        if len(sys.argv) < 3:
            print("Usage: python run.py shell <url>")
            sys.exit(1)
        url = sys.argv[2]
        subprocess.run(["scrapy", "shell", url])
    else:
        # 运行爬虫
        spider_name = command
        url = sys.argv[2] if len(sys.argv) > 2 else None
        args = sys.argv[3:] if len(sys.argv) > 3 else []
        run_spider(spider_name, url, args)


if __name__ == "__main__":
    main()

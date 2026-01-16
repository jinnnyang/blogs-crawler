#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
便捷运行脚本
用于快速运行 Scrapy 爬虫
"""

import subprocess
import sys
from pathlib import Path


def run_spider(spider_name, args=None):
    """
    运行 Scrapy 爬虫

    Args:
        spider_name: 爬虫名称
        args: 额外参数
    """
    cmd = ["scrapy", "crawl", spider_name]

    if args:
        cmd.extend(args)

    print(f"Running: {' '.join(cmd)}")
    subprocess.run(cmd)


def main():
    """主函数"""
    if len(sys.argv) < 2:
        print("Usage: python run.py <spider_name> [args...]")
        print("\nAvailable commands:")
        print("  python run.py example      - Run example spider")
        print("  python run.py list        - List all spiders")
        print("  python run.py shell <url>  - Open Scrapy shell")
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
    elif command == "check":
        # 检查爬虫
        if len(sys.argv) < 3:
            print("Usage: python run.py check <spider_name>")
            sys.exit(1)
        spider_name = sys.argv[2]
        subprocess.run(["scrapy", "check", spider_name])
    else:
        # 运行爬虫
        spider_name = command
        args = sys.argv[2:]
        run_spider(spider_name, args)


if __name__ == "__main__":
    main()

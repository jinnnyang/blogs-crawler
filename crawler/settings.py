# -*- coding: utf-8 -*-
# Scrapy settings for crawler project
#
# 博客爬虫配置文件
# 支持多种文档框架：ReadTheDocs, RBook, MkDocs, Sphinx, Teadocs, Docsify

import os
from pathlib import Path

# ============================================================
# 基础配置
# ============================================================

BOT_NAME = "crawler"

SPIDER_MODULES = ["crawler.spiders"]
NEWSPIDER_MODULE = "crawler.spiders"

ADDONS = {}

# 项目根目录
PROJECT_ROOT = Path(__file__).parent.parent
OUTPUT_DIR = PROJECT_ROOT / "output"
CACHE_DIR = PROJECT_ROOT / "cache"

# 确保目录存在
OUTPUT_DIR.mkdir(exist_ok=True)
CACHE_DIR.mkdir(exist_ok=True)

# ============================================================
# 用户代理和请求头
# ============================================================

USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"

DEFAULT_REQUEST_HEADERS = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
    "Accept-Encoding": "gzip,deflate,identity",  # 移除 br 编码，避免 Brotli 压缩解码问题
    "Connection": "keep-alive",
    "Upgrade-Insecure-Requests": "1",
}

# ============================================================
# Robots.txt 规则
# ============================================================

ROBOTSTXT_OBEY = False

# ============================================================
# 并发和延迟设置
# ============================================================

CONCURRENT_REQUESTS = 16
CONCURRENT_REQUESTS_PER_DOMAIN = 8
DOWNLOAD_DELAY = 1
RANDOMIZE_DOWNLOAD_DELAY = True

# ============================================================
# Cookie 和会话
# ============================================================

COOKIES_ENABLED = True
COOKIES_DEBUG = False

# ============================================================
# Telnet 控制台
# ============================================================

TELNETCONSOLE_ENABLED = False
TELNETCONSOLE_PORT = 6023

# ============================================================
# 日志配置
# ============================================================

LOG_LEVEL = "INFO"
LOG_FORMAT = "%(asctime)s [%(name)s] %(levelname)s: %(message)s"
LOG_DATEFORMAT = "%Y-%m-%d %H:%M:%S"
LOG_FILE = None

# ============================================================
# 重试设置
# ============================================================

RETRY_TIMES = 3
RETRY_DELAY = 3
RETRY_HTTP_CODES = [500, 502, 503, 504, 408, 429]

# ============================================================
# 超时设置
# ============================================================

DOWNLOAD_TIMEOUT = 180

# ============================================================
# 数据管道配置
# ============================================================

ITEM_PIPELINES = {
    "crawler.pipelines.MarkdownSavePipeline": 300,
}

# ============================================================
# 下载中间件配置
# ============================================================

DOWNLOADER_MIDDLEWARES = {
    "crawler.middlewares.CacheMiddleware": 400,
    "crawler.middlewares.RandomUserAgentMiddleware": 500,
}

# ============================================================
# 爬虫中间件配置
# ============================================================

SPIDER_MIDDLEWARES = {}

# ============================================================
# 扩展配置
# ============================================================

EXTENSIONS = {
    "scrapy.extensions.telnet.TelnetConsole": None,
}

# ============================================================
# AutoThrottle 自动限速
# ============================================================

AUTOTHROTTLE_ENABLED = True
AUTOTHROTTLE_START_DELAY = 1
AUTOTHROTTLE_MAX_DELAY = 60
AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
AUTOTHROTTLE_DEBUG = False

# ============================================================
# HTTP 缓存
# ============================================================

HTTPCACHE_ENABLED = False
HTTPCACHE_EXPIRATION_SECS = 0
HTTPCACHE_DIR = str(CACHE_DIR)
HTTPCACHE_IGNORE_HTTP_CODES = [500, 502, 503, 504, 400, 403, 404, 408]
HTTPCACHE_STORAGE = "scrapy.extensions.httpcache.FilesystemCacheStorage"
HTTPCACHE_IGNORE_MISSING = False
HTTPCACHE_IGNORE_SCHEMES = ["file"]

# ============================================================
# 自定义缓存中间件配置
# ============================================================

# 是否从 output/**/*.md 预加载缓存（默认 False，避免返回 markdown 内容导致框架检测失败）
CACHE_PRELOAD_FROM_OUTPUT = False

# ============================================================
# Feed Export 配置
# ============================================================

FEED_EXPORT_ENCODING = "utf-8"
FEED_FORMATS = {
    "json": "scrapy.exporters.JsonItemExporter",
    "jsonlines": "scrapy.exporters.JsonLinesItemExporter",
    "jl": "scrapy.exporters.JsonLinesItemExporter",
    "csv": "scrapy.exporters.CsvItemExporter",
    "xml": "scrapy.exporters.XmlItemExporter",
}

# ============================================================
# User-Agent 列表
# ============================================================

USER_AGENT_LIST = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2 Safari/605.1.15",
]

# ============================================================
# 统计信息收集
# ============================================================

STATS_CLASS = "scrapy.statscollectors.StatsCollector"
STATS_DUMP = True

# ============================================================
# 其他设置
# ============================================================

FEED_EXPORT_ENCODING = "utf-8"
DNS_TIMEOUT = 60
DNSCACHE_SIZE = 10000
COMPRESSION_ENABLED = True
DOWNLOAD_MAXSIZE = 1073741824  # 1GB
DOWNLOAD_WARNSIZE = 33554432  # 32MB
MEDIA_ALLOW_REDIRECTS = True

# -*- coding: utf-8 -*-
# Scrapy settings for crawler project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://docs.scrapy.org/en/latest/topics/settings.html
#     https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://docs.scrapy.org/en/latest/topics/spider-middleware.html

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

# 确保输出目录存在
OUTPUT_DIR.mkdir(exist_ok=True)

# ============================================================
# 用户代理和请求头
# ============================================================

# Crawl responsibly by identifying yourself (and your website) on the user-agent
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"

# Override the default request headers
DEFAULT_REQUEST_HEADERS = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
    "Accept-Encoding": "gzip, deflate, br",
    "Connection": "keep-alive",
    "Upgrade-Insecure-Requests": "1",
}

# ============================================================
# Robots.txt 规则
# ============================================================

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# ============================================================
# 并发和延迟设置
# ============================================================

# 并发请求数（全局）
CONCURRENT_REQUESTS = 16

# 每个域名的并发请求数
CONCURRENT_REQUESTS_PER_DOMAIN = 8
# CONCURRENT_REQUESTS_PER_IP 已在 Scrapy 2.14+ 中弃用，使用 CONCURRENT_REQUESTS_PER_DOMAIN 替代

# 下载延迟（秒）
DOWNLOAD_DELAY = 1

# 随机延迟因子
RANDOMIZE_DOWNLOAD_DELAY = True

# ============================================================
# Cookie 和会话
# ============================================================

# Disable cookies (enabled by default)
COOKIES_ENABLED = True

# Cookie 调试
COOKIES_DEBUG = False

# ============================================================
# Telnet 控制台
# ============================================================

# Disable Telnet Console (enabled by default)
TELNETCONSOLE_ENABLED = False

# Telnet 端口
TELNETCONSOLE_PORT = 6023

# ============================================================
# 日志配置
# ============================================================

# 日志级别
LOG_LEVEL = "INFO"

# 日志格式
LOG_FORMAT = "%(asctime)s [%(name)s] %(levelname)s: %(message)s"

# 日志日期格式
LOG_DATEFORMAT = "%Y-%m-%d %H:%M:%S"

# 日志文件
LOG_FILE = None

# ============================================================
# 重试设置
# ============================================================

# 重试次数
RETRY_TIMES = 3

# 重试延迟
RETRY_DELAY = 3

# 重试的 HTTP 状态码
RETRY_HTTP_CODES = [500, 502, 503, 504, 408, 429]

# ============================================================
# 超时设置
# ============================================================

# 下载超时（秒）
DOWNLOAD_TIMEOUT = 180

# ============================================================
# 数据管道配置
# ============================================================

# Configure item pipelines
# See https://docs.scrapy.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
    "crawler.pipelines.DataCleaningPipeline": 100,
    "crawler.pipelines.ValidationPipeline": 200,
    "crawler.pipelines.FileSavePipeline": 400,
}

# ============================================================
# 下载中间件配置
# ============================================================

# Enable or disable downloader middlewares
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
DOWNLOADER_MIDDLEWARES = {
    "crawler.middlewares.RandomUserAgentMiddleware": 400,
    "crawler.middlewares.ProxyMiddleware": 410,
    "crawler.middlewares.CrawlerDownloaderMiddleware": 543,
}

# ============================================================
# 爬虫中间件配置
# ============================================================

# Enable or disable spider middlewares
# See https://docs.scrapy.org/en/latest/topics/spider-middleware.html
SPIDER_MIDDLEWARES = {
    "crawler.middlewares.CrawlerSpiderMiddleware": 543,
}

# ============================================================
# 扩展配置
# ============================================================

# Enable or disable extensions
# See https://docs.scrapy.org/en/latest/topics/extensions.html
EXTENSIONS = {
    "scrapy.extensions.telnet.TelnetConsole": None,
}

# ============================================================
# AutoThrottle 自动限速
# ============================================================

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/autothrottle.html
AUTOTHROTTLE_ENABLED = True

# The initial download delay
AUTOTHROTTLE_START_DELAY = 1

# The maximum download delay to be set in case of high latencies
AUTOTHROTTLE_MAX_DELAY = 60

# The average number of requests Scrapy should be sending in parallel to
# each remote server
AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0

# Enable showing throttling stats for every response received:
AUTOTHROTTLE_DEBUG = False

# ============================================================
# HTTP 缓存
# ============================================================

# Enable and configure HTTP caching (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
HTTPCACHE_ENABLED = False
HTTPCACHE_EXPIRATION_SECS = 0
HTTPCACHE_DIR = ".scrapy/httpcache"
HTTPCACHE_IGNORE_HTTP_CODES = [500, 502, 503, 504, 400, 403, 404, 408]
HTTPCACHE_STORAGE = "scrapy.extensions.httpcache.FilesystemCacheStorage"
HTTPCACHE_IGNORE_MISSING = False
HTTPCACHE_IGNORE_SCHEMES = ["file"]

# ============================================================
# Feed Export 配置
# ============================================================

# Feed 输出编码
FEED_EXPORT_ENCODING = "utf-8"

# Feed 输出格式
FEED_FORMATS = {
    "json": "scrapy.exporters.JsonItemExporter",
    "jsonlines": "scrapy.exporters.JsonLinesItemExporter",
    "jl": "scrapy.exporters.JsonLinesItemExporter",
    "csv": "scrapy.exporters.CsvItemExporter",
    "xml": "scrapy.exporters.XmlItemExporter",
    "marshal": "scrapy.exporters.MarshalItemExporter",
    "pickle": "scrapy.exporters.PickleItemExporter",
}

# ============================================================
# 代理配置
# ============================================================

# 代理列表（每个代理一行）
# PROXY_LIST = [
#     "http://proxy1.example.com:8080",
#     "http://proxy2.example.com:8080",
# ]

# 代理模式
# "random" - 随机选择
# "round_robin" - 轮询
# PROXY_MODE = "random"

# ============================================================
# User-Agent 列表
# ============================================================

# User-Agent 列表（用于随机选择）
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

# 统计信息收集器
STATS_CLASS = "scrapy.statscollectors.StatsCollector"

# 统计信息转储
STATS_DUMP = True

# ============================================================
# 其他设置
# ============================================================

# Set settings whose default value is deprecated to a future-proof value
FEED_EXPORT_ENCODING = "utf-8"

# DNS 解析超时
DNS_TIMEOUT = 60

# DNS 缓存大小
DNSCACHE_SIZE = 10000

# 最大域名数
CONCURRENT_REQUESTS_PER_DOMAIN_LIMIT = 0

# 最大 IP 数
CONCURRENT_REQUESTS_PER_IP_LIMIT = 0

# 压缩响应
COMPRESSION_ENABLED = True

# 响应大小限制（字节）
DOWNLOAD_MAXSIZE = 1073741824  # 1GB

# 响应警告大小（字节）
DOWNLOAD_WARNSIZE = 33554432  # 32MB

# 媒体类型限制
MEDIA_ALLOW_REDIRECTS = True

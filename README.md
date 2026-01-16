# 博客爬虫

一个基于Scrapy的博客文档爬虫，支持多种文档框架，自动将HTML转换为Markdown格式并保存。

## 特性

- 🚀 支持多种文档框架：ReadTheDocs、RBook、MkDocs、Sphinx、Teadocs、Docsify
- 📦 自动检测文档框架类型
- 🔄 递归爬取文档站点
- 💾 缓存机制，避免重复请求
- 📝 输出为Markdown格式，包含YAML metadata
- 🗂️ 保持URL结构输出文件

## 快速开始

### 安装依赖

```bash
pip install -r requirements.txt
```

### 运行爬虫

```bash
# 使用通用爬虫（自动检测框架）
scrapy crawl blog -a url=https://example.com

# 使用特定框架爬虫
scrapy crawl readthedocs -a url=https://docs.readthedocs.io
scrapy crawl mkdocs -a url=https://mkdocs.org
```

### 输出格式

爬取的文档会保存为Markdown文件，包含YAML metadata：

```markdown
---
title: 页面标题
url: https://example.com/path/to/page.html
tags:
  - tag1
  - tag2
framework: readthedocs
crawl_time: 2024-01-16 16:00:00
---

# 页面内容

这里是转换后的Markdown正文内容...
```

### 文件路径规则

输出文件保持URL结构：

| 输入URL | 输出路径 |
|---------|----------|
| `https://example.com/` | `output/example.com/index.md` |
| `https://example.com/path/to/page.html` | `output/example.com/path/to/page.md` |
| `https://docs.python.org/3/library/` | `output/docs.python.org/3/library/index.md` |

## 项目结构

```
blogs-crawler/
├── crawler/
│   ├── __init__.py
│   ├── settings.py              # 配置文件
│   ├── items.py                # 数据模型 (BlogItem)
│   ├── middlewares.py          # 中间件（包含缓存中间件）
│   ├── pipelines.py            # 数据管道（Markdown保存管道）
│   ├── framework_detector.py    # 框架检测模块
│   ├── converters/             # HTML到Markdown转换器
│   │   ├── __init__.py
│   │   ├── base.py           # 基类
│   │   ├── readthedocs.py    # ReadTheDocs转换器
│   │   ├── rbook.py         # RBook转换器
│   │   ├── mkdocs.py        # MkDocs转换器
│   │   ├── sphinx.py        # Sphinx转换器
│   │   ├── teadocs.py       # Teadocs转换器
│   │   └── docsify.py       # Docsify转换器
│   └── spiders/             # 爬虫目录
│       ├── __init__.py
│       ├── base.py          # 博客爬虫基类
│       ├── readthedocs.py   # ReadTheDocs爬虫
│       ├── rbook.py         # RBook爬虫
│       ├── mkdocs.py        # MkDocs爬虫
│       ├── sphinx.py        # Sphinx爬虫
│       ├── teadocs.py       # Teadocs爬虫
│       └── docsify.py       # Docsify爬虫
├── output/                  # Markdown输出目录
├── cache/                   # HTTP缓存目录
├── scrapy.cfg
├── requirements.txt
└── README.md
```

## 核心功能

### 1. 框架检测

[`FrameworkDetector`](crawler/framework_detector.py) 自动检测文档框架类型：

- 通过URL域名检测
- 通过HTML特征检测
- 通过meta标签检测

### 2. 转换器架构

各框架专用转换器继承 [`BaseConverter`](crawler/converters/base.py)，提供优化的HTML到Markdown转换：

- [`ReadTheDocsConverter`](crawler/converters/readthedocs.py) - 针对ReadTheDocs优化
- [`RBookConverter`](crawler/converters/rbook.py) - 针对RBook优化
- [`MkDocsConverter`](crawler/converters/mkdocs.py) - 针对MkDocs优化
- [`SphinxConverter`](crawler/converters/sphinx.py) - 针对Sphinx优化
- [`TeadocsConverter`](crawler/converters/teadocs.py) - 针对Teadocs优化
- [`DocsifyConverter`](crawler/converters/docsify.py) - 针对Docsify优化

### 3. 缓存机制

[`CacheMiddleware`](crawler/middlewares.py) 提供缓存功能：

- 爬虫开始前自动从 `output/**/*.md` 预加载URL到缓存
- URL命中缓存则直接返回，避免重复请求
- 支持HTTP响应缓存

### 4. Markdown保存

[`MarkdownSavePipeline`](crawler/pipelines.py) 将数据保存为Markdown文件：

- 根据URL生成输出路径
- 构建YAML metadata
- 写入Markdown文件

## 配置说明

### 基础配置 ([`crawler/settings.py`](crawler/settings.py))

主要配置项：

- `OUTPUT_DIR` - 输出目录（默认：`output`）
- `CACHE_DIR` - 缓存目录（默认：`cache`）
- `DOWNLOAD_DELAY` - 下载延迟（秒）
- `CONCURRENT_REQUESTS` - 并发请求数
- `ITEM_PIPELINES` - 启用的数据管道
- `DOWNLOADER_MIDDLEWARES` - 启用的下载中间件

## 技术栈

- **Scrapy** - 爬虫框架
- **Markdownify** - HTML到Markdown转换
- **BeautifulSoup4** - HTML解析
- **lxml** - XML/HTML解析
- **PyYAML** - YAML解析

## 许可证

MIT License

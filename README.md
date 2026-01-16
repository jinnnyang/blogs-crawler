# Scrapy 爬虫开发模板

[![Open in Dev Containers](https://img.shields.io/static/v1?label=Dev%20Containers&message=Open&color=blue&logo=visualstudiocode)](https://vscode.dev/redirect?url=vscode://ms-vscode-remote.remote-containers/cloneInVolume?url=https://github.com/microsoft/vscode-remote-try-python)

一个功能完善的 Scrapy 爬虫开发模板，支持 Dev Containers 和 GitHub Codespaces 开发环境。

## 特性

- 🚀 开箱即用的 Scrapy 爬虫框架
- 🐳 支持 Docker Dev Containers 开发环境
- 💻 完善的 VS Code 调试配置
- 📦 预置常用爬虫中间件和管道
- 📝 丰富的示例爬虫代码
- 📚 详细的开发文档

## 快速开始

### 使用 GitHub Codespaces

1. 点击仓库的 **Code** 下拉菜单
2. 点击 **Codespaces** 标签
3. 点击 **Create codespace on main**

### 使用 VS Code Dev Containers

如果你已经安装了 VS Code 和 Docker：

1. 克隆仓库到本地
2. 在 VS Code 中打开仓库
3. 按 `F1` 并选择 **Dev Containers: Reopen in Container**
4. 等待容器构建完成

### 本地开发

确保已安装 Python 3.8+：

```bash
# 安装依赖
pip install -r requirements.txt

# 运行示例爬虫
scrapy crawl example

# 或使用便捷脚本
python run.py example
```

## 项目结构

```
.
├── crawler/                    # 爬虫核心目录
│   ├── __init__.py
│   ├── settings.py           # Scrapy 配置文件
│   ├── items.py             # 数据模型定义
│   ├── pipelines.py         # 数据处理管道
│   ├── middlewares.py       # 中间件
│   ├── utils.py             # 工具函数
│   ├── exporters.py         # 自定义导出器
│   └── spiders/             # 爬虫目录
│       ├── __init__.py
│       ├── example.py       # 基础示例爬虫
│       ├── async_spider.py  # 异步爬虫示例
│       └── selenium_spider.py # Selenium 爬虫示例
├── output/                   # 数据输出目录
│   └── .gitkeep
├── docs/                     # 文档目录
│   ├── GETTING_STARTED.md   # 快速开始指南
│   ├── BEST_PRACTICES.md    # 最佳实践
│   └── API_REFERENCE.md     # API 参考
├── .devcontainer/            # Dev Container 配置
├── .vscode/                  # VS Code 配置
├── scrapy.cfg               # Scrapy 项目配置
├── run.py                   # 便捷运行脚本
├── requirements.txt         # Python 依赖
└── README.md               # 项目说明
```

## 使用示例

### 运行爬虫

```bash
# 使用 Scrapy 命令
scrapy crawl example

# 使用便捷脚本
python run.py example

# 调试模式运行
scrapy crawl example -s LOG_LEVEL=DEBUG

# 保存数据到文件
scrapy crawl example -o output/example.json
```

### 创建新爬虫

```bash
# 使用 Scrapy 命令生成爬虫模板
scrapy genspider myspider example.com

# 或手动创建文件
# 在 crawler/spiders/ 目录下创建新的爬虫文件
```

### 调试爬虫

在 VS Code 中：

1. 打开 `crawler/spiders/example.py`
2. 在代码行号左侧点击设置断点
3. 按 `F5` 或选择 "Scrapy" 调试配置
4. 等待断点命中，开始调试

### 使用 Scrapy Shell

```bash
# 交互式调试
scrapy shell "https://example.com"

# 使用 VS Code 调试配置
# 选择 "Scrapy Shell" 配置启动
```

## 配置说明

### 基础配置 ([`crawler/settings.py`](crawler/settings.py))

主要配置项：

- `BOT_NAME` - 爬虫名称
- `SPIDER_MODULES` - 爬虫模块路径
- `USER_AGENT` - 用户代理
- `ROBOTSTXT_OBEY` - 是否遵守 robots.txt
- `CONCURRENT_REQUESTS` - 并发请求数
- `DOWNLOAD_DELAY` - 下载延迟
- `ITEM_PIPELINES` - 启用的数据管道
- `DOWNLOADER_MIDDLEWARES` - 启用的下载中间件

### 中间件 ([`crawler/middlewares.py`](crawler/middlewares.py))

内置中间件：

- `RandomUserAgentMiddleware` - 随机 User-Agent
- `ProxyMiddleware` - 代理支持
- `RetryMiddleware` - 请求重试

### 数据管道 ([`crawler/pipelines.py`](crawler/pipelines.py))

内置管道：

- `DataCleaningPipeline` - 数据清洗
- `FileSavePipeline` - 文件保存
- `DeduplicationPipeline` - 数据去重
- `ValidationPipeline` - 数据验证

## 示例爬虫

### 基础爬虫 ([`example.py`](crawler/spiders/example.py))

爬取 https://example.com 的基础示例：

```python
import scrapy
from crawler.items import CrawlerItem


class ExampleSpider(scrapy.Spider):
    name = "example"
    allowed_domains = ["example.com"]
    start_urls = ["https://example.com"]

    def parse(self, response):
        item = ClawerItem()
        item['url'] = response.url
        item['title'] = response.css('h1::text').get()
        item['content'] = response.css('p::text').getall()
        yield item
```

### 异步爬虫 ([`async_spider.py`](crawler/spiders/async_spider.py))

使用 aiohttp 的异步爬虫示例。

### Selenium 爬虫 ([`selenium_spider.py`](crawler/spiders/selenium_spider.py))

使用 Selenium 处理 JavaScript 渲染页面的示例。

## 常见问题

### Q: 如何修改爬虫的并发数？

A: 在 [`crawler/settings.py`](crawler/settings.py) 中修改 `CONCURRENT_REQUESTS` 配置项。

### Q: 如何添加代理？

A: 在 [`crawler/settings.py`](crawler/settings.py) 中启用 `ProxyMiddleware` 并配置代理列表。

### Q: 数据保存到数据库？

A: 在 [`crawler/pipelines.py`](crawler/pipelines.py) 中添加数据库管道，或在 `ITEM_PIPELINES` 中配置。

### Q: 如何处理登录认证？

A: 在爬虫的 `start_requests` 方法中添加登录逻辑，或使用 `FormRequest` 发送登录请求。

## 开发指南

详细的开发指南请参考：

- [快速开始指南](docs/GETTING_STARTED.md)
- [最佳实践](docs/BEST_PRACTICES.md)
- [API 参考](docs/API_REFERENCE.md)

## 技术栈

- **Scrapy** - 爬虫框架
- **BeautifulSoup4** - HTML 解析
- **Requests** - HTTP 请求
- **lxml** - XML/HTML 解析
- **Selenium** - 浏览器自动化
- **aiohttp** - 异步 HTTP 客户端

## 贡献

欢迎提交 Issue 和 Pull Request！

## 许可证

MIT License - 详见 [LICENSE](LICENSE) 文件

## 链接

- [Scrapy 官方文档](https://docs.scrapy.org/)
- [Scrapy GitHub](https://github.com/scrapy/scrapy)
- [VS Code Dev Containers](https://code.visualstudio.com/docs/devcontainers/containers)

# 快速开始指南

## 安装依赖

```bash
pip install -r requirements.txt
```

## 运行示例爬虫

### 使用 Scrapy 命令

```bash
scrapy crawl example
```

### 使用便捷脚本

```bash
python run.py example
```

### 使用 VS Code 调试

1. 打开 `crawler/spiders/example.py`
2. 设置断点
3. 按 `F5` 启动调试

## 创建新爬虫

### 使用 Scrapy 命令生成

```bash
scrapy genspider myspider example.com
```

### 手动创建

在 `crawler/spiders/` 目录下创建新的 Python 文件：

```python
import scrapy
from crawler.items import CrawlerItem


class MySpider(scrapy.Spider):
    name = "myspider"
    allowed_domains = ["example.com"]
    start_urls = ["https://example.com"]
    
    def parse(self, response):
        item = CrawlerItem()
        item['url'] = response.url
        item['title'] = response.css('h1::text').get()
        item['content'] = response.css('p::text').getall()
        yield item
```

## 常用命令

```bash
# 列出所有爬虫
scrapy list

# 检查爬虫
scrapy check example

# Scrapy Shell（交互式调试）
scrapy shell "https://example.com"

# 运行爬虫并保存到文件
scrapy crawl example -o output/example.json

# 调试模式运行
scrapy crawl example -s LOG_LEVEL=DEBUG
```

## 输出文件

爬取的数据会自动保存到 `output/` 目录：

- `output/example.txt` - 文本格式
- `output/example.json` - JSON 格式（使用 `-o` 参数）

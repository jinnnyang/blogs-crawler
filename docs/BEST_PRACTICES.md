# 最佳实践

## 爬虫开发建议

### 1. 遵守 robots.txt

尊重网站的爬取规则，在 `settings.py` 中设置：

```python
ROBOTSTXT_OBEY = True
```

### 2. 设置合理的延迟

避免对目标网站造成过大压力：

```python
DOWNLOAD_DELAY = 1  # 每次请求间隔 1 秒
CONCURRENT_REQUESTS = 16  # 控制并发数
```

### 3. 使用 User-Agent

设置真实的 User-Agent，避免被识别为爬虫：

```python
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
```

### 4. 错误处理

在爬虫中添加错误处理：

```python
def parse(self, response):
    try:
        # 解析逻辑
        pass
    except Exception as e:
        self.logger.error(f"Error parsing {response.url}: {e}")
```

### 5. 数据验证

使用 ValidationPipeline 验证数据：

```python
ITEM_PIPELINES = {
    "crawler.pipelines.ValidationPipeline": 200,
}
```

## 性能优化

### 1. 启用 HTTP 缓存

```python
HTTPCACHE_ENABLED = True
HTTPCACHE_EXPIRATION_SECS = 3600  # 缓存 1 小时
```

### 2. 使用 AutoThrottle

```python
AUTOTHROTTLE_ENABLED = True
AUTOTHROTTLE_START_DELAY = 1
AUTOTHROTTLE_MAX_DELAY = 60
```

### 3. 禁用不需要的扩展

```python
TELNETCONSOLE_ENABLED = False  # 不需要时禁用
```

## 调试技巧

### 1. 使用 Scrapy Shell

```bash
scrapy shell "https://example.com"
```

在 Shell 中测试选择器：

```python
response.css('h1::text').get()
response.xpath('//h1/text()').get()
```

### 2. 查看日志

```bash
scrapy crawl example -s LOG_LEVEL=DEBUG
```

### 3. 使用 VS Code 调试

设置断点后按 `F5` 启动调试。

## 部署建议

### 1. 使用 Scrapyd

部署到 Scrapyd 进行分布式爬取。

### 2. 使用定时任务

使用 cron 或 Celery 定时运行爬虫。

### 3. 监控和告警

监控爬虫运行状态，设置错误告警。

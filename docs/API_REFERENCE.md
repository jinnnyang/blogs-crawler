# API 参考

## Item 类

### CrawlerItem

基础爬虫数据模型。

**字段：**

| 字段 | 类型 | 说明 |
|------|------|------|
| url | str | 页面 URL |
| title | str | 页面标题 |
| content | str | 页面内容 |
| crawl_time | str | 爬取时间 |

## Pipeline 类

### DataCleaningPipeline

数据清洗管道，去除空白字符、清理空值。

**优先级：** 100

### ValidationPipeline

数据验证管道，验证必填字段。

**优先级：** 200

### FileSavePipeline

文件保存管道，将数据保存到 `output/` 目录。

**优先级：** 400

**输出格式：** txt

### JsonSavePipeline

JSON 文件保存管道。

**优先级：** 未启用（需手动配置）

## Middleware 类

### RandomUserAgentMiddleware

随机 User-Agent 中间件。

**优先级：** 400

### ProxyMiddleware

代理中间件。

**优先级：** 410

**配置：**

```python
PROXY_LIST = [
    "http://proxy1.example.com:8080",
    "http://proxy2.example.com:8080",
]
```

## 工具函数

### format_timestamp(timestamp=None)

格式化时间戳。

**参数：**
- `timestamp` - 时间戳对象（可选），默认为当前时间

**返回：** 格式化的时间字符串

### clean_text(text)

清理文本内容。

**参数：**
- `text` - 原始文本

**返回：** 清理后的文本

## Settings 配置

### 基础配置

| 配置项 | 默认值 | 说明 |
|--------|--------|------|
| BOT_NAME | "crawler" | 爬虫名称 |
| USER_AGENT | - | 用户代理 |
| ROBOTSTXT_OBEY | False | 是否遵守 robots.txt |

### 并发配置

| 配置项 | 默认值 | 说明 |
|--------|--------|------|
| CONCURRENT_REQUESTS | 16 | 并发请求数 |
| DOWNLOAD_DELAY | 1 | 下载延迟（秒） |

### Pipeline 配置

```python
ITEM_PIPELINES = {
    "crawler.pipelines.DataCleaningPipeline": 100,
    "crawler.pipelines.ValidationPipeline": 200,
    "crawler.pipelines.FileSavePipeline": 400,
}
```

### Middleware 配置

```python
DOWNLOADER_MIDDLEWARES = {
    "crawler.middlewares.RandomUserAgentMiddleware": 400,
    "crawler.middlewares.ProxyMiddleware": 410,
}
```

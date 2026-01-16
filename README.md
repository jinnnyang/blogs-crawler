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

## 优化待办事项

### 🎯 核心优化目标

当前项目存在架构冗余问题，需要进行一次大规模的重构优化，以提高代码可维护性和扩展性。

### 📋 详细优化清单

#### 1. Converter 架构重构

**问题描述：**
- 虽然设计了多个 Converter（ReadTheDocsConverter、MkDocsConverter、SphinxConverter 等），但实际上几乎只有 BaseConverter 起作用
- 各子类 Converter 仅修改了 `strip_tags` 列表和重写了 `extract_title`、`extract_tags`、`extract_content` 方法
- 这些方法本质上只是 CSS 选择器的差异，并没有真正利用 `markdownify.MarkdownConverter` 的 `convert_*` 方法

**优化方案：**
- [ ] 移除自定义的 `BaseConverter`，改用 `markdownify.MarkdownConverter` 作为基类
- [ ] 通过重写 `convert_*` 方法（如 `convert_a`、`convert_img`、`convert_div` 等）来适配不同框架的 HTML 结构
- [ ] 将 CSS 选择器配置化，减少 Converter 的数量
- [ ] 创建统一的配置文件管理各框架的选择器规则（如 `framework_config.yaml`）

**预期效果：**
- 减少代码重复
- 更好地利用 markdownify 的功能
- 提高代码可维护性

#### 2. Spider 架构简化

**问题描述：**
- spiders 目录下有 6 个框架专用的 Spider 类（readthedocs.py、mkdocs.py、sphinx.py 等）
- 各 Spider 的主要差异仅在于 `LinkExtractor` 的 `allow` 和 `deny` 规则
- 实际的解析逻辑都在 `BlogSpider` 基类中，造成大量代码重复

**优化方案：**
- [ ] 合并所有 Spider 为一个通用的 `BlogSpider`
- [ ] 将 LinkExtractor 的 allow/deny 规则配置化，存储在 `FrameworkDetector` 或独立配置文件中
- [ ] 在 `FrameworkDetector` 中增加返回框架规则配置的方法
- [ ] 删除冗余的 Spider 文件（readthedocs.py、mkdocs.py、sphinx.py、docsify.py、rbook.py、teadocs.py）

**预期效果：**
- 减少代码重复
- 简化项目结构
- 更易于添加新框架支持

#### 3. 相对路径转换优化

**问题描述：**
- 相对路径转换操作在 Converter 的 `convert` 方法中进行
- 这是一个框架无关的操作，应该在更早的阶段完成

**优化方案：**
- [ ] 将相对路径转换逻辑移至 Spider 的 `parse` 阶段
- [ ] 使用 BeautifulSoup 统一处理 URL 转换（img src、a href、link href、script src 等）
- [ ] 在转换前完成所有 URL 的绝对路径化
- [ ] 确保转换后的 HTML 已经是绝对路径形式

**预期效果：**
- 职责分离更清晰
- 避免在 Converter 中处理 URL
- 提高代码可测试性

#### 4. FrameworkDetector 增强

**问题描述：**
- 当前框架检测功能较为基础
- 没有缓存机制，每次都需要重新检测
- 规则硬编码在代码中，不易扩展

**优化方案：**
- [ ] 增强框架检测的准确性，添加更多特征匹配规则
- [ ] 添加框架检测结果缓存，避免重复检测同一域名的页面
- [ ] 支持自定义规则配置，从配置文件读取框架特征
- [ ] 添加框架规则优先级机制，提高检测准确度
- [ ] 支持多框架混合页面的检测

**预期效果：**
- 提高检测准确性
- 减少重复计算
- 更易于扩展新框架

#### 5. 配置管理优化

**问题描述：**
- 框架相关的配置分散在多个文件中
- CSS 选择器、LinkExtractor 规则等硬编码在代码中
- 不易于维护和扩展

**优化方案：**
- [ ] 创建统一的配置文件 `framework_config.yaml` 管理所有框架相关配置
- [ ] 配置文件包含：框架特征、CSS 选择器、LinkExtractor 规则、strip_tags 列表等
- [ ] 创建配置加载器 `FrameworkConfigLoader` 类
- [ ] 支持配置文件热重载（开发环境）

**配置文件结构示例：**
```yaml
frameworks:
  readthedocs:
    patterns:
      url: ["readthedocs.io", "readthedocs.org"]
      html: ["ethical-ad-client", "rtd-container", "wy-nav-top"]
      meta: []
    selectors:
      title: [".wy-nav-content h1", ".document h1"]
      content: [".wy-nav-content .document", ".wy-nav-content .rst-content"]
      tags: [".wy-breadcrumbs li a"]
    strip_tags: ["div.ethical-ad", "div.rtd-container", "div.wy-nav-top"]
    link_extractor:
      allow: [".*/en/stable/.*", ".*/en/latest/.*", r".*/.*\.html"]
      deny: [".*/_static/.*", ".*/_downloads/.*", r".*/search\.html"]
```

**预期效果：**
- 配置集中管理
- 易于维护和扩展
- 支持快速添加新框架

#### 6. 代码结构优化

**问题描述：**
- 公共逻辑分散在多个文件中
- 缺少工具类封装
- 代码复用率低

**优化方案：**
- [ ] 提取 URL 转换逻辑到 `UrlNormalizer` 工具类
- [ ] 提取 HTML 清理逻辑到 `HtmlCleaner` 工具类
- [ ] 提取 CSS 选择器查询逻辑到 `SelectorHelper` 工具类
- [ ] 改进错误处理和日志记录
- [ ] 统一代码风格和命名规范

**预期效果：**
- 提高代码复用率
- 更清晰的职责划分
- 更易于测试和维护

#### 7. 错误处理和日志优化

**问题描述：**
- 错误处理不够完善
- 日志记录不够详细
- 缺少异常捕获和恢复机制

**优化方案：**
- [ ] 改进异常处理，添加更详细的错误信息
- [ ] 增加关键操作的日志记录
- [ ] 添加性能监控日志（如转换耗时、请求耗时）
- [ ] 实现失败重试机制
- [ ] 添加爬取统计信息（成功/失败页面数、框架分布等）

**预期效果：**
- 更好的问题诊断能力
- 更完善的错误恢复
- 更清晰的运行状态

#### 8. 测试覆盖

**问题描述：**
- 缺少单元测试
- 缺少集成测试
- 代码质量难以保证

**优化方案：**
- [ ] 为 Converter 添加单元测试
- [ ] 为 FrameworkDetector 添加单元测试
- [ ] 为 Spider 添加集成测试
- [ ] 添加端到端测试
- [ ] 配置 CI/CD 自动化测试

**预期效果：**
- 提高代码质量
- 减少回归问题
- 更安全的重构

#### 9. 性能优化

**问题描述：**
- 存在重复的 BeautifulSoup 解析
- 缓存机制可以进一步优化
- 并发处理可以改进

**优化方案：**
- [ ] 优化 BeautifulSoup 解析，避免重复解析
- [ ] 改进缓存策略，支持更细粒度的缓存控制
- [ ] 优化并发请求配置
- [ ] 添加请求去重机制
- [ ] 优化内存使用

**预期效果：**
- 提高爬取效率
- 减少资源消耗
- 更好的并发性能

#### 10. 文档完善

**问题描述：**
- 代码注释不够详细
- 缺少架构设计文档
- 缺少使用示例

**优化方案：**
- [ ] 完善代码注释和文档字符串
- [ ] 添加架构设计文档（ARCHITECTURE.md）
- [ ] 添加开发指南（CONTRIBUTING.md）
- [ ] 添加更多使用示例
- [ ] 添加常见问题解答（FAQ.md）

**预期效果：**
- 更易于理解项目
- 更易于参与开发
- 更好的用户体验

### 🚀 实施计划

#### 阶段一：核心重构（高优先级）
1. Converter 架构重构
2. Spider 架构简化
3. 相对路径转换优化

#### 阶段二：配置和工具（中优先级）
4. FrameworkDetector 增强
5. 配置管理优化
6. 代码结构优化

#### 阶段三：质量提升（中优先级）
7. 错误处理和日志优化
8. 测试覆盖

#### 阶段四：性能和文档（低优先级）
9. 性能优化
10. 文档完善

### 📊 优化效果预期

- **代码行数减少**：预计减少 30-40% 的重复代码
- **文件数量减少**：预计减少 6 个 Spider 文件
- **维护成本降低**：配置化后添加新框架只需修改配置文件
- **代码质量提升**：通过测试覆盖保证代码质量
- **性能提升**：通过缓存和并发优化提高爬取效率

## 许可证

MIT License

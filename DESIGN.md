# arXiv MCP Server 设计方案

## 概述

一个 MCP Server，让 LLM 客户端（如 Claude Code）能够直接搜索、下载和阅读 arXiv 论文。

## 技术栈

- **语言**: Python 3.10+
- **MCP SDK**: `mcp` (官方 Python SDK)
- **arXiv API**: `arxiv` 库
- **PDF 解析**: `pymupdf` (速度快，效果好)

## 核心 Tools

### 1. `search_papers`
按标题/关键词/arXiv ID 搜索论文

**参数:**
- `query`: 搜索关键词或 arXiv ID
- `max_results`: 返回数量（默认 10）

**返回:** 论文列表（ID、标题、作者、摘要、发布日期）

### 2. `get_paper`
获取论文全文

**参数:**
- `paper_id`: arXiv ID (如 "2401.12345")
- `section`: 可选，指定章节 (abstract/introduction/method/all)

**返回:** 论文全文或指定章节

### 3. `list_papers`
列出本地已下载的论文

**返回:** 本地论文列表

## 目录结构

```
arxiv-mcp/
├── pyproject.toml
├── README.md
├── DESIGN.md
├── src/
│   └── arxiv_mcp_server/
│       ├── __init__.py
│       ├── server.py      # MCP Server 主入口
│       ├── arxiv_client.py # arXiv API 封装
│       ├── pdf_parser.py   # PDF 文本提取
│       └── storage.py      # 本地存储管理
└── papers/                 # 下载的论文存储目录
```

## 工作流程

```
用户: "帮我看一下 PIS: Linking Importance Sampling... 这篇论文"

Claude Code:
  1. search_papers("PIS Importance Sampling Prompt Compression")
  2. 返回匹配论文列表，找到 arXiv ID
  3. get_paper("2401.xxxxx")
  4. 返回全文，Claude 开始分析
```

## 本地缓存策略

- 下载的 PDF 保存在 `papers/` 目录
- 提取的文本缓存为 `.txt` 文件
- 避免重复下载和解析

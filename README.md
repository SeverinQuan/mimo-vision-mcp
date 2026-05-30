# mimo-vision-mcp 👁️🧠

> Let text-only LLMs see images through MiMo Vision.  
> 让纯文本大模型通过 MiMo Vision 获得图像理解能力。

<p align="center">
  <b>MiMo Vision MCP Bridge for Text-only LLM Agents</b>
</p>

<p align="center">
  <code>MCP</code> · <code>MiMo Vision</code> · <code>Image Analysis</code> · <code>OCR</code> · <code>Text-only LLM</code> · <code>Agent Tool</code> · <code>Python</code>
</p>

---

## 🌐 Language

- [English](#english)
- [中文](#中文)

---

# English

## 📌 Overview

`mimo-vision-mcp` is a lightweight **MCP server** that gives **image understanding capability** to text-only LLMs (like DeepSeek, Qwen, or text-mode agents).

When the main model receives an image-related task, it can call the `mimo_image_analyze` MCP tool, send the image to MiMo Vision, and receive a clean text description.

In short:

```txt
Text-only LLM + MiMo Vision MCP = Visual Agent
```

---

## 🧠 How It Works

```
┌────────────────────┐
│   User Message      │
│  Image / Screenshot │
└─────────┬──────────┘
          │
          ▼
┌────────────────────┐
│ Text-only LLM       │
│ DeepSeek / Qwen /   │
│ custom agent        │
└─────────┬──────────┘
          │  needs visual understanding
          ▼
┌────────────────────────────┐
│ mimo_image_analyze Tool     │
│ MCP Vision Bridge           │
└─────────┬──────────────────┘
          │  image path / URL + base64
          ▼
┌────────────────────────────┐
│ MiMo Vision API             │
│ v2.5 multimodal model       │
└─────────┬──────────────────┘
          │  text description / analysis
          ▼
┌────────────────────┐
│ Text-only LLM       │
│ reasons with text   │
└─────────┬──────────┘
          │
          ▼
┌────────────────────┐
│ Final Reply         │
└────────────────────┘
```

---

## ✨ Features

- 👁️ Add vision ability to text-only LLMs via MCP
- 🔌 Standard MCP tool server (stdio transport)
- 🖼️ Supports local image paths and remote URLs
- 📝 Returns clean text descriptions for downstream reasoning
- 🌏 Domestic direct network connection (no proxy needed for MiMo API)
- ⚡ Lightweight — single Python file
- 🧠 Main model handles reasoning; MiMo handles visual perception

---

## 🚀 Quick Start

### 1. Clone

```bash
git clone https://github.com/SeverinQuan/mimo-vision-mcp.git
cd mimo-vision-mcp
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Set your API key

```bash
cp .env.example .env
# Edit .env — replace with your real MiMo API key
```

### 4. Configure your MCP client

Add to your MCP client configuration (Claude Desktop / Cline / Cursor / OpenClaw / OpenCode):

```json
{
  "mcpServers": {
    "mimo-vision": {
      "command": "python",
      "args": ["/path/to/mimo-vision-mcp/server.py"],
      "env": {
        "MIMO_API_KEY": "your_mimo_api_key_here"
      }
    }
  }
}
```

### 5. Restart your client

The `mimo_image_analyze` tool should now be available.

---

## 📦 One-click Bundle Install

This repository also includes an MCPB/DXT-friendly bundle manifest.

The MiMo API key is **not** stored in code or in the bundle. It is declared in
`manifest.json` as a sensitive `user_config` field and injected at runtime as
`MIMO_API_KEY`.

Build the bundle with the current official MCPB CLI:

```bash
npm install -g @anthropic-ai/mcpb
mcpb validate manifest.json
mcpb pack
```

This creates an installable `.mcpb` bundle for desktop clients that support MCP
Bundles. Older DXT-only clients may require the legacy `@anthropic-ai/dxt`
toolchain, but the packaging model is the same: a zip archive with
`manifest.json` and the MCP server files.

---

## ⚙️ Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `MIMO_API_KEY` | *(required)* | Your MiMo platform API key |
| `MIMO_BASE_URL` | `https://api.xiaomimimo.com/v1` | API base URL |
| `MIMO_MODEL` | `mimo-v2.5` | Model ID |

---

## 🛠️ MCP Tool

### `mimo_image_analyze`

Analyze an image and return a text-based visual description.

**Parameters:**

| Param | Type | Required | Description |
|-------|------|:--------:|-------------|
| `image_path` | string | ✅ | Local file path or http(s) URL |
| `prompt` | string | | Custom prompt (default: detailed description) |

**Example usage by an agent:**

```json
{
  "image_path": "/path/to/screenshot.png",
  "prompt": "What error does this screenshot show?"
}
```

---

## 🎯 Use Cases

| Scenario | Example |
|----------|---------|
| Screenshot debugging | Explain an error from a screenshot |
| UI analysis | Describe a webpage or app layout |
| OCR extraction | Read text from an image |
| Chart interpretation | Explain a chart or table image |
| Document analysis | Understand scanned documents |
| Agent vision extension | Give text-only agents vision tools |

---

## 🔗 Related Official Resources

This project is **an independent community MCP bridge** for the Xiaomi MiMo ecosystem.

Official Xiaomi MiMo resources:

- [XiaomiMiMo GitHub Organization](https://github.com/XiaomiMiMo)
- [XiaomiMiMo/MiMo](https://github.com/XiaomiMiMo/MiMo)
- [XiaomiMiMo/MiMo-VL](https://github.com/XiaomiMiMo/MiMo-VL)
- [XiaomiMiMo/MiMo-Skills](https://github.com/XiaomiMiMo/MiMo-Skills)
- [XiaomiMiMo/MiMo-V2-Flash](https://github.com/XiaomiMiMo/MiMo-V2-Flash)

---

## 📦 Project Structure

```
mimo-vision-mcp/
├── README.md
├── LICENSE              (MIT)
├── .gitignore
├── .env.example
├── .mcpbignore          (MCPB/DXT packaging ignore rules)
├── manifest.json        (MCPB/DXT bundle manifest)
├── pyproject.toml       (uv bundle dependencies)
├── requirements.txt
├── server.py            (legacy direct MCP server entry)
└── src/
    └── server.py        (MCPB/DXT bundle entry)
```

---

## 🧩 Design Philosophy

This project separates two responsibilities:

```
┌──────────────────────────┐
│ Main LLM                  │
│ Reasoning / planning /    │
│ coding / conversation     │
└─────────────┬────────────┘
              │  delegates visual perception
              ▼
┌──────────────────────────┐
│ MiMo Vision MCP            │
│ Image understanding / OCR  │
└──────────────────────────┘
```

The main model stays in charge of reasoning. MiMo Vision provides perception.

---

## 🔒 Security

- Never commit `.env` (it is in `.gitignore`)
- Never expose API keys in logs
- Validate local image paths before reading files
- Be careful with screenshots containing tokens, credentials, or personal data
- Uses `trust_env=False` — bypasses system proxy, connects directly to MiMo API

---

## 🗺️ Roadmap

- [x] Local image path input
- [x] Remote image URL input
- [ ] Structured JSON output mode
- [ ] OCR-focused mode
- [ ] Batch image analysis
- [ ] More MCP client config examples (OpenClaw, Claude Desktop, Cursor)

---

## 📄 License

MIT License · Copyright (c) 2026 SeverinQuan

---

## 👤 Author

Created by [SeverinQuan](https://github.com/SeverinQuan)

---

## 🏷️ Keywords

`MCP` · `MiMo` · `Vision MCP` · `Image Analysis` · `OCR` · `Multimodal AI`
`DeepSeek` · `Text-only LLM` · `Agent Tool` · `Visual Understanding`
`Screenshot Analysis` · `AI Agent` · `Model Context Protocol` · `Python`

---

# 中文

## 📌 项目简介

`mimo-vision-mcp` 是一个轻量级 **MCP 服务**，用于让**纯文本大模型获得图像理解能力**。

它适合推理、编码、规划能力很强，但本身没有视觉能力的模型或 Agent。当主模型收到图片、截图、图表等视觉任务时，可以调用 `mimo_image_analyze` MCP 工具，将图片交给 MiMo Vision 分析，再把返回的文本描述交给主模型继续推理和回答。

一句话概括：

```txt
纯文本大模型 + MiMo Vision MCP = 可看图的 Agent
```

---

## 🧠 工作原理

```
┌────────────────────┐
│   用户消息          │
│  图片 / 截图 / 图表  │
└─────────┬──────────┘
          │
          ▼
┌────────────────────┐
│ 纯文本大模型        │
│ DeepSeek / Qwen /   │
│ 自定义 Agent        │
└─────────┬──────────┘
          │  发现自己需要图像理解能力
          ▼
┌────────────────────────────┐
│ mimo_image_analyze 工具      │
│ MCP 视觉桥接层               │
└─────────┬──────────────────┘
          │  图片路径 / 图片 URL（base64 编码）
          ▼
┌────────────────────────────┐
│ MiMo Vision API             │
│ v2.5 多模态模型              │
└─────────┬──────────────────┘
          │  文本描述 / 视觉分析
          ▼
┌────────────────────┐
│ 纯文本大模型        │
│ 基于文本结果继续推理 │
└─────────┬──────────┘
          │
          ▼
┌────────────────────┐
│ 最终回复            │
└────────────────────┘
```

---

## ✨ 功能特性

- 👁️ 为纯文本大模型补充视觉理解能力
- 🔌 标准 MCP 工具服务（stdio 传输）
- 🖼️ 支持本地图片路径和远程 URL
- 📝 返回干净的文本描述，方便主模型继续推理
- 🌏 国内直连，不经过代理
- ⚡ 轻量级 — 单文件 Python 实现
- 🧠 主模型负责推理，MiMo 负责看图

---

## 🚀 快速开始

### 1. 克隆仓库

```bash
git clone https://github.com/SeverinQuan/mimo-vision-mcp.git
cd mimo-vision-mcp
```

### 2. 安装依赖

```bash
pip install -r requirements.txt
```

### 3. 配置 API Key

```bash
cp .env.example .env
# 编辑 .env，替换为你的真实 MiMo API Key
```

### 4. 配置 MCP 客户端

在 MCP 客户端配置中（Claude Desktop / Cline / Cursor / OpenClaw / OpenCode）添加：

```json
{
  "mcpServers": {
    "mimo-vision": {
      "command": "python",
      "args": ["/path/to/mimo-vision-mcp/server.py"],
      "env": {
        "MIMO_API_KEY": "your_mimo_api_key_here"
      }
    }
  }
}
```

### 5. 重启客户端

`mimo_image_analyze` 工具应该已经可以使用。

---

## 📦 一键安装包

本仓库也包含 MCPB/DXT 友好的安装包配置。

MiMo API Key **不会**写入代码或打包产物。它在 `manifest.json` 中声明为
敏感的 `user_config` 配置项，安装时由客户端收集，并在运行时注入为
`MIMO_API_KEY` 环境变量。

使用当前官方 MCPB CLI 构建：

```bash
npm install -g @anthropic-ai/mcpb
mcpb validate manifest.json
mcpb pack
```

这会生成可安装的 `.mcpb` 包，用于支持 MCP Bundles 的桌面客户端。旧版
DXT-only 客户端可能需要使用旧的 `@anthropic-ai/dxt` 工具链，但核心格式
仍然是包含 `manifest.json` 和 MCP server 文件的压缩包。

---

## ⚙️ 环境变量

| 变量 | 默认值 | 说明 |
|----------|---------|-------------|
| `MIMO_API_KEY` | *(必填)* | MiMo 开放平台 API Key |
| `MIMO_BASE_URL` | `https://api.xiaomimimo.com/v1` | API 地址 |
| `MIMO_MODEL` | `mimo-v2.5` | 模型标识 |

---

## 🛠️ MCP 工具

### `mimo_image_analyze`

用于分析图片，并返回文本形式的视觉描述。

**参数：**

| 参数 | 类型 | 必填 | 说明 |
|-------|------|:--------:|-------------|
| `image_path` | string | ✅ | 本地文件路径或 http(s) URL |
| `prompt` | string | | 自定义提问（默认：详细描述图片） |

**Agent 调用示例：**

```json
{
  "image_path": "/path/to/screenshot.png",
  "prompt": "这张截图显示了什么错误信息？"
}
```

---

## 🎯 使用场景

| 场景 | 示例 |
|----------|---------|
| 截图排错 | 分析报错截图、控制台截图 |
| UI 分析 | 描述网页、App、后台页面布局 |
| OCR 提取 | 读取图片中的文字 |
| 图表理解 | 解读图表、表格截图 |
| 文档分析 | 分析扫描件、图片版文档 |
| Agent 视觉扩展 | 给纯文本 Agent 接入看图能力 |

---

## 🔗 相关官方资源

本项目是面向 Xiaomi MiMo 生态的**独立社区 MCP 桥接项目**。

Xiaomi MiMo 官方资源：

- [XiaomiMiMo GitHub 组织](https://github.com/XiaomiMiMo)
- [XiaomiMiMo/MiMo](https://github.com/XiaomiMiMo/MiMo)
- [XiaomiMiMo/MiMo-VL](https://github.com/XiaomiMiMo/MiMo-VL)
- [XiaomiMiMo/MiMo-Skills](https://github.com/XiaomiMiMo/MiMo-Skills)
- [XiaomiMiMo/MiMo-V2-Flash](https://github.com/XiaomiMiMo/MiMo-V2-Flash)

---

## 📦 项目结构

```
mimo-vision-mcp/
├── README.md
├── LICENSE              (MIT)
├── .gitignore
├── .env.example
├── .mcpbignore          (MCPB/DXT 打包忽略规则)
├── manifest.json        (MCPB/DXT 安装包 manifest)
├── pyproject.toml       (uv 打包依赖)
├── requirements.txt
├── server.py            (兼容旧配置的 MCP 入口)
└── src/
    └── server.py        (MCPB/DXT 安装包入口)
```

---

## 🧩 设计理念

本项目不是为了替代原生多模态大模型。它把职责拆开：

```
┌──────────────────────────┐
│ 主大模型                  │
│ 推理 / 规划 / 编码 / 对话  │
└─────────────┬────────────┘
              │  将视觉感知任务委托出去
              ▼
┌──────────────────────────┐
│ MiMo Vision MCP            │
│ 图像理解 / OCR / 截图分析  │
└──────────────────────────┘
```

主模型负责思考，MiMo Vision 负责看图。低耦合、可替换、易编排。

---

## 🔒 安全提示

- 不要提交 `.env`（已在 `.gitignore` 中忽略）
- 不要在日志中输出 API Key
- 读取本地图片前应校验路径
- 截图中可能包含 token、聊天记录、密钥或个人隐私信息，注意脱敏
- 服务端使用 `trust_env=False`，绕过系统代理，直连 MiMo API

---

## 🗺️ 开发计划

- [x] 本地图片路径输入
- [x] 远程图片 URL 输入
- [ ] 结构化 JSON 输出模式
- [ ] OCR 专用模式
- [ ] 批量图片分析
- [ ] 更多 MCP 客户端配置示例（OpenClaw, Claude Desktop, Cursor）

---

## 📄 开源协议

MIT License · Copyright (c) 2026 SeverinQuan

---

## 👤 作者

Created by [SeverinQuan](https://github.com/SeverinQuan)

---

## 🏷️ 关键词

`MCP` · `MiMo` · `Vision MCP` · `Image Analysis` · `OCR` · `Multimodal AI`
`DeepSeek` · `Text-only LLM` · `Agent Tool` · `Visual Understanding`
`Screenshot Analysis` · `AI Agent` · `Model Context Protocol` · `Python`
`图像理解` · `视觉 MCP` · `纯文本大模型` · `多模态桥接` · `智能体工具`

---

## ⭐ Star History

If this project helps you build a better AI agent workflow, feel free to give it a star.

如果这个项目对你的 Agent 工作流有帮助，欢迎点一个 Star。

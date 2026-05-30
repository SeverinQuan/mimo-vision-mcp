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

## 🧩 Runtime Requirements

### Client compatibility

| Package | Use when | Runtime needed |
|---------|----------|----------------|
| `.mcpb` | Your client supports MCP Bundle / MCPB packages | Client-provided Python or `uv` runtime |
| `.dxt` | Your client only supports legacy Desktop Extension / DXT packages | Python 3.8.0 or newer |
| Source install | Your client uses manual `mcpServers` JSON configuration | Python 3.8.0 or newer |

Supported MCP clients include Claude Desktop, Cline, Cursor, OpenClaw, OpenCode,
and other clients that can start a stdio MCP server with `command`, `args`, and
`env`.

### Python runtime

- Minimum Python version: `3.8.0`
- Recommended Python version: `3.10+` when available
- Python packages:

```txt
httpx>=0.27,<0.29
anyio>=4.0,<4.6
```

The server implements MCP stdio directly and does **not** require the Python
`mcp` package. This keeps the legacy DXT package usable on Python 3.8.

### Build tools

Only needed if you build packages yourself:

| Tool | Required for | Install command |
|------|--------------|-----------------|
| `@anthropic-ai/mcpb` | Build `.mcpb` package | `npm install -g @anthropic-ai/mcpb` |
| `@anthropic-ai/dxt` | Build legacy `.dxt` package | `npm install -g @anthropic-ai/dxt` |

The prebuilt release packages already include the needed manifest and bundled
DXT dependencies, so normal users only need to install the package and fill in
the MiMo API key.

---

## 🚀 Manual MCP Install

Use this path when your MCP client still expects a manual `mcpServers` JSON
configuration.

### 1. Clone the repository

```bash
git clone https://github.com/SeverinQuan/mimo-vision-mcp.git
cd mimo-vision-mcp
```

### 2. Install Python dependencies

Python 3.8.0 or newer is supported. The server uses a lightweight native MCP
stdio implementation and keeps dependencies limited to Python 3.8-compatible
HTTP packages.

```bash
pip install -r requirements.txt
```

### 3. Get and set your MiMo API key

Get a MiMo API key from the Xiaomi MiMo platform, then either export it in your
shell:

```bash
export MIMO_API_KEY="your_mimo_api_key_here"
export MIMO_MODEL="mimo-v2.5"
export MIMO_BASE_URL="https://api.xiaomimimo.com/v1"
```

Or keep it in your MCP client configuration as shown below. `.env` is provided
only as a local note template; the server reads environment variables.

```bash
cp .env.example .env
# Optional local note only. Do not commit .env.
```

### 4. Configure your MCP client manually

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

### 5. Restart the client

The `mimo_image_analyze` tool should now be available.

---

## 📦 MCPB / DXT Install

This repository can publish both installable bundle formats:

| Format | File | Best for |
|--------|------|----------|
| MCPB | `dist/mimo-vision-mcp-1.0.0.mcpb` | Current MCP Bundle clients and newer Claude Desktop builds |
| DXT | `dist/mimo-vision-mcp-1.0.0.dxt` | Legacy Desktop Extension clients |

The MiMo API key is **not** stored in code or in the bundle. It is declared in
`manifest.json` as a sensitive `user_config` field and injected at runtime as
`MIMO_API_KEY`. The bundle hardcodes the official MiMo API base URL and default
model to avoid client-side `user_config` interpolation issues.

### Option A: Install a prebuilt package

1. Download the `.mcpb` or `.dxt` file from the release assets.
2. Open your desktop MCP client.
3. Go to the extensions or MCP bundle page.
4. Import or double-click the downloaded package.
5. Fill in the prompted fields:

```text
MiMo API Key: your_mimo_api_key_here
```

Only paste the raw key value, such as `sk-xxxx`. Do not include
`MIMO_API_KEY=`, quotes, or leading/trailing spaces.

6. Enable the extension and restart the client if required.
7. Confirm that the `mimo_image_analyze` tool is listed.

### Option B: Build the current MCPB package

Use this for current MCPB-compatible clients:

```bash
npm install -g @anthropic-ai/mcpb
mcpb validate manifest.json
mcpb pack . dist/mimo-vision-mcp-1.0.0.mcpb
```

### Option C: Build the legacy DXT package

Use this for older DXT-only clients:

```bash
npm install -g @anthropic-ai/dxt
python3 -m pip install -r legacy-dxt/requirements.txt -t legacy-dxt/server/lib
dxt validate legacy-dxt/manifest.json
dxt pack legacy-dxt dist/mimo-vision-mcp-1.0.0.dxt
```

The DXT package bundles Python dependencies under `legacy-dxt/server/lib`, so it
is larger than the MCPB package. The legacy DXT runtime supports Python 3.8.0
or newer.

### Option D: Build both formats

To publish both formats from the same repository, run:

```bash
bash scripts/build_bundles.sh
```

It writes both artifacts to `dist/`:

- `mimo-vision-mcp-1.0.0.mcpb` for the current MCPB toolchain
- `mimo-vision-mcp-1.0.0.dxt` for legacy DXT clients

Both packages are unsigned by default. Sign them before public distribution if
your target client or release process requires signed bundles.

---

## ⚙️ Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `MIMO_API_KEY` | *(required)* | Your MiMo platform API key |
| `MIMO_BASE_URL` | `https://api.xiaomimimo.com/v1` | Hardcoded in bundle manifests; optional manual override |
| `MIMO_MODEL` | `mimo-v2.5` | Hardcoded in bundle manifests; optional manual override |

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

## 🧩 依赖环境

### 客户端兼容性

| 安装包 | 适用场景 | 所需运行环境 |
|--------|----------|--------------|
| `.mcpb` | 客户端支持 MCP Bundle / MCPB 包 | 客户端提供的 Python 或 `uv` 运行时 |
| `.dxt` | 客户端只支持旧版 Desktop Extension / DXT 包 | Python 3.8.0 或以上 |
| 源码安装 | 客户端使用手写 `mcpServers` JSON 配置 | Python 3.8.0 或以上 |

支持的 MCP 客户端包括 Claude Desktop、Cline、Cursor、OpenClaw、OpenCode，
以及其他能够通过 `command`、`args`、`env` 启动 stdio MCP server 的客户端。

### Python 运行时

- 最低 Python 版本：`3.8.0`
- 推荐 Python 版本：有条件时使用 `3.10+`
- Python 依赖包：

```txt
httpx>=0.27,<0.29
anyio>=4.0,<4.6
```

服务端直接实现 MCP stdio 协议，不依赖 Python `mcp` 包，因此旧版 DXT 包可以在
Python 3.8 环境中使用。

### 构建工具

只有你需要自己构建安装包时才需要安装：

| 工具 | 用途 | 安装命令 |
|------|------|----------|
| `@anthropic-ai/mcpb` | 构建 `.mcpb` 包 | `npm install -g @anthropic-ai/mcpb` |
| `@anthropic-ai/dxt` | 构建旧版 `.dxt` 包 | `npm install -g @anthropic-ai/dxt` |

预构建 Release 包已经包含所需 manifest；DXT 包也已经打入依赖。普通用户只需要
安装对应包，然后填写 MiMo API Key。

---

## 🚀 手动 MCP 安装

如果你的 MCP 客户端仍然使用手写 `mcpServers` JSON 配置，使用这一种方式。

### 1. 克隆仓库

```bash
git clone https://github.com/SeverinQuan/mimo-vision-mcp.git
cd mimo-vision-mcp
```

### 2. 安装 Python 依赖

支持 Python 3.8.0 及以上版本。服务端使用轻量级原生 MCP stdio 实现，
依赖限定为兼容 Python 3.8 的 HTTP 包。

```bash
pip install -r requirements.txt
```

### 3. 获取并配置 MiMo API Key

先从 Xiaomi MiMo 平台获取 API Key，然后可以在 shell 里导出环境变量：

```bash
export MIMO_API_KEY="your_mimo_api_key_here"
export MIMO_MODEL="mimo-v2.5"
export MIMO_BASE_URL="https://api.xiaomimimo.com/v1"
```

也可以直接写在 MCP 客户端配置里，见下一步。`.env` 只作为本地记录模板；
服务本身读取的是环境变量。

```bash
cp .env.example .env
# 可选本地记录。不要提交 .env。
```

### 4. 手动配置 MCP 客户端

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

## 📦 MCPB / DXT 安装

本仓库可以发布两种可安装包格式：

| 格式 | 文件 | 适用场景 |
|------|------|----------|
| MCPB | `dist/mimo-vision-mcp-1.0.0.mcpb` | 当前 MCP Bundle 客户端和新版 Claude Desktop |
| DXT | `dist/mimo-vision-mcp-1.0.0.dxt` | 旧版 Desktop Extension 客户端 |

MiMo API Key **不会**写入代码或打包产物。它在 `manifest.json` 中声明为
敏感的 `user_config` 配置项，安装时由客户端收集，并在运行时注入为
`MIMO_API_KEY` 环境变量。安装包会固定写入官方 MiMo API 地址和默认模型，
避免客户端未正确展开 `user_config` 时导致启动失败。

### 方式 A：安装预构建包

1. 从 release assets 下载 `.mcpb` 或 `.dxt` 文件。
2. 打开你的桌面 MCP 客户端。
3. 进入 extensions / MCP bundle 页面。
4. 导入或双击下载的安装包。
5. 按提示填写配置：

```text
MiMo API Key: your_mimo_api_key_here
```

只填写原始 Key 值，例如 `sk-xxxx`。不要带 `MIMO_API_KEY=`，不要加引号，
前后也不要有空格。

6. 启用扩展；如客户端要求，重启一次。
7. 确认工具列表中出现 `mimo_image_analyze`。

### 方式 B：构建新版 MCPB 包

适用于支持 MCPB 的当前客户端：

```bash
npm install -g @anthropic-ai/mcpb
mcpb validate manifest.json
mcpb pack . dist/mimo-vision-mcp-1.0.0.mcpb
```

### 方式 C：构建旧版 DXT 包

适用于只支持旧 DXT 的客户端：

```bash
npm install -g @anthropic-ai/dxt
python3 -m pip install -r legacy-dxt/requirements.txt -t legacy-dxt/server/lib
dxt validate legacy-dxt/manifest.json
dxt pack legacy-dxt dist/mimo-vision-mcp-1.0.0.dxt
```

DXT 包会把 Python 依赖放进 `legacy-dxt/server/lib`，因此体积会比 MCPB
包更大。旧版 DXT 运行时支持 Python 3.8.0 及以上版本。

### 方式 D：同时构建两种格式

如需从同一仓库同时发布两种格式，运行：

```bash
bash scripts/build_bundles.sh
```

脚本会将两个产物写入 `dist/`：

- `mimo-vision-mcp-1.0.0.mcpb`：当前 MCPB 工具链
- `mimo-vision-mcp-1.0.0.dxt`：旧 DXT 客户端兼容包

两个安装包默认未签名。如果目标客户端或发布流程要求签名，请在公开分发前
补充签名步骤。

---

## ⚙️ 环境变量

| 变量 | 默认值 | 说明 |
|----------|---------|-------------|
| `MIMO_API_KEY` | *(必填)* | MiMo 开放平台 API Key |
| `MIMO_BASE_URL` | `https://api.xiaomimimo.com/v1` | 安装包 manifest 中已固定；手动配置时可覆盖 |
| `MIMO_MODEL` | `mimo-v2.5` | 安装包 manifest 中已固定；手动配置时可覆盖 |

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

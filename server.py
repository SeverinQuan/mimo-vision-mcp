#!/usr/bin/env python3
"""
MiMo Vision MCP Server
========================
bridges text-only LLMs to MiMo v2.5 multimodal vision capabilities via MCP.

Requires:
    MIMO_API_KEY  — your MiMo platform API key (env var)
"""

import os, sys, base64, asyncio
from pathlib import Path

from openai import AsyncOpenAI
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent

# ── config ──────────────────────────────────────────────
MIMO_BASE  = os.environ.get("MIMO_BASE_URL", "https://api.xiaomimimo.com/v1")
MIMO_MODEL = os.environ.get("MIMO_MODEL", "mimo-v2.5")
MIMO_KEY   = os.environ.get("MIMO_API_KEY", "")

if not MIMO_KEY:
    print("FATAL: MIMO_API_KEY environment variable is required.", file=sys.stderr)
    sys.exit(1)

# ── HTTP client (NO proxy) ──────────────────────────────
import httpx

_http = httpx.AsyncClient(
    timeout=httpx.Timeout(60.0),
    trust_env=False,   # bypass system-wide http_proxy for domestic direct connection
)

client = AsyncOpenAI(
    api_key=MIMO_KEY,
    base_url=MIMO_BASE,
    http_client=_http,
    default_headers={"api-key": MIMO_KEY},   # MiMo uses api-key header (not Authorization: Bearer)
)

# ── MCP server ──────────────────────────────────────────
server = Server("mimo-vision")


@server.list_tools()
async def list_tools() -> list[Tool]:
    return [
        Tool(
            name="mimo_image_analyze",
            description=(
                "Analyze an image using Xiaomi MiMo v2.5 vision model. "
                "Supports local file paths (jpg/png/webp) and remote http(s) URLs. "
                "Returns a text description of the image content."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "image_path": {
                        "type": "string",
                        "description": "Path to a local image file or a http(s) URL.",
                    },
                    "prompt": {
                        "type": "string",
                        "description": "What to ask about the image (default: detailed description).",
                    },
                },
                "required": ["image_path"],
            },
        ),
    ]


def _encode_image(path: str) -> str:
    """Return base64 data-uri for local file, or raw url for remote."""
    if path.startswith("http://") or path.startswith("https://"):
        return path
    p = Path(path)
    if not p.exists():
        raise FileNotFoundError(f"Image not found: {path}")
    raw = p.read_bytes()
    ext = p.suffix.lower().lstrip(".")
    mime = {"jpg": "jpeg", "jpeg": "jpeg", "png": "png", "webp": "webp", "gif": "gif"}.get(ext, "jpeg")
    b64 = base64.b64encode(raw).decode()
    return f"data:image/{mime};base64,{b64}"


@server.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent]:
    if name != "mimo_image_analyze":
        raise ValueError(f"Unknown tool: {name}")

    image_path = arguments["image_path"]
    prompt = arguments.get("prompt", "Please describe the content of this image in detail.")

    try:
        image_uri = _encode_image(image_path)
    except FileNotFoundError as e:
        return [TextContent(type="text", text=f"Error: {e}")]

    try:
        response = await client.chat.completions.create(
            model=MIMO_MODEL,
            messages=[{
                "role": "user",
                "content": [
                    {"type": "image_url", "image_url": {"url": image_uri}},
                    {"type": "text", "text": prompt},
                ],
            }],
            max_completion_tokens=2048,
        )
    except Exception as e:
        return [TextContent(type="text", text=f"MiMo API error: {e}")]

    result = response.choices[0].message.content or "(empty response)"
    return [TextContent(type="text", text=result)]


# ── entry ───────────────────────────────────────────────
async def main():
    async with stdio_server() as (read, write):
        await server.run(read, write, server.create_initialization_options())


if __name__ == "__main__":
    asyncio.run(main())

#!/usr/bin/env python3
"""
MiMo Vision MCP server.

This entry point is intended for DXT/MCPB packaging. Runtime configuration is
provided by the host application through manifest user_config and environment
variable substitution.
"""

import asyncio
import base64
import os
import sys
from pathlib import Path

import httpx
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import TextContent, Tool
from openai import AsyncOpenAI


MIMO_BASE = os.environ.get("MIMO_BASE_URL", "https://api.xiaomimimo.com/v1")
MIMO_MODEL = os.environ.get("MIMO_MODEL", "mimo-v2.5")
MIMO_KEY = os.environ.get("MIMO_API_KEY", "")

if not MIMO_KEY:
    print(
        "FATAL: MIMO_API_KEY is required. Configure it in the extension settings.",
        file=sys.stderr,
    )
    sys.exit(1)

http_client = httpx.AsyncClient(
    timeout=httpx.Timeout(60.0),
    trust_env=False,
)

client = AsyncOpenAI(
    api_key=MIMO_KEY,
    base_url=MIMO_BASE,
    http_client=http_client,
    default_headers={"api-key": MIMO_KEY},
)

server = Server("mimo-vision")


@server.list_tools()
async def list_tools() -> list[Tool]:
    return [
        Tool(
            name="mimo_image_analyze",
            description=(
                "Analyze an image using Xiaomi MiMo v2.5 vision model. "
                "Supports local image files and http(s) image URLs."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "image_path": {
                        "type": "string",
                        "description": "Path to a local image file or an http(s) URL.",
                    },
                    "prompt": {
                        "type": "string",
                        "description": "Question or instruction for image analysis.",
                        "default": "Please describe the content of this image in detail.",
                    },
                },
                "required": ["image_path"],
            },
        )
    ]


def encode_image(path: str) -> str:
    if path.startswith(("http://", "https://")):
        return path

    image_file = Path(path)
    if not image_file.exists():
        raise FileNotFoundError(f"Image not found: {path}")
    if not image_file.is_file():
        raise FileNotFoundError(f"Image path is not a file: {path}")

    raw = image_file.read_bytes()
    ext = image_file.suffix.lower().lstrip(".")
    mime_subtype = {
        "jpg": "jpeg",
        "jpeg": "jpeg",
        "png": "png",
        "webp": "webp",
        "gif": "gif",
    }.get(ext, "jpeg")
    encoded = base64.b64encode(raw).decode("ascii")
    return f"data:image/{mime_subtype};base64,{encoded}"


@server.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent]:
    if name != "mimo_image_analyze":
        raise ValueError(f"Unknown tool: {name}")

    image_path = arguments["image_path"]
    prompt = arguments.get(
        "prompt",
        "Please describe the content of this image in detail.",
    )

    try:
        image_uri = encode_image(image_path)
    except FileNotFoundError as exc:
        return [TextContent(type="text", text=f"Error: {exc}")]

    try:
        response = await client.chat.completions.create(
            model=MIMO_MODEL,
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "image_url", "image_url": {"url": image_uri}},
                        {"type": "text", "text": prompt},
                    ],
                }
            ],
            max_completion_tokens=2048,
        )
    except Exception as exc:
        return [TextContent(type="text", text=f"MiMo API error: {exc}")]

    result = response.choices[0].message.content or "(empty response)"
    return [TextContent(type="text", text=result)]


async def main() -> None:
    async with stdio_server() as (read, write):
        await server.run(read, write, server.create_initialization_options())


if __name__ == "__main__":
    asyncio.run(main())

#!/usr/bin/env python3
"""
MiMo Vision MCP server.

This implementation speaks the MCP stdio JSON-RPC transport directly so the
bundle can run on Python 3.8 without depending on the Python `mcp` package,
which requires newer Python versions.
"""

import asyncio
import base64
import json
import os
import sys
from pathlib import Path
from typing import Any, Dict, Optional

import httpx


MIMO_BASE = os.environ.get("MIMO_BASE_URL", "https://api.xiaomimimo.com/v1").rstrip("/")
MIMO_MODEL = os.environ.get("MIMO_MODEL", "mimo-v2.5")
MIMO_KEY = os.environ.get("MIMO_API_KEY", "")

TOOL = {
    "name": "mimo_image_analyze",
    "description": (
        "Analyze an image using Xiaomi MiMo v2.5 vision model. "
        "Supports local image files and http(s) image URLs."
    ),
    "inputSchema": {
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
}


def encode_image(path: str) -> str:
    if path.startswith(("http://", "https://")):
        return path

    image_file = Path(path)
    if not image_file.exists():
        raise FileNotFoundError("Image not found: {0}".format(path))
    if not image_file.is_file():
        raise FileNotFoundError("Image path is not a file: {0}".format(path))

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
    return "data:image/{0};base64,{1}".format(mime_subtype, encoded)


async def analyze_image(arguments: Dict[str, Any]) -> str:
    if not MIMO_KEY:
        return "Error: MIMO_API_KEY is required. Configure it in the extension settings."

    image_path = arguments.get("image_path")
    if not image_path:
        return "Error: image_path is required."

    prompt = arguments.get(
        "prompt",
        "Please describe the content of this image in detail.",
    )

    try:
        image_uri = encode_image(str(image_path))
    except FileNotFoundError as exc:
        return "Error: {0}".format(exc)

    payload = {
        "model": MIMO_MODEL,
        "messages": [
            {
                "role": "user",
                "content": [
                    {"type": "image_url", "image_url": {"url": image_uri}},
                    {"type": "text", "text": prompt},
                ],
            }
        ],
        "max_completion_tokens": 2048,
    }
    headers = {
        "Authorization": "Bearer {0}".format(MIMO_KEY),
        "api-key": MIMO_KEY,
        "Content-Type": "application/json",
    }

    try:
        async with httpx.AsyncClient(
            timeout=httpx.Timeout(60.0),
            trust_env=False,
        ) as client:
            response = await client.post(
                "{0}/chat/completions".format(MIMO_BASE),
                headers=headers,
                json=payload,
            )
            response.raise_for_status()
            data = response.json()
    except Exception as exc:
        return "MiMo API error: {0}".format(exc)

    try:
        return data["choices"][0]["message"].get("content") or "(empty response)"
    except Exception:
        return "MiMo API error: unexpected response {0}".format(data)


def read_message() -> Optional[Dict[str, Any]]:
    headers = {}
    while True:
        line = sys.stdin.buffer.readline()
        if line == b"":
            return None
        if line in (b"\r\n", b"\n"):
            break
        name, value = line.decode("ascii").split(":", 1)
        headers[name.lower()] = value.strip()

    length = int(headers.get("content-length", "0"))
    if length <= 0:
        return None
    body = sys.stdin.buffer.read(length)
    return json.loads(body.decode("utf-8"))


def write_message(message: Dict[str, Any]) -> None:
    body = json.dumps(message, separators=(",", ":"), ensure_ascii=False).encode("utf-8")
    sys.stdout.buffer.write(b"Content-Length: " + str(len(body)).encode("ascii") + b"\r\n\r\n")
    sys.stdout.buffer.write(body)
    sys.stdout.buffer.flush()


def result_response(request_id: Any, result: Dict[str, Any]) -> Dict[str, Any]:
    return {"jsonrpc": "2.0", "id": request_id, "result": result}


def error_response(request_id: Any, code: int, message: str) -> Dict[str, Any]:
    return {"jsonrpc": "2.0", "id": request_id, "error": {"code": code, "message": message}}


async def handle_request(message: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    method = message.get("method")
    request_id = message.get("id")
    params = message.get("params") or {}

    if request_id is None:
        return None

    if method == "initialize":
        return result_response(
            request_id,
            {
                "protocolVersion": params.get("protocolVersion", "2024-11-05"),
                "capabilities": {"tools": {}},
                "serverInfo": {"name": "mimo-vision", "version": "1.0.0"},
            },
        )

    if method == "ping":
        return result_response(request_id, {})

    if method == "tools/list":
        return result_response(request_id, {"tools": [TOOL]})

    if method == "tools/call":
        name = params.get("name")
        arguments = params.get("arguments") or {}
        if name != "mimo_image_analyze":
            return error_response(request_id, -32602, "Unknown tool: {0}".format(name))
        text = await analyze_image(arguments)
        return result_response(
            request_id,
            {"content": [{"type": "text", "text": text}], "isError": text.startswith("Error:")},
        )

    return error_response(request_id, -32601, "Method not found: {0}".format(method))


async def main() -> None:
    loop = asyncio.get_event_loop()
    while True:
        message = await loop.run_in_executor(None, read_message)
        if message is None:
            return
        response = await handle_request(message)
        if response is not None:
            write_message(response)


if __name__ == "__main__":
    asyncio.run(main())

# MiMo Vision MCP v1.0.1-dual

This release publishes both current MCPB and legacy DXT installable packages.

## Highlights

- Adds MCPB bundle support through `manifest.json` and `pyproject.toml`.
- Adds legacy DXT bundle support through `legacy-dxt/manifest.json`.
- Keeps `MIMO_API_KEY` out of source code and package contents by using sensitive `user_config`.
- Hardcodes the official MiMo base URL and default model in both bundle manifests to avoid client-side interpolation failures.
- Lowers the Python runtime requirement to Python 3.8.0 by replacing Python `mcp` / `openai` package usage with a native MCP stdio implementation and direct `httpx` API calls.
- Includes both installable artifacts:
  - `mimo-vision-mcp-1.0.0.mcpb`
  - `mimo-vision-mcp-1.0.0.dxt`
- Documents manual MCP setup, MCPB install, DXT install, and dual-format builds in English and Chinese.

## Installation

Download the package that matches your client:

- Use `.mcpb` for current MCP Bundle clients.
- Use `.dxt` for legacy Desktop Extension clients.

During installation, fill in:

```text
MiMo API Key: your_mimo_api_key_here
```

Paste only the raw key value, such as `sk-xxxx`; do not include
`MIMO_API_KEY=`, quotes, or spaces.

## Notes

The packages are not signed. If your target client requires signed bundles, sign the release assets before redistribution.

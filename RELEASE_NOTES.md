# MiMo Vision MCP v1.0.1-dual

This release publishes both current MCPB and legacy DXT installable packages.

## Highlights

- Adds MCPB bundle support through `manifest.json` and `pyproject.toml`.
- Adds legacy DXT bundle support through `legacy-dxt/manifest.json`.
- Keeps `MIMO_API_KEY` out of source code and package contents by using sensitive `user_config`.
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
MiMo Base URL: https://api.xiaomimimo.com/v1
MiMo Model: mimo-v2.5
```

## Notes

The packages are not signed. If your target client requires signed bundles, sign the release assets before redistribution.

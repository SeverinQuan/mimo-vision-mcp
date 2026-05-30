# MiMo Vision Legacy DXT Bundle

This directory is the source for the legacy `.dxt` package.

Use it for clients that still support the older Desktop Extensions toolchain
and do not support the newer `.mcpb` / `uv` bundle format yet.

The MiMo API key is declared as a sensitive `user_config` field in
`manifest.json` and is injected at runtime as `MIMO_API_KEY`.

Build from the repository root:

```bash
bash scripts/build_bundles.sh
```

The build script installs Python dependencies into `legacy-dxt/server/lib`
before packing so the final `.dxt` is self-contained for the legacy Python
bundle model. The legacy runtime supports Python 3.8.0 or newer and only
bundles Python 3.8-compatible HTTP dependencies; the server implements MCP
stdio directly.

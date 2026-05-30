#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
DIST="$ROOT/dist"

mkdir -p "$DIST"

echo "[1/4] Validate MCPB manifest"
npx -y @anthropic-ai/mcpb validate "$ROOT/manifest.json"

echo "[2/4] Build MCPB package"
npx -y @anthropic-ai/mcpb pack "$ROOT" "$DIST/mimo-vision-mcp-1.0.0.mcpb"

echo "[3/4] Prepare legacy DXT Python dependencies"
rm -rf "$ROOT/legacy-dxt/server/lib"
find "$ROOT/legacy-dxt" -type d -name "__pycache__" -prune -exec rm -rf {} +
python3 -m pip install \
  --disable-pip-version-check \
  --no-cache-dir \
  -r "$ROOT/legacy-dxt/requirements.txt" \
  -t "$ROOT/legacy-dxt/server/lib"

echo "[4/4] Validate and build legacy DXT package"
npx -y @anthropic-ai/dxt validate "$ROOT/legacy-dxt/manifest.json"
npx -y @anthropic-ai/dxt pack "$ROOT/legacy-dxt" "$DIST/mimo-vision-mcp-1.0.0.dxt"

echo "Built:"
echo "  $DIST/mimo-vision-mcp-1.0.0.mcpb"
echo "  $DIST/mimo-vision-mcp-1.0.0.dxt"

# Code Change Log

## 时间
- 日期: 2026-05-30
- 任务: 将 MiMo Vision MCP 的 Python 运行时要求降低到 3.8.0

## 变更摘要
- 移除对 Python `mcp` 与 `openai` 包的运行时依赖，避免被 Python >=3.10 门槛限制。
- 将服务端改为原生 MCP stdio JSON-RPC 实现，并使用 `httpx` 直接调用 MiMo OpenAI-compatible 接口。
- 将 `pyproject.toml` 的 `requires-python` 降低为 `>=3.8`。
- 将旧版 DXT manifest 的 Python runtime 降低为 `>=3.8.0`。
- 将依赖收敛为 Python 3.8-compatible HTTP 包，并约束 `anyio<4.6`。
- 更新中英文 README、legacy DXT README 与 Release Notes。
- 重新构建 MCPB 与 DXT 产物。

## 影响文件
- `src/server.py`: 改为原生 MCP stdio JSON-RPC 服务端。
- `server.py`: 同步手动 MCP 入口实现。
- `legacy-dxt/server/main.py`: 同步旧版 DXT 入口实现。
- `requirements.txt`: 移除 `mcp` / `openai`，保留 Python 3.8-compatible HTTP 依赖。
- `legacy-dxt/requirements.txt`: 同步旧版 DXT 打包依赖。
- `pyproject.toml`: 降低 Python 版本要求并更新依赖。
- `legacy-dxt/manifest.json`: 降低 runtime Python 要求到 `>=3.8.0`。
- `README.md`: 更新中英文 Python 3.8 兼容说明。
- `legacy-dxt/README.md`: 更新 legacy DXT Python 3.8 说明。
- `RELEASE_NOTES.md`: 记录 Python 3.8 runtime 兼容调整。
- `dist/mimo-vision-mcp-1.0.0.mcpb`: 重新构建 MCPB 产物。
- `dist/mimo-vision-mcp-1.0.0.dxt`: 重新构建 DXT 产物。

## 验证
- 执行命令: `python3 -m json.tool manifest.json >/dev/null && python3 -m json.tool legacy-dxt/manifest.json >/dev/null`
- 结果: 通过
- 执行命令: `ast.parse(..., feature_version=(3, 8))`
- 结果: `src/server.py`、`server.py`、`legacy-dxt/server/main.py` 均通过 Python 3.8 语法解析
- 执行命令: `python3 -m pip install --dry-run --ignore-installed --python-version 3.8 --only-binary=:all: --target /tmp/mimo-py38-test -r requirements.txt`
- 结果: 通过；解析到 `httpx-0.28.1`、`anyio-4.5.2` 等 Python 3.8-compatible 依赖
- 执行命令: stdio initialize/tools-list smoke test
- 结果: 通过；返回 `mimo_image_analyze`
- 执行命令: `bash scripts/build_bundles.sh`
- 结果: 通过；MCPB 与 DXT 均重新生成。pip 输出宿主环境中 `sse-starlette` 与 `anyio` 的全局依赖冲突提示，但目标安装目录为 `legacy-dxt/server/lib`，构建成功。

## 风险与回滚
- 风险: 原生 MCP stdio 实现覆盖当前工具列表与工具调用路径；若未来需要更多 MCP 能力，需要继续补充对应 JSON-RPC 方法。
- 回滚: `git revert <本次提交>`，或恢复到依赖 Python `mcp` 包的旧实现。

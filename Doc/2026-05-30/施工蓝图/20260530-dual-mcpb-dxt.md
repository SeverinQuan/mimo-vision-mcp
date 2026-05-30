# Code Change Log

## 时间
- 日期: 2026-05-30
- 任务: 为 MiMo Vision MCP 增加 MCPB 与旧 DXT 双格式发布能力

## 变更摘要
- 新建 `legacy-dxt` 旧 DXT 打包输入目录，使用 `dxt_version` 和传统 `python` server 类型兼容旧工具链。
- 新增 `scripts/build_bundles.sh`，一条命令生成 `.mcpb` 与 `.dxt` 两版发布产物。
- 调整 MCPB/DXT 忽略规则，避免新版 MCPB 包混入 legacy DXT 源目录，并避免旧 DXT 包混入 Python 缓存。
- 更新 README，补充双格式发布说明。

## 影响文件
- `.gitignore`: 忽略旧 DXT 构建时生成的 `legacy-dxt/server/lib/` 依赖目录。
- `.mcpbignore`: 排除 `legacy-dxt/`，让新版 MCPB 包保持轻量。
- `README.md`: 增加同时构建 `.mcpb` 与 `.dxt` 的说明。
- `legacy-dxt/manifest.json`: 新增旧 DXT schema 兼容 manifest。
- `legacy-dxt/server/main.py`: 新增旧 DXT Python server 入口。
- `legacy-dxt/requirements.txt`: 新增旧 DXT Python 依赖清单。
- `legacy-dxt/.dxtignore`: 新增旧 DXT 打包忽略规则。
- `legacy-dxt/README.md`: 新增旧 DXT 包说明。
- `scripts/build_bundles.sh`: 新增双格式构建脚本。
- `dist/mimo-vision-mcp-1.0.0.mcpb`: 更新新版 MCPB 产物。
- `dist/mimo-vision-mcp-1.0.0.dxt`: 新增旧 DXT 兼容产物。

## 验证
- 执行命令: `python3 -m py_compile server.py src/server.py legacy-dxt/server/main.py`
- 结果: 通过。
- 执行命令: `npx -y @anthropic-ai/dxt validate legacy-dxt/manifest.json`
- 结果: 通过，输出 `Manifest is valid!`。
- 执行命令: `bash scripts/build_bundles.sh`
- 结果: 通过，生成 `dist/mimo-vision-mcp-1.0.0.mcpb` 与 `dist/mimo-vision-mcp-1.0.0.dxt`。
- 执行命令: `npx -y @anthropic-ai/dxt info dist/mimo-vision-mcp-1.0.0.dxt`
- 结果: 可读取包信息；提示未签名。
- 执行命令: `npx -y @anthropic-ai/mcpb info dist/mimo-vision-mcp-1.0.0.mcpb`
- 结果: 可读取包信息；提示未签名。

## 风险与回滚
- 风险: 旧 DXT 包内置 Python 依赖，体积约 11MB，且未签名；公开发布前可考虑 release asset 签名。
- 风险: 旧 DXT 使用本机 Python 打包出的依赖，跨平台运行仍需在目标客户端实测。
- 回滚: `git revert <本次提交>` 或删除 `legacy-dxt/`、`scripts/build_bundles.sh`、`dist/*.dxt` 并恢复 README/忽略规则。

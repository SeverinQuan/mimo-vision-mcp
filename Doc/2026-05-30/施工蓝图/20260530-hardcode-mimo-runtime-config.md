# Code Change Log

## 时间
- 日期: 2026-05-30
- 任务: 将 MiMo Base URL 和 Model 固定写入 MCPB/DXT manifest，避免客户端未展开 user_config 导致启动失败

## 变更摘要
- 在新版 MCPB `manifest.json` 中固定 `MIMO_BASE_URL` 与 `MIMO_MODEL`。
- 在旧版 DXT `legacy-dxt/manifest.json` 中同步固定相同运行时环境变量。
- 移除安装阶段的 Base URL / Model 用户配置项，安装界面只需要填写 MiMo API Key。
- 更新中英文 README 与 Release Notes，说明 Base URL / Model 已由安装包固定。
- 重新构建 MCPB 与 DXT 发布产物。

## 影响文件
- `manifest.json`: 固定 MiMo 运行时配置并移除可选 user_config。
- `legacy-dxt/manifest.json`: 固定旧版 DXT 运行时配置并移除可选 user_config。
- `README.md`: 更新中英文安装说明与环境变量表。
- `RELEASE_NOTES.md`: 更新安装提示与变更摘要。
- `dist/mimo-vision-mcp-1.0.0.mcpb`: 重新构建 MCPB 产物。
- `dist/mimo-vision-mcp-1.0.0.dxt`: 重新构建 DXT 产物。

## 验证
- 执行命令: `python3 -m json.tool manifest.json >/dev/null && python3 -m json.tool legacy-dxt/manifest.json >/dev/null`
- 结果: 通过
- 执行命令: `bash scripts/build_bundles.sh`
- 结果: 通过；MCPB 与 DXT 均重新生成。pip 输出了宿主环境已有 FastAPI/Starlette 版本冲突提示，但依赖安装目标是 `legacy-dxt/server/lib`，构建未失败。

## 风险与回滚
- 风险: 安装包不再暴露自定义 Base URL / Model 输入项；如未来需要切换模型，需要重新发包或手动 MCP 配置覆盖。
- 回滚: `git revert <本次提交>`，或恢复 `manifest.json` 与 `legacy-dxt/manifest.json` 中的 `user_config` 占位符配置。

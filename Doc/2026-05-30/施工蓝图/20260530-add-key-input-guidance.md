# Code Change Log

## 时间
- 日期: 2026-05-30
- 任务: 在 MiMo API Key 配置旁增加示例填写规范

## 变更摘要
- 在 MCPB 与 DXT manifest 的 `MiMo API Key` 描述中写入填写规范。
- 在 README 的中英文安装步骤中补充只填写原始 Key 值的说明。
- 在 Release Notes 中同步安装提示。
- 重新构建 MCPB 与 DXT 产物，确保安装包内包含新的配置说明。

## 影响文件
- `manifest.json`: 更新 `mimo_api_key.description`。
- `legacy-dxt/manifest.json`: 更新旧版 DXT 的 `mimo_api_key.description`。
- `README.md`: 增加中英文 Key 示例填写规范。
- `RELEASE_NOTES.md`: 增加 Release 安装填写提示。
- `dist/mimo-vision-mcp-1.0.0.mcpb`: 重新构建 MCPB 产物。
- `dist/mimo-vision-mcp-1.0.0.dxt`: 重新构建 DXT 产物。

## 验证
- 执行命令: `python3 -m json.tool manifest.json >/dev/null && python3 -m json.tool legacy-dxt/manifest.json >/dev/null`
- 结果: 通过
- 执行命令: `bash scripts/build_bundles.sh`
- 结果: 通过；MCPB 与 DXT 均重新生成。pip 输出宿主环境 FastAPI/Starlette 版本冲突提示，但依赖安装目标为 `legacy-dxt/server/lib`，构建成功。

## 风险与回滚
- 风险: 无运行逻辑变更，仅调整安装提示和发布产物。
- 回滚: `git revert <本次提交>`，或恢复 manifest/文档中的 Key 描述文本后重新构建。

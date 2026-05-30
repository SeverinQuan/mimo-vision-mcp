# Code Change Log

## 时间
- 日期: 2026-05-30
- 任务: 在 README 中补充依赖环境说明

## 变更摘要
- 新增英文 `Runtime Requirements` 小节，说明客户端兼容性、Python runtime、Python 依赖与构建工具。
- 新增中文 `依赖环境` 小节，覆盖 MCPB、DXT、源码安装三种使用方式。
- 明确最低 Python 版本为 `3.8.0`，并说明服务端不依赖 Python `mcp` 包。

## 影响文件
- `README.md`: 增加中英文依赖环境说明。

## 验证
- 执行命令: `sed -n '80,150p' README.md && sed -n '430,520p' README.md`
- 结果: 通过；确认新增小节已写入中英文 README 区域。
- 执行命令: `git diff -- README.md`
- 结果: 通过；确认只修改 README 文档内容。

## 风险与回滚
- 风险: 无运行逻辑变更，仅文档更新。
- 回滚: `git revert <本次提交>` 或手动删除 README 新增小节。

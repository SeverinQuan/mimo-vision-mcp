# Code Change Log

## 时间
- 日期: 2026-05-30
- 任务: 增加 GitHub Release 自动发布流程

## 变更摘要
- 新增 GitHub Actions workflow，在推送 `v*` tag 时创建 Release。
- Release 自动上传 MCPB 与 DXT 两个安装包。
- 新增 `RELEASE_NOTES.md` 作为 Release 正文。

## 影响文件
- `.github/workflows/release.yml`: 定义 tag 触发的 Release 发布流程。
- `RELEASE_NOTES.md`: 定义 v1.0.1-dual Release 说明。
- `Doc/2026-05-30/施工蓝图/20260530-github-release-workflow.md`: 本次施工记录。

## 验证
- 执行命令: `git diff --check`
- 结果: 待执行。
- 执行命令: `git push origin legacy-dxt-compatible v1.0.1-dual`
- 结果: 待执行，执行后由 GitHub Actions 创建 Release。

## 风险与回滚
- 风险: 依赖 GitHub Actions 可用性和仓库 Actions 权限；若 Actions 被禁用，Release 不会自动创建。
- 风险: Release 使用未签名的 `.mcpb` 与 `.dxt` 产物。
- 回滚: 删除 `.github/workflows/release.yml` 与 `RELEASE_NOTES.md`，或删除对应 tag/release。

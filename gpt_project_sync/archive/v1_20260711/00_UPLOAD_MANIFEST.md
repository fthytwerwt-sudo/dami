# GPT Project 同步包上传清单

## 包信息

- `package_version`: `v1_20260711`
- `generated_at`: `2026-07-11`
- `source_repo`: `fthytwerwt-sudo/dami`
- `source_commit`: `f2eb1b440fc2c5cc9dc22cee716022e56c9f3988`
- `status`: `gpt_project_sync_package_generated_pending_user_upload`
- `ui_uploaded`: `false`

## 上传方式

1. 将 `01_GPT_PROJECT_INSTRUCTIONS.md` 的内容粘贴到 ChatGPT Project Instructions。
2. 将 `02_PROJECT_COLLABORATION_SYSTEM.md`、`03_SOURCE_OF_TRUTH_AND_HUMAN_GATES.md`、`04_CURRENT_PROJECT_STATE_SNAPSHOT.md` 和 `05_CODEX_HANDOFF_CONTRACT.md` 上传为 Project 文件。
3. 上传后由用户回读并确认指令与文件均可见。在确认前，不得声称 ChatGPT Project UI 已同步。

## 文件职责

| 文件 | 类型 | 职责 | 上传目标 |
| --- | --- | --- | --- |
| `01_GPT_PROJECT_INSTRUCTIONS.md` | 静态 | ChatGPT 的长期判断、对齐、下发和完成真实性规则 | Project Instructions |
| `02_PROJECT_COLLABORATION_SYSTEM.md` | 静态 | 四层架构、角色、激活机制与每轮闭环 | Project file |
| `03_SOURCE_OF_TRUTH_AND_HUMAN_GATES.md` | 静态 | 事实源、冲突裁决、人工闸门与公开仓库边界 | Project file |
| `04_CURRENT_PROJECT_STATE_SNAPSHOT.md` | 动态快照 | 从仓库正式 current 文件生成的当前状态摘要 | Project file |
| `05_CODEX_HANDOFF_CONTRACT.md` | 静态 | 将已对齐任务交给 Codex 时的最低完整契约 | Project file |
| `00_UPLOAD_MANIFEST.md` | 静态 | 上传顺序、包状态和文件职责说明 | Local/package reference |
| `package_manifest.json` | 静态 | 机器可读的包元数据、文件属性和校验值 | Local/package reference |

## 真实性声明

本包的生成只证明上传材料已准备。它不证明用户已上传、ChatGPT Project UI 已读取、规则已在 UI 生效，也不证明任何业务事实已获批。

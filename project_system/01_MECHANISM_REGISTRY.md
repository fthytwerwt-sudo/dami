# Formal Mechanism Registry v2

本注册表登记 M01—M28 的正式迁移裁决。它是路由索引，不要求每个任务全量运行。机器字段的完整来源是同名 JSON。

## Counts

- Total registered: `28`
- `ACTIVE_DIRECT`: `16`
- `ACTIVE_ADAPTED`: `9`
- `DEFERRED`: `0`
- `REJECTED_NOT_MIGRATED`: `3`

| ID | Name | Activation | Canonical rule |
| --- | --- | --- | --- |
| M01 | ChatGPT/Codex/user authority separation | `ACTIVE_DIRECT` | `rules/01_ROLES_AND_AUTHORITY.md` |
| M02 | Static rules/dynamic facts separation | `ACTIVE_DIRECT` | `rules/02_SOURCE_OF_TRUTH_AND_CONFLICT.md` |
| M03 | Source authority/conflict | `ACTIVE_DIRECT` | `rules/02_SOURCE_OF_TRUTH_AND_CONFLICT.md` |
| M04 | Cross-border task routing and state machine | `ACTIVE_ADAPTED` | `rules/11_路由判断与流程启动_route_decision_and_process_boot.md` |
| M05 | Six-layer requirement alignment | `ACTIVE_DIRECT` | `rules/03_REQUIREMENT_ALIGNMENT_AND_IMPLEMENTATION_DESIGN.md` |
| M06 | Ambiguous-goal clarification | `ACTIVE_DIRECT` | `rules/03_REQUIREMENT_ALIGNMENT_AND_IMPLEMENTATION_DESIGN.md` |
| M07 | Implementation design | `ACTIVE_DIRECT` | `rules/03_REQUIREMENT_ALIGNMENT_AND_IMPLEMENTATION_DESIGN.md` |
| M08 | Capability confirmation/probe separation | `ACTIVE_DIRECT` | `rules/03_REQUIREMENT_ALIGNMENT_AND_IMPLEMENTATION_DESIGN.md` |
| M09 | Primary/fallback/loss | `ACTIVE_DIRECT` | `rules/03_REQUIREMENT_ALIGNMENT_AND_IMPLEMENTATION_DESIGN.md` |
| M10 | Startup impact check | `ACTIVE_ADAPTED` | `rules/11_路由判断与流程启动_route_decision_and_process_boot.md` |
| M11 | Completion Relay | `ACTIVE_DIRECT` | `rules/16_完成接力与失败路由_completion_relay_and_failure_routes.md` |
| M12 | Completion truth | `ACTIVE_DIRECT` | `rules/16_完成接力与失败路由_completion_relay_and_failure_routes.md` |
| M13 | Four-state completion | `ACTIVE_ADAPTED` | `rules/16_完成接力与失败路由_completion_relay_and_failure_routes.md` |
| M14 | Git decision/validation fields | `ACTIVE_DIRECT` | `rules/08_GIT_AND_SYNC_TRUTH.md` |
| M15 | GPT Project sync truth | `ACTIVE_DIRECT` | `rules/08_GIT_AND_SYNC_TRUTH.md` |
| M16 | Original-source readback | `ACTIVE_ADAPTED` | `rules/14_供料与执行中补料_supply_and_mid_task_supply.md` |
| M17 | Dry-run and secret boundary | `ACTIVE_DIRECT` | `rules/05_EXECUTION_SAFETY_AND_HUMAN_GATES.md` |
| M18 | Cross-border human/AI boundary | `ACTIVE_ADAPTED` | `rules/05_EXECUTION_SAFETY_AND_HUMAN_GATES.md` |
| M19 | L0-L3 engineering depth | `ACTIVE_ADAPTED` | `rules/12_完整工程线_engineering_line.md` |
| M20 | Execution budget | `ACTIVE_DIRECT` | `rules/09_ENGINEERING_DEPTH_AND_COLLABORATION_EFFECTIVENESS.md` |
| M21 | Collaboration effectiveness | `ACTIVE_DIRECT` | `rules/09_ENGINEERING_DEPTH_AND_COLLABORATION_EFFECTIVENESS.md` |
| M22 | Research Source-to-Action | `ACTIVE_ADAPTED` | `rules/14_供料与执行中补料_supply_and_mid_task_supply.md` |
| M23 | Single-primary-variable experiment | `ACTIVE_ADAPTED` | `rules/07_RESEARCH_TO_ACTION_AND_EXPERIMENTS.md` |
| M24 | Media-production workflows | `REJECTED_NOT_MIGRATED` | this registry |
| M25 | Fixed retrieval/external-AI dependency | `REJECTED_NOT_MIGRATED` | this registry |
| M26 | Legacy statuses, paths, conclusions | `REJECTED_NOT_MIGRATED` | this registry |
| M27 | Conditional Git closeout | `ACTIVE_ADAPTED` | `rules/08_GIT_AND_SYNC_TRUTH.md` |
| M28 | Latest/history separation | `ACTIVE_DIRECT` | `rules/08_GIT_AND_SYNC_TRUTH.md` |

## M19 v2 decision

M19 从 `DEFERRED` 改为 `ACTIVE_ADAPTED`。这激活工程深度路由、L0-L3、L3 的 13 层工程线和可执行验证；不代表每个任务都进入 L3。深度由价值、风险、重复度、状态/节点复杂度和维护成本决定。

## Rejection boundary

M24-M26 是长期负面边界：不迁移视频/TTS/剪辑/卡片等领域流程，不迁移固定 RAG 或外部 AI 供应商依赖，不迁移旧项目状态、路径或业务结论。它们保留为审计证据，不能进入 runtime prompt、current、默认工具或正式路径。

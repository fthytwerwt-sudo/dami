# 完整工程线（engineering line）

状态：`active`
适用机制：M19
适用习惯：H05-H08

## 深度路由

`L0_light_chat` 用于解释且不写正式文件；`L1_task_card` 用于小范围可逆任务；`L2_node_contract` 用于有稳定输入输出和验证的单节点；`L3_system_line` 仅在同时有状态、多节点、工具、评估、失败路由和长期运行价值时使用。用户说“直接做”不等于跳过判断。

## L3 的 13 层

```text
0 project_goal_layer（项目目标层）
1 current_task_awareness_layer（当前任务意识层）
2 process_node_layer（流程节点层）
3 cleaning_layer（清洗层）
4 structuring_layer（结构化层）
5 source_retrieval_layer（资料召回层）
6 tool_connection_layer（工具连接层）
7 execution_node_layer（执行节点层）
8 evaluation_layer（判断评估层）
9 failure_route_layer（失败路由层）
10 human_fallback_layer（人工兜底层）
11 state_record_layer（状态记录层）
12 retrospective_iteration_layer（复盘迭代层）
```

L3 必须有数据契约（Schema）、Evaluator（评估器）、Fixture、fail-closed 失败路由和记录；不得只画图、只列文件名或只生成说明。复杂任务至少完成工程线五问法，并用 `engineering_depth_router.py` 输出选择理由。

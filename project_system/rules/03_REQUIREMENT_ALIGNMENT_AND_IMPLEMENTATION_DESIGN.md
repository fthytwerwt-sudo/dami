# 需求对齐与实现设计

状态：`active`
适用机制：M05、M06、M07、M08、M09、M10

## 六层需求对齐

复杂、修改、研究、合规、方向、自动化或外部动作任务，在执行前必须对齐以下六层：

1. `Goal`：真实目标、表面请求、非目标。
2. `Context`：当前状态、已确认事实、候选与未知项。
3. `Source of truth`：正式入口、直接证据、适用范围与冲突。
4. `Constraints`：时间、成本、合规、隐私、文件范围、外部动作与人工闸门。
5. `Done when`：交付、验证证据、允许提升与不得提升的状态。
6. `Blocked if`：缺事实、冲突、权限、能力、回滚或合规证据时的明确阻断。

任一关键层模糊且会改变实现路线、外部后果或完成定义时，进入澄清闸门；可以安全推定且不扩大范围的事项，必须记录为 `assumption`。

## 实现设计

执行单至少记录：

- `confirmed_capabilities`
- `unverified_capabilities`
- `primary_route`
- `alternative_route`
- `alternative_loss`
- `capability_probe`
- `affected_files_or_systems`
- `external_accounts_or_paid_resources`
- `human_gates`
- `rollback`
- `validation`

能力探测与目标执行必须分开。未验证能力不得写成已具备；探测应使用最小、低风险、可逆范围。首选路线失败时，不得用替代路线的降级结果冒充原目标完成，必须报告替代损失。

## 启动报告与影响面检查

修改前检查：项目与仓库根、分支和工作树；允许与禁止路径；已有正式机制；未提交改动归属；事实源冲突；秘密和敏感数据；外部副作用；回滚条件。发现既有冲突、范围不明或无法隔离的脏改时，先阻断，不覆盖、不夹带。

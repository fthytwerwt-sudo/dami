# 真实获客最小闭环 V1 实施报告

status: `completed_code_ready_pending_real_target_authorization`

## 路由判断

- `task_type`: `code_or_automation`, `project_file_change`, `local_file_governance`, `audit`
- `engineering_depth`: `L3_system_line`
- `target_branch`: `codex/web-lead-minimal-loop-v1`
- `base_ref`: `origin/main`
- 写入范围：`.gitignore` 与 `tools/web_lead_agent/`
- 禁止范围：`AGENTS.md`、`project_system/current/`、正式业务决定、历史分支、`main`

## 已实现闭环

```text
获准的公开网页
→ 企业资料抓取
→ 结构化
→ 去重/评分
→ 产品知识检索
→ 个性化初稿
→ 确定性策略
→ 人工审批闸门
→ 一次受监督发送
→ 回执/页面结果
→ 状态保存
→ 强制停止
```

## 关键模块

- `contracts.py`: 数据契约、运行模式和回执状态。
- `discovery.py` / `extract.py`: 白名单域名、公开页面安全探测、HTML 字段/表单解析。
- `normalize.py` / `scoring.py`: 企业资料结构化、去重和确定性评分。
- `knowledge.py`: SQLite 产品知识库检索，支持 `FOUND` / `MISSING` / `CONFLICT`。
- `drafting.py`: 模板草稿生成，只使用已检索知识。
- `policy.py`: 确定性策略；价格、MOQ、健康/医疗、低 GI、认证、合同等词进入复核或阻断。
- `approval.py`: 人工审批 payload 必须同时满足目标、通道、账号、消息、`send_limit=1` 和动作确认。
- `idempotency.py`: 同一目标、表单和消息只允许一次提交。
- `runtime.py`: SQLite 运行状态、事件、回执、发送次数保存。
- `channels/website_contact_form.py`: 公开网页联系表单适配器；不登录、不保存 Cookie、不自动重试。
- `workflow.py`: LangGraph `StateGraph`，在人工审批节点支持 `interrupt` / `resume`，可使用 SQLite checkpointer。

## 开源依赖复用

- `langgraph==1.2.9`: 用作可恢复状态图和 human-in-the-loop 工作流。官方文档说明 `interrupt` 可暂停图并等待外部输入，persistence 可保存图状态。
- `langgraph-checkpoint-sqlite==3.1.0`: SQLite checkpoint。
- `jsonschema==4.26.0`: JSON Schema 校验。
- `PyYAML==6.0.3`: YAML 配置读取。
- `pytest==9.1.1`: 测试运行。

参考来源：

- [LangGraph interrupts](https://docs.langchain.com/oss/python/langgraph/interrupts)
- [LangGraph persistence](https://docs.langchain.com/oss/python/langgraph/persistence)
- [LangGraph GitHub / license](https://github.com/langchain-ai/langgraph)
- [jsonschema documentation](https://python-jsonschema.readthedocs.io/en/stable/validate/)
- [PyYAML GitHub / license](https://github.com/yaml/pyyaml)
- [pytest license](https://docs.pytest.org/en/stable/license.html)

## 发送状态

- 真实外部发送：`0`
- 合成本地 POST：`1`，仅用于 fixture E2E，不代表业务动作。
- 最高可提升状态：`completed_code_ready_pending_real_target_authorization`
- 不提升为：`real_lead_sent`、`customer_contacted`、`business_validated`

## 待授权项

进入真实目标前还需要用户逐项授权：

1. 获准公开网页 URL。
2. 可使用的平台账号或发送账号。
3. 产品事实和允许表达范围。
4. 最终消息正文。
5. 本轮只发送一次的明确批准。

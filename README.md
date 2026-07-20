# 大米低 GI 网页获客工具底座

这是一个独立的技术工具仓库，用纯合成数据验证：公开网页读取、企业结构化、去重评分、来源约束知识召回、确定性政策闸门、LangGraph 人工中断/恢复、DOM 填入和提交前阻断。

它不是业务事实源，也不代表已选择市场、渠道、产品、价格或健康宣称。当前唯一启用模式是 `draft_only`；本地沙箱只模拟一次人工批准，最终仍返回 `send_status=BLOCKED`。

## 安全边界

- 只允许 `localhost` 网页；不读取真实企业或客户。
- 不登录账号，不处理验证码，不使用反检测、截图坐标或隐藏 API。
- 不包含真实提交、邮件或消息发送实现。
- 不需要 API key，不调用付费模型或外部服务。
- `runtime_data/`、SQLite、JSONL、浏览器缓存和 `.env*` 不进入 Git。

## 安装

需要 Python 3.12。依赖版本由 `pyproject.toml` 和 `requirements.lock` 固定。

```bash
python3.12 -m venv .venv
.venv/bin/python -m pip install '.[dev]'
.venv/bin/python -m playwright install chromium
```

## 验证

```bash
.venv/bin/pytest -q
.venv/bin/python -m web_agent_toolkit.sandbox --output runtime_data/sandbox_run
```

沙箱预期结尾：

```json
{
  "stage": "FILLED_PENDING_SUBMIT",
  "send_status": "BLOCKED",
  "deduplicated_lead_count": 1
}
```

运行输出在 `runtime_data/sandbox_run/`，包括业务状态、LangGraph checkpoint 和 `trace.jsonl`；该目录默认忽略。

## 统一接口

代码公开定义或实现：`crawl_page`、`extract_company`、`normalize_lead`、`score_lead`、`retrieve_knowledge`、`generate_draft`、`evaluate_policy`、`request_approval`、`fill_web_form`、`submit_message`、`read_result`、`save_checkpoint`、`resume_run`、`stop_run`。

底层替换点在 `contracts.py` 的 Protocol 和 `config/tool_registry.yaml`。未来真实平台 Adapter 必须单独授权、单独测试，并继续保留政策与人工闸门。

## 文档导航

- `docs/01_开源项目选型_open_source_selection.md`：候选矩阵、证据、许可证和自建证明。
- `docs/02_组合架构_composed_architecture.md`：两套架构、唯一推荐、数据流和回滚。
- `docs/03_知识库契约_knowledge_contract.md`：知识域、来源、冲突和过期规则。
- `docs/04_客户对话边界_conversation_policy.md`：客户状态、政策和人工权限。
- `docs/05_LangGraph流程蓝图_langgraph_blueprint.md`：State/Node/Edge/interrupt/retry/resume。
- `docs/06_Runtime运行时契约_runtime_contract.md`：checkpoint、幂等、Trace、费用和终止条件。
- `docs/07_未来定制规划_customization_blueprint.md`：产品、市场、客户、Prompt、工具升级路线。
- `reports/00_执行报告_execution_report.md`：Route decision、测试和 Git 真实性。

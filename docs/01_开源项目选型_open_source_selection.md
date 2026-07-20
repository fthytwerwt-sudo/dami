# 开源项目选型与复用证明

## 1. 结论和证据口径

调研快照日期为 2026-07-21。只把官方仓库、LICENSE、Release、Security/Docs 当直接证据；没有逐项核准 tag/HEAD 的条目显式写 `待验证`，不把搜索摘要升级为事实。

唯一推荐是“轻量组合 A”：`Playwright Python + SQLite + LangGraph/SQLite checkpointer + JSON Schema + 自有薄 Adapter/确定性政策`。这不是从零造平台：浏览器、状态图、checkpoint 和 Schema 全部复用开源包，自建仅限跨项目胶水、业务边界和可替换接口。

已确认版本证据：Playwright 上游 [v1.61.1](https://github.com/microsoft/playwright/releases/tag/v1.61.1)（Python 包实际安装 1.61.0）、LangGraph [1.2.9](https://github.com/langchain-ai/langgraph/releases/tag/1.2.9)、Crawl4AI [v0.9.2](https://github.com/unclecode/crawl4ai/releases/tag/v0.9.2)、Chroma [1.5.9](https://github.com/chroma-core/chroma/releases/tag/1.5.9)、OpenTelemetry Python [v1.36.0](https://github.com/open-telemetry/opentelemetry-python/releases/tag/v1.36.0)。

## 2. 能力覆盖检查

| 能力 | 至少 3—5 个候选 |
|---|---|
| 网页抓取/正文 | Scrapy、Crawlee、Firecrawl、Crawl4AI、changedetection.io、Trafilatura |
| 结构化/自然语言提取 | Crawl4AI、Firecrawl、ScrapeGraphAI、Maxun、GPT Researcher |
| DOM 交互 | Playwright、Puppeteer、Selenium、Crawlee、browser-use |
| 企业清洗 | OpenRefine、dedupe、Splink、Pandas、RecordLinkage |
| 知识/RAG | LangChain、LlamaIndex、Haystack、RAGFlow、AnythingLLM、Dify |
| 向量数据库 | Chroma、Qdrant、Weaviate、pgvector、Milvus |
| 工作流/Runtime | LangGraph、Temporal、Prefect、Dagster、Windmill、Activepieces、n8n |
| 客户状态/人工审核 | Chatwoot、Twenty、Baserow、NocoDB、Grist |
| 多渠道/营销 | Mautic、listmonk、Chatwoot、n8n、Activepieces |
| 可观测/评估 | OpenTelemetry、Langfuse、Phoenix、DeepEval、Ragas |

## 3. 复用评估字段 Profile

下表是每个项目行必须继承的工程字段，避免在 50 行矩阵里重复同一组文字。

| Profile | self_hosting / programmatic_interface | input_output | required_dependencies / model_dependency / external_service_dependency | setup / integration / replacement | export / platform / privacy / maintenance cost |
|---|---|---|---|---|
| `LIB` | 是；Python/JS API | 本地对象/文件 → 结构化对象 | 语言运行时；模型通常无；外部服务无 | 低/低/低 | 高/低/低/低 |
| `BROWSER` | 是；浏览器 API | URL+DOM 契约 → 页面/动作证据 | 浏览器二进制；模型无；目标网页 | 中/中/低（经 Adapter） | 高/中/中/中 |
| `MODEL_LIB` | 是；SDK/API | 文档/Prompt → 抽取/RAG/Agent 结果 | Python/Node；模型常为可选或必需；模型服务可能存在 | 中/中/中 | 中高/中/中高/中 |
| `PLATFORM` | 是；REST/Webhook/UI | 多源数据 → 工作流/知识/消息 | 容器、数据库、队列；常依赖模型/外部连接 | 高/高/高 | 中/高/高/高 |
| `DATABASE` | 是；SQL/HTTP/gRPC | 向量/文档 → 近邻结果 | 服务或数据库扩展；embedding 外置；外部服务无 | 中高/中/中 | 高/中/中/中 |
| `DURABLE` | 是；SDK/API | 任务/事件 → 可恢复状态 | 服务、数据库/worker；模型无；外部服务无 | 高/高/中高 | 高/中高/中/高 |
| `CRM` | 是；REST/Webhook/UI | 联系人/会话/阶段 → 任务/历史 | Web 服务、数据库、消息通道；模型非必要 | 高/高/高 | 中高/高/高/高 |
| `OBS` | 是；SDK/OTLP/API | trace/eval 数据 → 指标/界面 | collector/数据库或 SDK；模型评估可能需要；外部服务可选 | 中高/中/中 | 高/中/中高/中高 |

## 4. 候选矩阵

`latest_commit` 记录调研时可确认的维护判断；没有在本轮逐 SHA 回读的条目写 `待验证`。商业边界是工程初筛，不是法律意见。

### 4.1 网页抓取、结构化、DOM 和企业清洗

| project_name / repository_url | capability | maintenance_status | latest_release | latest_commit | license / commercial_use_boundary | Profile | pilot_fit / future_fit | adoption_mode | rejection_reason |
|---|---|---|---|---|---|---|---|---|---|
| [Playwright](https://github.com/microsoft/playwright) | Chromium/WebKit/Firefox 自动化 | 活跃 | v1.61.1；Python 1.61.0 | 2026-07 活跃 | Apache-2.0；遵守目标站条款 | BROWSER | 高/高 | `package_dependency` | 已采用；只允许 localhost 和提交前停止 |
| [Puppeteer](https://github.com/puppeteer/puppeteer) | Chrome DOM 自动化 | 活跃 | 待验证 | 待验证 | Apache-2.0 | BROWSER | 中/中 | `reference_only` | Python 主栈不匹配，能力与 Playwright 重叠 |
| [Selenium](https://github.com/SeleniumHQ/selenium) | WebDriver 浏览器自动化 | 活跃 | 待验证 | 待验证 | Apache-2.0 | BROWSER | 中/中 | `reference_only` | 本地契约下 Playwright locator 和上下文更直接 |
| [Crawlee](https://github.com/apify/crawlee) | 抓取队列、浏览器爬取 | 活跃 | 待验证 | 待验证 | Apache-2.0；云服务可选 | BROWSER | 中/高 | `recheck_later` | Node/队列引入超出当前单页沙箱 |
| [Scrapy](https://github.com/scrapy/scrapy) | 高吞吐静态抓取 | 活跃 | 待验证 | 待验证 | BSD-3-Clause | LIB | 中/高 | `recheck_later` | JS/DOM 不是主能力；本轮没有批量任务 |
| [Firecrawl](https://github.com/mendableai/firecrawl) | 网页转 Markdown/JSON | 活跃 | 待验证 | 待验证 | AGPL/云服务边界需逐版本复核 | PLATFORM | 中/中 | `recheck_later` | 服务与许可/外部依赖比本地沙箱重 |
| [Crawl4AI](https://github.com/unclecode/crawl4ai) | LLM 友好抓取与抽取 | 活跃 | v0.9.2 | 2026-07 活跃 | LICENSE 含额外 attribution/branding；需法律复核 | MODEL_LIB | 中/高 | `recheck_later` | [v0.8.7](https://github.com/unclecode/crawl4ai/releases/tag/v0.8.7) 曾修 RCE/SSRF 等，且许可不是纯净基线 |
| [ScrapeGraphAI](https://github.com/ScrapeGraphAI/Scrapegraph-ai) | 自然语言抽取图 | 活跃度待验证 | 待验证 | 待验证 | MIT；模型/Provider 条款另计 | MODEL_LIB | 中/中 | `reference_only` | 模型依赖，不满足无 key 基础测试 |
| [Maxun](https://github.com/getmaxun/maxun) | 无代码网页数据/机器人 | 活跃度待验证 | 待验证 | 待验证 | AGPL/商业边界需复核 | PLATFORM | 低/中 | `recheck_later` | 平台过重，当前只需代码 Adapter |
| [changedetection.io](https://github.com/dgtlmoon/changedetection.io) | 网页变化监测 | 活跃 | 待验证 | 待验证 | Apache-2.0 | PLATFORM | 低/中 | `reference_only` | 监测而非企业抽取/对话主链路 |
| [Trafilatura](https://github.com/adbar/trafilatura) | 正文/元数据抽取 | 活跃 | 待验证 | 待验证 | Apache-2.0 | LIB | 中/高 | `recheck_later` | 当前合成页 DOM 已足够，未来静态正文优先候选 |
| [browser-use](https://github.com/browser-use/browser-use) | LLM 浏览器 Agent | 活跃 | 待验证 | 待验证 | MIT；模型条款另计 | MODEL_LIB | 低/中 | `reject` | 自主 Agent、模型和浏览器攻击面超出确定性 DOM 契约 |
| [GPT Researcher](https://github.com/assafelovic/gpt-researcher) | 多源研究 Agent | 活跃度待验证 | 待验证 | 待验证 | Apache-2.0；模型/搜索服务另计 | MODEL_LIB | 低/低 | `reference_only` | 面向研究报告，不是网页获客执行层 |
| [OpenRefine](https://github.com/OpenRefine/OpenRefine) | 交互式清洗/聚类 | 活跃 | 待验证 | 待验证 | BSD-3-Clause | PLATFORM | 低/中 | `reference_only` | UI/Java 服务，不适合嵌入式确定性 pipeline |
| [dedupe](https://github.com/dedupeio/dedupe) | 机器学习实体去重 | 活跃度待验证 | 待验证 | 待验证 | MIT | LIB | 中/高 | `recheck_later` | 当前根域名规则足够；需有标注数据后再引入 |
| [Splink](https://github.com/moj-analytical-services/splink) | 概率实体链接 | 活跃 | 待验证 | 待验证 | MIT | LIB | 低/高 | `recheck_later` | 当前数据量不值得引入统计模型和列式引擎 |

### 4.2 知识库、RAG 和向量数据库

| project_name / repository_url | capability | maintenance_status | latest_release | latest_commit | license / commercial_use_boundary | Profile | pilot_fit / future_fit | adoption_mode | rejection_reason |
|---|---|---|---|---|---|---|---|---|---|
| [LangChain](https://github.com/langchain-ai/langchain) | Loader/Retriever/Agent 基线 | 活跃 | langchain-core 1.4.9 | 2026-07 活跃 | MIT；Provider 条款另计 | MODEL_LIB | 中/高 | `reference_only` | 全套抽象过重；仅作为 LangGraph 传递 core，不主动绑定平台 |
| [LlamaIndex](https://github.com/run-llama/llama_index) | 数据连接、索引、RAG | 活跃 | 待验证 | 待验证 | MIT | MODEL_LIB | 中/高 | `recheck_later` | 当前结构化知识无分块/embedding 需求 |
| [Haystack](https://github.com/deepset-ai/haystack) | RAG Pipeline/评估 | 活跃 | 待验证 | 待验证 | Apache-2.0 | MODEL_LIB | 中/高 | `recheck_later` | Pipeline 和模型依赖超出轻量试点 |
| [RAGFlow](https://github.com/infiniflow/ragflow) | 完整 RAG 平台 | 活跃 | v0.26.4 | 待验证 | Apache-2.0 | PLATFORM | 低/中 | `reference_only` | 容器、数据库、模型和运维面过重 |
| [AnythingLLM](https://github.com/Mintplex-Labs/anything-llm) | 桌面/服务知识对话 | 活跃度待验证 | 待验证 | 待验证 | MIT；集成服务条款另计 | PLATFORM | 低/中 | `reference_only` | UI 产品，不是可替换事实层契约 |
| [Dify](https://github.com/langgenius/dify) | LLM App/RAG/Workflow 平台 | 活跃 | 1.16.0 | 待验证 | modified Apache；多租户/标识限制 | PLATFORM | 低/中 | `reject` | 许可附加条件和平台锁定不适合首层底座 |
| [Flowise](https://github.com/FlowiseAI/Flowise) | 可视化 LLM Flow | 活跃度待验证 | 待验证 | 待验证 | Apache-2.0；组件 Provider 另计 | PLATFORM | 低/中 | `reference_only` | Node 平台和 UI 状态会形成第二事实源 |
| [Langflow](https://github.com/langflow-ai/langflow) | 可视化 Agent/RAG Flow | 活跃 | 待验证 | 待验证 | MIT | PLATFORM | 低/中 | `reference_only` | 当前流程需代码审计和确定性测试，不需可视化搭建器 |
| [Chroma](https://github.com/chroma-core/chroma) | 向量存储 | 活跃 | 1.5.9 | 2026 活跃 | Apache-2.0 | DATABASE | 低/高 | `recheck_later` | 太早引入 embedding、索引迁移和备份成本 |
| [Qdrant](https://github.com/qdrant/qdrant) | 向量数据库 | 活跃 | 待验证 | 待验证 | Apache-2.0 | DATABASE | 低/高 | `recheck_later` | 当前 4 条结构化知识无需服务化向量库 |
| [Weaviate](https://github.com/weaviate/weaviate) | 向量数据库/混合检索 | 活跃 | 待验证 | 待验证 | BSD-3-Clause；模块服务另计 | DATABASE | 低/高 | `recheck_later` | 服务和模块较重 |
| [pgvector](https://github.com/pgvector/pgvector) | PostgreSQL 向量扩展 | 活跃 | 待验证 | 待验证 | PostgreSQL License | DATABASE | 中/高 | `recheck_later` | 未来若已有 PostgreSQL 优先；本轮 SQLite 足够 |
| [Milvus](https://github.com/milvus-io/milvus) | 分布式向量数据库 | 活跃 | 待验证 | 待验证 | Apache-2.0 | DATABASE | 低/中 | `reject` | 分布式运维远超当前规模 |

### 4.3 Agent、Durable Runtime 和工作流

| project_name / repository_url | capability | maintenance_status | latest_release | latest_commit | license / commercial_use_boundary | Profile | pilot_fit / future_fit | adoption_mode | rejection_reason |
|---|---|---|---|---|---|---|---|---|---|
| [LangGraph](https://github.com/langchain-ai/langgraph) | StateGraph/interrupt/checkpoint | 活跃 | 1.2.9 | 2026-07 活跃 | MIT；本地 OSS 能力 | MODEL_LIB | 高/高 | `package_dependency` | 已采用最小 OSS 库，不使用 LangGraph Platform |
| [Temporal](https://github.com/temporalio/temporal) | Durable Execution | 活跃 | 待验证 | 待验证 | MIT；Cloud 可选 | DURABLE | 低/高 | `recheck_later` | 服务和 worker 运维不适合单机试点 |
| [Prefect](https://github.com/PrefectHQ/prefect) | Python 工作流编排 | 活跃 | 待验证 | 待验证 | Apache-2.0；Cloud 可选 | DURABLE | 低/中 | `reference_only` | 数据流调度强，但人审对话图不如 LangGraph 直接 |
| [Dagster](https://github.com/dagster-io/dagster) | 数据资产/编排 | 活跃 | 待验证 | 待验证 | Apache-2.0 core；Cloud 另计 | DURABLE | 低/低 | `reference_only` | 面向数据平台而非逐客户会话 |
| [Windmill](https://github.com/windmill-labs/windmill) | 脚本/工作流平台 | 活跃度待验证 | 待验证 | 待验证 | AGPL/enterprise 边界需复核 | PLATFORM | 低/中 | `recheck_later` | 平台、权限和 secret 运维超出本轮 |
| [Activepieces](https://github.com/activepieces/activepieces) | 集成自动化 | 活跃 | 待验证 | 待验证 | MIT core/enterprise 边界需逐目录复核 | PLATFORM | 低/中 | `reference_only` | connectors/secrets 面过大，审批不是业务事实闸门 |
| [n8n](https://github.com/n8n-io/n8n) | 集成工作流 | 活跃 | 2.30.8 | 待验证 | Sustainable Use；enterprise 目录另计 | PLATFORM | 低/中 | `reject` | 非 OSI 基线、secret hub 和平台锁定 |

### 4.4 CRM、多渠道、审批、可观测和评估

| project_name / repository_url | capability | maintenance_status | latest_release | latest_commit | license / commercial_use_boundary | Profile | pilot_fit / future_fit | adoption_mode | rejection_reason |
|---|---|---|---|---|---|---|---|---|---|
| [Chatwoot](https://github.com/chatwoot/chatwoot) | 多渠道客服/会话 | 活跃 | 4.16.0 | 待验证 | MIT core + enterprise 专有目录 | CRM | 低/高 | `reference_only` | 未来可作 Channel Adapter，当前不存真实会话 |
| [Twenty](https://github.com/twentyhq/twenty) | 开源 CRM | 活跃 | 2.22.0 | 待验证 | mixed/copyleft/商业边界需复核 | CRM | 低/高 | `recheck_later` | 许可和部署面未过闸门 |
| [Baserow](https://github.com/bramw/baserow) | 数据库式业务台 | 活跃 | 待验证 | 待验证 | MIT core + premium 边界 | CRM | 中/中 | `reference_only` | 可做人工队列原型，但不能成为事实源 |
| [NocoDB](https://github.com/nocodb/nocodb) | 数据库 UI/协作 | 活跃 | 待验证 | 待验证 | 许可/enterprise 边界需复核 | CRM | 中/中 | `recheck_later` | UI 平台并非必要；本轮 SQLite 足够 |
| [Grist](https://github.com/gristlabs/grist-core) | 表格式业务数据 | 活跃 | 待验证 | 待验证 | Apache-2.0 core；enterprise/hosted 另计 | CRM | 中/中 | `reference_only` | 适合人工队列参考，当前不引入服务 |
| [Mautic](https://github.com/mautic/mautic) | 营销自动化 | 活跃 | 待验证 | 待验证 | GPL-3.0 | CRM | 低/中 | `reject` | 面向真实营销发送，违反本轮无外发边界 |
| [listmonk](https://github.com/knadh/listmonk) | 邮件列表/发送 | 活跃 | 待验证 | 待验证 | AGPL-3.0 | CRM | 低/低 | `reject` | 核心是批量外发，本轮明确禁止 |
| [OpenTelemetry Python](https://github.com/open-telemetry/opentelemetry-python) | 标准 Trace/Metrics | 活跃 | 1.36.0 | 2026-07 活跃 | Apache-2.0 | OBS | 中/高 | `recheck_later` | 当前 JSONL 足够；未来第一优先观测 Adapter |
| [Langfuse](https://github.com/langfuse/langfuse) | LLM Trace/Eval UI | 活跃 | 3.222.0 | 待验证 | MIT core + enterprise 专有目录 | OBS | 低/中 | `reference_only` | 平台、数据库和 mixed license 超出本轮 |
| [Phoenix](https://github.com/Arize-ai/phoenix) | LLM Trace/Eval | 活跃 | 待验证 | 待验证 | Elastic-2.0/组件边界需逐版本复核 | OBS | 低/中 | `recheck_later` | 服务化界面与数据治理成本偏高 |
| [DeepEval](https://github.com/confident-ai/deepeval) | LLM 单测/评估 | 活跃 | 待验证 | 待验证 | Apache-2.0；Cloud 可选 | MODEL_LIB | 中/高 | `recheck_later` | 当前为确定性 Fake Draft，无模型质量评估需求 |
| [Ragas](https://github.com/explodinggradients/ragas) | RAG 评估 | 活跃 | 待验证 | 待验证 | Apache-2.0 | MODEL_LIB | 中/高 | `recheck_later` | 等真实授权语料和 RAG 基线后再引入 |

## 5. 自建证明 Build justification

| 自建薄层 | 已搜索/不满足的直接证据 | 为什么 Adapter 仍需自有代码 | 最小范围/维护成本 | 未来替换/人工复审点 |
|---|---|---|---|---|
| `contracts.py` | 各项目 I/O、状态和许可证不同 | 上层不能直接绑定 Playwright/LangGraph/CRM | 5 个 dataclass + Protocol；低 | 兼容 Protocol 即可替换；用户确认正式字段 |
| `lead.py` | OpenRefine/dedupe/Splink 面向 UI、概率或大数据 | 本轮规则只有根域名合并和显式评分 | 3 个纯函数；低 | 数据量/误差达到阈值后换 dedupe/Splink |
| `knowledge.py` | LangChain/LlamaIndex/Haystack/RAG 平台均带不必要抽象或模型 | 需要 4 条结构化 Fixture、来源/冲突 fail-closed | SQLite 表+token 检索；低 | KnowledgeAdapter 可换 pgvector/Haystack |
| `policy.py` | 通用 Agent/LLM 不能决定项目商业/合规权限 | 价格、MOQ、低 GI 等必须确定性硬闸门 | 规则表+来源拼接；中（规则需治理） | 用户批准政策版本后接规则引擎；模型不可覆盖 |
| `runtime.py` glue | LangGraph 已提供 checkpoint；Temporal/Prefect 过重 | 仍需业务可读状态、stop 和 JSONL Trace | SQLite/JSONL Adapter；低 | RuntimeAdapter 换 Temporal/Postgres，Trace 换 OTel |
| `workflow.py` glue | LangGraph 提供图能力但不了解本项目人工边界 | 需把知识、政策、审批、DOM 连接并确保不发送 | 7 节点最小图；中 | 节点通过 Adapter 替换；用户确认 supervised 才扩展 |

无法通过“零代码配置”解决的是项目特定的授权、状态语义、来源冲突和发送禁令；因此自建严格限制在边界胶水，不复制第三方源码，不实现浏览器引擎、向量库、Durable Engine、CRM 或可观测平台。

## 6. 许可与安全红线

- `Crawl4AI`：必须先完成许可证和安全复核；不启用远程 Docker API、登录、代理、stealth 或验证码能力。
- `Dify`、`n8n`、`Langfuse`、`Chatwoot`、`Twenty`：不得把“可见源码”写成“可自由商用”；采用前逐目录/版本审查。
- 所有容器未来锁 digest，Git 依赖锁 commit，Python 包锁 exact version。
- 技术可运行不代表目标站条款允许；真实域名 allowlist 和平台条款是独立人工闸门。

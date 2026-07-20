"""纯合成端到端沙箱命令。"""

from __future__ import annotations

import argparse
import json
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from threading import Thread

from langgraph.types import Command

from .knowledge import SQLiteKnowledgeAdapter
from .lead import deduplicate_leads, normalize_lead, score_lead
from .policy import DeterministicPolicyGate
from .runtime import JsonlTraceRecorder, SQLiteRuntimeStore
from .web import PlaywrightWebAdapter
from .workflow import build_conversation_graph


class _QuietHandler(SimpleHTTPRequestHandler):
    """关闭本地沙箱 HTTP 访问日志。"""

    def log_message(self, format: str, *args: object) -> None:  # noqa: A002
        return


def run_sandbox(output_dir: Path, fixtures_dir: Path) -> dict[str, object]:
    """运行中断/恢复闭环，并返回提交前状态。"""

    output_dir.mkdir(parents=True, exist_ok=True)
    handler = partial(_QuietHandler, directory=str(fixtures_dir))
    server = ThreadingHTTPServer(("127.0.0.1", 0), handler)
    thread = Thread(target=server.serve_forever, daemon=True)
    thread.start()
    runtime = SQLiteRuntimeStore(output_dir / "runtime.sqlite")
    knowledge = SQLiteKnowledgeAdapter(output_dir / "knowledge.sqlite")
    knowledge.replace_all(
        json.loads((fixtures_dir / "synthetic_knowledge.json").read_text(encoding="utf-8"))
    )
    config = {"configurable": {"thread_id": "sandbox-thread-1"}}
    url = f"http://127.0.0.1:{server.server_port}/synthetic_company.html"
    try:
        web = PlaywrightWebAdapter()
        page_evidence = web.crawl_page(url)
        company = web.extract_company(
            url,
            {
                "company_name": "company-name",
                "country": "country",
                "buyer_type_candidate": "business-type",
                "category_evidence": "category",
            },
        )
        lead = normalize_lead(
            {
                **company,
                "company_name_raw": company["company_name"],
                "root_domain": "localhost.synthetic",
                "source_url": url,
                "source_type": "synthetic_local_site",
                "import_distribution_evidence": "synthetic_distribution_statement",
                "channel_fit_evidence": "synthetic_retail_channel",
                "public_contact_type": "local_test_form",
            }
        )
        deduped = deduplicate_leads([lead, dict(lead)])
        lead_score = score_lead(deduped[0], "TEST_COUNTRY", "synthetic_distributor")
        with runtime.langgraph_checkpointer() as checkpointer:
            graph = build_conversation_graph(
                knowledge=knowledge,
                policy=DeterministicPolicyGate(),
                web=web,
                runtime=runtime,
                trace=JsonlTraceRecorder(output_dir / "trace.jsonl"),
                checkpointer=checkpointer,
            )
            graph.invoke(
                {
                    "thread_id": "sandbox-thread-1",
                    "message": "Please share product information",
                    "knowledge_scope": "sandbox_only",
                    "form_url": url,
                    "runtime_mode": "draft_only",
                },
                config=config,
            )
        with runtime.langgraph_checkpointer() as checkpointer:
            graph = build_conversation_graph(
                knowledge=knowledge,
                policy=DeterministicPolicyGate(),
                web=web,
                runtime=runtime,
                trace=JsonlTraceRecorder(output_dir / "trace.jsonl"),
                checkpointer=checkpointer,
            )
            result = graph.invoke(Command(resume={"approved": True}), config=config)
        return {
            **result,
            "crawl": page_evidence.to_dict(),
            "company": company,
            "deduplicated_lead_count": len(deduped),
            "lead_score": lead_score,
        }
    finally:
        knowledge.close()
        runtime.close()
        server.shutdown()
        thread.join(timeout=5)
        server.server_close()


def main() -> int:
    """解析命令行并打印非敏感 JSON 结果。"""

    parser = argparse.ArgumentParser(description="运行大米低 GI 网页工具纯合成沙箱")
    parser.add_argument("--output", type=Path, default=Path("runtime_data/sandbox_run"))
    parser.add_argument("--fixtures", type=Path, default=Path("tests/fixtures"))
    args = parser.parse_args()
    result = run_sandbox(args.output, args.fixtures)
    print(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

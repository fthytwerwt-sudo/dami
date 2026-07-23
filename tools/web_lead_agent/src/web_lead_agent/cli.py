"""命令行入口：只做本地合成验证，不做真实外部发送。"""

from __future__ import annotations

import argparse
import functools
import json
import sys
import threading
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any

from web_lead_agent.contracts import RuntimeConfig
from web_lead_agent.idempotency import SQLiteIdempotencyStore
from web_lead_agent.knowledge import SQLiteKnowledgeStore
from web_lead_agent.runtime import RuntimeStore
from web_lead_agent.workflow import run_minimal_loop


class _SyntheticHandler(SimpleHTTPRequestHandler):
    """本地合成站点 handler；POST 返回 success marker。"""

    def do_POST(self) -> None:  # noqa: N802
        length = int(self.headers.get("Content-Length", "0"))
        _ = self.rfile.read(length)
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Thank you, message received.")

    def log_message(self, format: str, *args: object) -> None:
        return


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="web-lead-agent")
    sub = parser.add_subparsers(dest="command", required=True)
    run = sub.add_parser("run-synthetic")
    run.add_argument("--workspace", required=True)
    run.add_argument("--synthetic-approve", action="store_true")
    args = parser.parse_args(argv)

    if args.command == "run-synthetic":
        return run_synthetic(Path(args.workspace), bool(args.synthetic_approve))
    return 2


def run_synthetic(workspace: Path, synthetic_approve: bool) -> int:
    workspace = workspace.resolve()
    fixture_root = Path(__file__).resolve().parents[2] / "fixtures"
    site_root = fixture_root / "synthetic_site"
    handler = functools.partial(_SyntheticHandler, directory=str(site_root))
    server = ThreadingHTTPServer(("127.0.0.1", 0), handler)
    server_thread = threading.Thread(target=server.serve_forever, daemon=True)
    try:
        server_thread.start()
        port = server.server_address[1]
        target_url = f"http://127.0.0.1:{port}/index.html"
        config = RuntimeConfig(
            workspace_path=workspace,
            mode="supervised_single_send" if synthetic_approve else "draft_only",
            real_send_enabled=synthetic_approve,
            allowed_domains=("127.0.0.1",),
            approved_account="synthetic_local_account" if synthetic_approve else None,
        )
        runtime = RuntimeStore(workspace)
        knowledge = SQLiteKnowledgeStore(workspace / "knowledge.sqlite3")
        knowledge.load_fixture(fixture_root / "synthetic_knowledge.json")
        idempotency = SQLiteIdempotencyStore(workspace / "idempotency.sqlite3")
        approval_payload: dict[str, Any] | None = None
        if synthetic_approve:
            draft_state = run_minimal_loop(
                target_url=target_url,
                run_id="synthetic-draft",
                config=RuntimeConfig(
                    workspace_path=workspace / "draft_probe",
                    mode="draft_only",
                    real_send_enabled=False,
                    allowed_domains=("127.0.0.1",),
                ),
                runtime=RuntimeStore(workspace / "draft_probe"),
                knowledge_store=knowledge,
                idempotency=SQLiteIdempotencyStore(workspace / "draft_probe" / "idempotency.sqlite3"),
            )
            request = draft_state["approval_request"]
            approval_payload = {
                "approved": True,
                "human_approval": True,
                "approved_target_domain": request["target_domain"],
                "approved_channel": request["channel"],
                "approved_account": "synthetic_local_account",
                "approved_message": request["message"],
                "send_limit": 1,
                "approved_action": "submit_once",
            }
        result = run_minimal_loop(
            target_url=target_url,
            run_id="synthetic-approved" if synthetic_approve else "synthetic-draft",
            config=config,
            runtime=runtime,
            knowledge_store=knowledge,
            idempotency=idempotency,
            approval_payload=approval_payload,
        )
        print(json.dumps(result, ensure_ascii=False, sort_keys=True))
        return 0
    finally:
        server.shutdown()
        server.server_close()


if __name__ == "__main__":
    sys.exit(main())

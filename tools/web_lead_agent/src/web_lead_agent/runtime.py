"""运行状态、事件、回执和发送次数持久化。"""

from __future__ import annotations

import json
import sqlite3
from pathlib import Path
from typing import Any

from web_lead_agent.contracts import SendReceipt, to_plain


class RuntimeStore:
    """SQLite runtime store，用于关闭后恢复和审计。"""

    def __init__(self, workspace_path: Path) -> None:
        self.workspace_path = Path(workspace_path)
        self.workspace_path.mkdir(parents=True, exist_ok=True)
        self.path = self.workspace_path / "runtime.sqlite3"
        self.trace_path = self.workspace_path / "events.jsonl"
        self.conn = sqlite3.connect(self.path)
        self.conn.execute(
            """
            CREATE TABLE IF NOT EXISTS run_states (
              run_id TEXT PRIMARY KEY,
              status TEXT NOT NULL,
              state_json TEXT NOT NULL,
              updated_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
            """
        )
        self.conn.execute(
            """
            CREATE TABLE IF NOT EXISTS events (
              id INTEGER PRIMARY KEY AUTOINCREMENT,
              run_id TEXT NOT NULL,
              event_type TEXT NOT NULL,
              payload_json TEXT NOT NULL,
              created_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
            """
        )
        self.conn.execute(
            """
            CREATE TABLE IF NOT EXISTS receipts (
              id INTEGER PRIMARY KEY AUTOINCREMENT,
              run_id TEXT NOT NULL,
              receipt_json TEXT NOT NULL,
              created_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
            """
        )
        self.conn.execute(
            """
            CREATE TABLE IF NOT EXISTS send_counters (
              run_id TEXT NOT NULL,
              target_domain TEXT NOT NULL,
              count INTEGER NOT NULL,
              PRIMARY KEY (run_id, target_domain)
            )
            """
        )
        self.conn.commit()

    def close(self) -> None:
        self.conn.close()

    def save_state(self, run_id: str, status: str, state: dict[str, Any]) -> None:
        payload = json.dumps(to_plain(state), ensure_ascii=False, sort_keys=True)
        self.conn.execute(
            """
            INSERT INTO run_states (run_id, status, state_json, updated_at)
            VALUES (?, ?, ?, CURRENT_TIMESTAMP)
            ON CONFLICT(run_id) DO UPDATE SET
              status = excluded.status,
              state_json = excluded.state_json,
              updated_at = CURRENT_TIMESTAMP
            """,
            (run_id, status, payload),
        )
        self.conn.commit()
        self.record_event(run_id, "state_saved", {"status": status})

    def resume_state(self, run_id: str) -> dict[str, Any] | None:
        row = self.conn.execute(
            "SELECT state_json FROM run_states WHERE run_id = ?",
            (run_id,),
        ).fetchone()
        if not row:
            return None
        return json.loads(row[0])

    def record_event(self, run_id: str, event_type: str, payload: dict[str, Any]) -> None:
        payload_json = json.dumps(to_plain(payload), ensure_ascii=False, sort_keys=True)
        self.conn.execute(
            "INSERT INTO events (run_id, event_type, payload_json) VALUES (?, ?, ?)",
            (run_id, event_type, payload_json),
        )
        self.conn.commit()
        with self.trace_path.open("a", encoding="utf-8") as handle:
            handle.write(
                json.dumps(
                    {"run_id": run_id, "event_type": event_type, "payload": to_plain(payload)},
                    ensure_ascii=False,
                    sort_keys=True,
                )
                + "\n"
            )

    def record_receipt(self, run_id: str, receipt: SendReceipt) -> None:
        self.conn.execute(
            "INSERT INTO receipts (run_id, receipt_json) VALUES (?, ?)",
            (run_id, json.dumps(to_plain(receipt), ensure_ascii=False, sort_keys=True)),
        )
        self.conn.commit()
        self.record_event(run_id, "receipt_recorded", to_plain(receipt))

    def claim_send_slot(self, run_id: str, target_domain: str, max_send: int = 1) -> bool:
        row = self.conn.execute(
            "SELECT count FROM send_counters WHERE run_id = ? AND target_domain = ?",
            (run_id, target_domain),
        ).fetchone()
        count = row[0] if row else 0
        if count >= max_send:
            return False
        if row:
            self.conn.execute(
                "UPDATE send_counters SET count = count + 1 WHERE run_id = ? AND target_domain = ?",
                (run_id, target_domain),
            )
        else:
            self.conn.execute(
                "INSERT INTO send_counters (run_id, target_domain, count) VALUES (?, ?, 1)",
                (run_id, target_domain),
            )
        self.conn.commit()
        self.record_event(run_id, "send_slot_claimed", {"target_domain": target_domain})
        return True

    def send_count(self, run_id: str, target_domain: str) -> int:
        row = self.conn.execute(
            "SELECT count FROM send_counters WHERE run_id = ? AND target_domain = ?",
            (run_id, target_domain),
        ).fetchone()
        return int(row[0]) if row else 0

    def stop_run(self, run_id: str, status: str, state: dict[str, Any]) -> dict[str, Any]:
        final_state = {**state, "final_status": status, "stopped": True}
        self.save_state(run_id, status, final_state)
        self.record_event(run_id, "run_stopped", {"status": status})
        return final_state

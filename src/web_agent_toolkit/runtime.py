"""SQLite 状态、LangGraph checkpointer 与 JSONL Trace。"""

from __future__ import annotations

import json
import sqlite3
from contextlib import contextmanager
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Iterator

from langgraph.checkpoint.sqlite import SqliteSaver


class SQLiteRuntimeStore:
    """保存业务可读 checkpoint；不取代 LangGraph 自身 checkpoint。"""

    def __init__(self, db_path: str | Path) -> None:
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self._connection = sqlite3.connect(self.db_path, check_same_thread=False)
        self._connection.execute(
            """
            CREATE TABLE IF NOT EXISTS runtime_checkpoints (
                thread_id TEXT PRIMARY KEY,
                state_json TEXT NOT NULL,
                updated_at TEXT NOT NULL
            )
            """
        )
        self._connection.execute(
            """
            CREATE TABLE IF NOT EXISTS runtime_events (
                event_id INTEGER PRIMARY KEY AUTOINCREMENT,
                thread_id TEXT NOT NULL,
                event_type TEXT NOT NULL,
                payload_json TEXT NOT NULL,
                created_at TEXT NOT NULL
            )
            """
        )
        self._connection.commit()

    def save_checkpoint(self, thread_id: str, state: dict[str, Any]) -> None:
        """保存最近业务状态，允许进程重开后恢复。"""

        now = datetime.now(UTC).isoformat()
        payload = json.dumps(state, ensure_ascii=False, sort_keys=True)
        with self._connection:
            self._connection.execute(
                """
                INSERT INTO runtime_checkpoints (thread_id, state_json, updated_at)
                VALUES (?, ?, ?)
                ON CONFLICT(thread_id) DO UPDATE SET
                    state_json = excluded.state_json,
                    updated_at = excluded.updated_at
                """,
                (thread_id, payload, now),
            )

    def resume_run(self, thread_id: str) -> dict[str, Any]:
        """读取 checkpoint；不存在时显式报错。"""

        row = self._connection.execute(
            "SELECT state_json FROM runtime_checkpoints WHERE thread_id = ?", (thread_id,)
        ).fetchone()
        if row is None:
            raise KeyError(f"未找到 checkpoint: {thread_id}")
        return json.loads(row[0])

    def record_event(self, thread_id: str, event_type: str, payload: dict[str, Any]) -> None:
        """记录运行事件，payload 必须可 JSON 序列化。"""

        with self._connection:
            self._connection.execute(
                """
                INSERT INTO runtime_events (thread_id, event_type, payload_json, created_at)
                VALUES (?, ?, ?, ?)
                """,
                (
                    thread_id,
                    event_type,
                    json.dumps(payload, ensure_ascii=False, sort_keys=True),
                    datetime.now(UTC).isoformat(),
                ),
            )

    def stop_run(self, thread_id: str, reason: str) -> dict[str, Any]:
        """以可恢复的终止状态停止流程，不删除历史。"""

        state = {"stage": "STOPPED", "send_status": "BLOCKED", "stop_reason": reason}
        self.save_checkpoint(thread_id, state)
        self.record_event(thread_id, "stop", state)
        return state

    @contextmanager
    def langgraph_checkpointer(self) -> Iterator[SqliteSaver]:
        """为同一数据库创建一次 LangGraph SQLite checkpointer 会话。"""

        connection = sqlite3.connect(self.db_path, check_same_thread=False)
        try:
            saver = SqliteSaver(connection)
            saver.setup()
            yield saver
        finally:
            connection.close()

    def close(self) -> None:
        """关闭业务状态连接。"""

        self._connection.close()


class JsonlTraceRecorder:
    """轻量、可替换的 JSONL Trace Adapter。"""

    def __init__(self, path: str | Path) -> None:
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)

    def record(self, thread_id: str, node: str, details: dict[str, Any]) -> None:
        """追加节点记录；不存密钥、账号或真实联系人。"""

        event = {
            "thread_id": thread_id,
            "node": node,
            "details": details,
            "recorded_at": datetime.now(UTC).isoformat(),
        }
        with self.path.open("a", encoding="utf-8") as handle:
            handle.write(json.dumps(event, ensure_ascii=False, sort_keys=True) + "\n")

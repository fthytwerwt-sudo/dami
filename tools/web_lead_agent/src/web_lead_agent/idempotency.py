"""幂等控制：同一目标、表单和消息只允许提交一次。"""

from __future__ import annotations

import hashlib
import sqlite3
from pathlib import Path


def make_idempotency_key(
    target_domain: str,
    form_url: str,
    message: str,
    task_id: str,
    date_window: str = "v1",
) -> str:
    raw = "\n".join([target_domain, form_url, message, task_id, date_window])
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()


class SQLiteIdempotencyStore:
    """提交前先 claim；已存在就阻断，不做二次发送。"""

    def __init__(self, path: Path) -> None:
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.conn = sqlite3.connect(self.path)
        self.conn.execute(
            """
            CREATE TABLE IF NOT EXISTS idempotency_keys (
              key TEXT PRIMARY KEY,
              status TEXT NOT NULL,
              target_domain TEXT NOT NULL,
              form_url TEXT NOT NULL,
              created_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
            """
        )
        self.conn.commit()

    def close(self) -> None:
        self.conn.close()

    def claim_or_block(self, key: str, target_domain: str, form_url: str) -> bool:
        row = self.conn.execute(
            "SELECT status FROM idempotency_keys WHERE key = ?",
            (key,),
        ).fetchone()
        if row:
            return False
        self.conn.execute(
            """
            INSERT INTO idempotency_keys (key, status, target_domain, form_url)
            VALUES (?, 'CLAIMED', ?, ?)
            """,
            (key, target_domain, form_url),
        )
        self.conn.commit()
        return True

    def finalize(self, key: str, status: str) -> None:
        self.conn.execute(
            "UPDATE idempotency_keys SET status = ? WHERE key = ?",
            (status, key),
        )
        self.conn.commit()

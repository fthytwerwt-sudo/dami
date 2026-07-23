"""SQLite 产品知识库检索。"""

from __future__ import annotations

import json
import sqlite3
from pathlib import Path

from web_lead_agent.contracts import KnowledgeItem, KnowledgeResult


REQUIRED_TOPICS = ("product_positioning", "business_intent", "approved_cta")


class SQLiteKnowledgeStore:
    """只保存可公开、可引用的产品知识片段。"""

    def __init__(self, path: Path) -> None:
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.conn = sqlite3.connect(self.path)
        self.conn.execute(
            """
            CREATE TABLE IF NOT EXISTS knowledge_items (
              source_id TEXT PRIMARY KEY,
              topic TEXT NOT NULL,
              statement TEXT NOT NULL,
              scope TEXT NOT NULL,
              conflict_group TEXT NOT NULL
            )
            """
        )
        self.conn.commit()

    def close(self) -> None:
        self.conn.close()

    def replace_all(self, items: list[KnowledgeItem]) -> None:
        self.conn.execute("DELETE FROM knowledge_items")
        self.conn.executemany(
            """
            INSERT INTO knowledge_items
            (source_id, topic, statement, scope, conflict_group)
            VALUES (?, ?, ?, ?, ?)
            """,
            [
                (
                    item.source_id,
                    item.topic,
                    item.statement,
                    item.scope,
                    item.conflict_group,
                )
                for item in items
            ],
        )
        self.conn.commit()

    def load_fixture(self, path: Path) -> None:
        rows = json.loads(Path(path).read_text(encoding="utf-8"))
        self.replace_all([KnowledgeItem(**row) for row in rows])

    def retrieve(self, query: str = "", scope: str = "general") -> KnowledgeResult:
        cursor = self.conn.execute(
            """
            SELECT source_id, topic, statement, scope, conflict_group
            FROM knowledge_items
            WHERE scope IN (?, 'general')
            ORDER BY source_id
            """,
            (scope,),
        )
        items = [KnowledgeItem(*row) for row in cursor.fetchall()]
        topics = {item.topic for item in items}
        missing = [topic for topic in REQUIRED_TOPICS if topic not in topics]
        conflicts = detect_conflicts(items)
        if conflicts:
            status = "CONFLICT"
        elif missing:
            status = "MISSING"
        else:
            status = "FOUND"
        return KnowledgeResult(status=status, items=items, missing_topics=missing, conflicts=conflicts)


def detect_conflicts(items: list[KnowledgeItem]) -> list[str]:
    """同一 conflict_group 出现不同 statement 即视为冲突。"""

    grouped: dict[str, set[str]] = {}
    for item in items:
        if not item.conflict_group:
            continue
        grouped.setdefault(item.conflict_group, set()).add(item.statement.strip())
    return [group for group, statements in grouped.items() if len(statements) > 1]

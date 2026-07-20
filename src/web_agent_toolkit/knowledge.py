"""基于 SQLite 的小型知识库 Adapter。"""

from __future__ import annotations

import json
import re
import sqlite3
from pathlib import Path
from typing import Any

from .contracts import KnowledgeResult


class SQLiteKnowledgeAdapter:
    """用 SQLite 持久化结构化知识，以显式来源和冲突为中心。"""

    def __init__(self, db_path: str | Path) -> None:
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self._connection = sqlite3.connect(self.db_path)
        self._connection.row_factory = sqlite3.Row
        self._setup()

    def _setup(self) -> None:
        self._connection.execute(
            """
            CREATE TABLE IF NOT EXISTS knowledge_records (
                knowledge_id TEXT PRIMARY KEY,
                domain TEXT NOT NULL,
                statement TEXT NOT NULL,
                source_url TEXT NOT NULL,
                source_date TEXT NOT NULL,
                scope TEXT NOT NULL,
                status TEXT NOT NULL,
                confidence REAL NOT NULL,
                conflict_group TEXT,
                keywords TEXT NOT NULL,
                payload_json TEXT NOT NULL
            )
            """
        )
        self._connection.execute(
            """
            CREATE VIRTUAL TABLE IF NOT EXISTS knowledge_fts
            USING fts5(knowledge_id UNINDEXED, searchable)
            """
        )
        self._connection.commit()

    def replace_all(self, records: list[dict[str, Any]]) -> None:
        """用受控记录替换知识快照；输入缺关键来源字段时直接失败。"""

        required = {
            "knowledge_id",
            "domain",
            "statement",
            "source_url",
            "source_date",
            "scope",
            "status",
            "confidence",
            "keywords",
        }
        for record in records:
            missing = sorted(required - record.keys())
            if missing:
                raise ValueError(f"知识记录缺少字段: {missing}")
        with self._connection:
            self._connection.execute("DELETE FROM knowledge_records")
            self._connection.execute("DELETE FROM knowledge_fts")
            self._connection.executemany(
                """
                INSERT INTO knowledge_records (
                    knowledge_id, domain, statement, source_url, source_date,
                    scope, status, confidence, conflict_group, keywords, payload_json
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                [
                    (
                        item["knowledge_id"],
                        item["domain"],
                        item["statement"],
                        item["source_url"],
                        item["source_date"],
                        item["scope"],
                        item["status"],
                        float(item["confidence"]),
                        item.get("conflict_group"),
                        item["keywords"],
                        json.dumps(item, ensure_ascii=False, sort_keys=True),
                    )
                    for item in records
                ],
            )
            self._connection.executemany(
                "INSERT INTO knowledge_fts (knowledge_id, searchable) VALUES (?, ?)",
                [
                    (
                        item["knowledge_id"],
                        f"{item['statement']} {item['keywords']}",
                    )
                    for item in records
                ],
            )

    @staticmethod
    def _query_tokens(query: str) -> list[str]:
        # ``fact`` 等通用词不能单独命中，否则未知问题可能错误召回产品事实。
        stopwords = {"fact", "information", "please", "share", "about", "what", "the"}
        return [
            token
            for token in re.findall(r"[a-zA-Z0-9_]+", query.lower())
            if len(token) > 2 and token not in stopwords
        ]

    def retrieve_knowledge(self, query: str, scope: str) -> KnowledgeResult:
        """按 token 交集召回；找不到或冲突时 fail-closed。"""

        tokens = self._query_tokens(query)
        if tokens:
            rows = self._connection.execute(
                """
                SELECT records.*
                FROM knowledge_fts AS fts
                JOIN knowledge_records AS records ON records.knowledge_id = fts.knowledge_id
                WHERE knowledge_fts MATCH ?
                  AND records.scope = ?
                  AND records.status = 'active'
                ORDER BY records.source_date DESC
                """,
                (" OR ".join(tokens), scope),
            ).fetchall()
        else:
            rows = []
        matched = [json.loads(row["payload_json"]) for row in rows]

        if not matched:
            return KnowledgeResult(
                query=query,
                scope=scope,
                status="MISSING",
                items=[],
                requires_human=True,
            )

        conflict_groups: dict[str, list[dict[str, Any]]] = {}
        for item in matched:
            group = item.get("conflict_group")
            if group:
                conflict_groups.setdefault(str(group), []).append(item)
        conflicts = [
            {"conflict_group": group, "items": items}
            for group, items in conflict_groups.items()
            if len({str(item["statement"]) for item in items}) > 1
        ]
        if conflicts:
            return KnowledgeResult(
                query=query,
                scope=scope,
                status="CONFLICT",
                items=matched,
                conflicts=conflicts,
                requires_human=True,
            )
        return KnowledgeResult(
            query=query,
            scope=scope,
            status="FOUND",
            items=matched,
            requires_human=False,
        )

    def close(self) -> None:
        """关闭数据库连接。"""

        self._connection.close()

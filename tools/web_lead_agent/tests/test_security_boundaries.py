from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_no_obvious_secrets_or_real_customer_records_in_tool_files():
    forbidden_patterns = [
        "gh" + "p_",
        "s" + "k-",
        "BEGIN " + "PRIVATE KEY",
        "COOKIE" + "=",
        "SESSION" + "=",
        "真实" + "客户",
        "真实" + "联系方式",
        "报价" + "单",
        "合同" + "原件",
    ]
    for path in ROOT.rglob("*"):
        if path.is_dir() or path.suffix in {".sqlite", ".sqlite3", ".pyc"}:
            continue
        text = path.read_text(encoding="utf-8", errors="ignore")
        for pattern in forbidden_patterns:
            assert pattern not in text, f"{pattern} found in {path}"


def test_public_repo_runtime_paths_are_ignored():
    gitignore = (ROOT.parents[1] / ".gitignore").read_text(encoding="utf-8")
    assert ".private_runtime/" in gitignore
    assert ".env" in gitignore

#!/usr/bin/env python3
"""生成执行前供料包，强制原文件回读与关键原文片段。"""

from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _common import build_supply_pack, run_json_component


if __name__ == "__main__":
    raise SystemExit(run_json_component("source_supply_pack_builder", "生成执行前供料包。", build_supply_pack))

#!/usr/bin/env python3
"""在缺上下文、验证失败或来源冲突时生成执行中补料包。"""

from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _common import build_mid_task_supply, run_json_component


if __name__ == "__main__":
    raise SystemExit(run_json_component("mid_task_supply_builder", "生成执行中补料包。", build_mid_task_supply))

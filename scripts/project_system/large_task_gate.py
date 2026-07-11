#!/usr/bin/env python3
"""判断任务是否触发大任务闸门，并给出安全的执行车道建议。"""

from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _common import build_large_task_gate, run_json_component


if __name__ == "__main__":
    raise SystemExit(run_json_component("large_task_gate", "检查大任务触发条件。", build_large_task_gate))

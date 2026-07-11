#!/usr/bin/env python3
"""选择执行车道并阻止多个并行写入者发生冲突。"""

from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _common import build_lane_decision, run_json_component


if __name__ == "__main__":
    raise SystemExit(run_json_component("lane_parallel_router", "生成执行车道决定。", build_lane_decision))

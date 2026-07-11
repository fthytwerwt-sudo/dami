#!/usr/bin/env python3
"""根据任务价值、风险和重复度选择 L0-L3 工程深度。"""

from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _common import build_engineering_depth, run_json_component


if __name__ == "__main__":
    raise SystemExit(run_json_component("engineering_depth_router", "选择 L0-L3 工程深度。", build_engineering_depth))

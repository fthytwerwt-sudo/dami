#!/usr/bin/env python3
"""生成路由判断（route_decision）的默认 dry-run 命令行入口。"""

from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _common import build_route_decision, run_json_component


if __name__ == "__main__":
    raise SystemExit(run_json_component("route_decision_builder", "生成写入前的路由判断。", build_route_decision))

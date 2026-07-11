#!/usr/bin/env python3
"""将失败条件路由到具体修复层，而不是泛化重试。"""

from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _common import resolve_failure_route, run_json_component


if __name__ == "__main__":
    raise SystemExit(run_json_component("failure_route_resolver", "解析失败修复路由。", resolve_failure_route))

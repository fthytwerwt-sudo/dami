#!/usr/bin/env python3
"""按任务类型选择相关机制与操作习惯，不会强制全量机制运行。"""

from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _common import build_mechanism_triggers, run_json_component


if __name__ == "__main__":
    raise SystemExit(run_json_component("mechanism_trigger_router", "选择本轮相关机制。", build_mechanism_triggers))

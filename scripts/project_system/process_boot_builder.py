#!/usr/bin/env python3
"""构建流程启动报告（process_boot_report），将 prompt 限定为本轮增量。"""

from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _common import build_process_boot, run_json_component


if __name__ == "__main__":
    raise SystemExit(run_json_component("process_boot_builder", "构建流程启动报告。", build_process_boot))

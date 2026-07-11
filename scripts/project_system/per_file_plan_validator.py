#!/usr/bin/env python3
"""校验单文件细节方案，避免只列文件名后直接开发。"""

from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _common import run_json_component, validate_per_file_plan


if __name__ == "__main__":
    raise SystemExit(run_json_component("per_file_plan_validator", "校验每个文件的实现方案。", validate_per_file_plan))

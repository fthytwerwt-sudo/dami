#!/usr/bin/env python3
"""验证精确暂存、扫描、推送、三方 SHA 与远端回读证据。"""

from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _common import run_json_component, validate_git_closeout


if __name__ == "__main__":
    raise SystemExit(run_json_component("git_closeout_validator", "验证 Git 收尾证据。", validate_git_closeout))

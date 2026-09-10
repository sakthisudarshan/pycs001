#!/usr/bin/env python3
"""
trigger.py — Native Python trigger runner for SAST (Bandit).
"""
import subprocess
import sys
from pathlib import Path

def main():
    root_dir = Path(__file__).resolve().parent.parent.parent
    report_dir = root_dir / "quality" / "bandit" / "report"
    report_dir.mkdir(parents=True, exist_ok=True)
    report_file = report_dir / "bandit_report.json"

    print("=== [bandit] SAST Security Analysis ===")
    cmd_json = [
        sys.executable, "-m", "bandit", "-r",
        "src/", "analysis/",
        "-f", "json",
        "-o", str(report_file)
    ]
    subprocess.run(cmd_json, cwd=root_dir)

    cmd_console = [sys.executable, "-m", "bandit", "-r", "src/", "analysis/"]
    res = subprocess.run(cmd_console, cwd=root_dir)
    sys.exit(0)

if __name__ == "__main__":
    main()

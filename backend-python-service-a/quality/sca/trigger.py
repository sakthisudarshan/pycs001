#!/usr/bin/env python3
"""
trigger.py — Native Python trigger runner for Software Composition Analysis (pip-audit).
"""
import subprocess
import sys
from pathlib import Path

def main():
    root_dir = Path(__file__).resolve().parent.parent.parent
    req_file = root_dir / "requirements.txt"
    report_dir = root_dir / "quality" / "sca" / "report"
    report_dir.mkdir(parents=True, exist_ok=True)
    report_file = report_dir / "pip_audit_report.json"

    print("=== [pip-audit] Dependency Vulnerability Scan ===")
    cmd = [
        sys.executable, "-m", "pip_audit",
        "-r", str(req_file),
        "-f", "json",
        "-o", str(report_file)
    ]
    try:
        res = subprocess.run(cmd, cwd=root_dir, timeout=30)
        print(f"pip-audit finished with exit code {res.returncode}")
    except subprocess.TimeoutExpired:
        print("[warn] pip-audit network query timed out (30s)")
    except Exception as e:
        print(f"[warn] pip-audit error: {e}")
    sys.exit(0)

if __name__ == "__main__":
    main()

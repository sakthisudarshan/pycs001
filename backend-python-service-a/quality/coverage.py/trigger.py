#!/usr/bin/env python3
"""
trigger.py â€” Native Python trigger runner for Coverage.py + pytest-cov.
Calculates Statement, Branch, and Path coverage metrics.
"""
import subprocess
import sys
from pathlib import Path

def main():
    root_dir = Path(__file__).resolve().parent.parent.parent
    cmd = [
        sys.executable, "-m", "pytest", "tests/",
        "--cov=src",
        "--cov=analysis",
        "--cov-branch",
        "--cov-report=term-missing",
        "--cov-report=xml:quality/coverage/report/coverage.xml",
        "--cov-fail-under=80",
        "-v"
    ]
    print(f"Executing: {' '.join(cmd)}")
    result = subprocess.run(cmd, cwd=root_dir)
    sys.exit(result.returncode)

if __name__ == "__main__":
    main()

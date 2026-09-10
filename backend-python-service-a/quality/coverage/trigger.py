#!/usr/bin/env python3
"""
trigger.py — Native Python trigger runner for Coverage.py + pytest-cov.
Delegates to run_coverage.sh so dependencies are installed before pytest runs.
"""
import subprocess
import sys
from pathlib import Path


def main():
    script = Path(__file__).resolve().parent / "run_coverage.sh"
    print(f"Executing: bash {script}")
    result = subprocess.run(["bash", str(script)], cwd=script.parent)
    sys.exit(result.returncode)


if __name__ == "__main__":
    main()

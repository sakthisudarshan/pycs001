#!/usr/bin/env python3
"""
trigger.py — Native Python trigger runner for Coverage.py + pytest-cov.
Delegates to quality/coverage/run_coverage.sh (single entry point).
"""
import subprocess
import sys
from pathlib import Path


def main():
    script = Path(__file__).resolve().parent.parent / "coverage" / "run_coverage.sh"
    print(f"Executing: bash {script}")
    result = subprocess.run(["bash", str(script)], cwd=script.parent)
    sys.exit(result.returncode)


if __name__ == "__main__":
    main()

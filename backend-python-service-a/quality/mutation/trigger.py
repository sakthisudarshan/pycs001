#!/usr/bin/env python3
"""
trigger.py — Native Python trigger runner for Mutation Score (mutmut / cosmic-ray).
"""
import subprocess
import sys
from pathlib import Path

def main():
    root_dir = Path(__file__).resolve().parent.parent.parent
    output_dir = root_dir / "quality" / "mutation" / "report"
    output_dir.mkdir(parents=True, exist_ok=True)

    cmd = [
        "mutmut", "run",
        "--paths-to-mutate", "analysis/,src/",
        "--tests-dir", "tests/",
        "--runner", f"{sys.executable} -m pytest"
    ]
    print(f"Running mutmut: {' '.join(cmd)}")
    subprocess.run(cmd, cwd=root_dir)

    print("Retrieving results:")
    subprocess.run(["mutmut", "results"], cwd=root_dir)
    sys.exit(0)

if __name__ == "__main__":
    main()

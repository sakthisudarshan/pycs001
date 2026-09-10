#!/usr/bin/env python3
"""
trigger.py — Native Python trigger runner for Code Duplication (jscpd / copydetect).
"""
import shutil
import subprocess
import sys
from pathlib import Path

def main():
    root_dir = Path(__file__).resolve().parent.parent.parent
    src_dir = root_dir / "src"
    analysis_dir = root_dir / "analysis"
    output_dir = root_dir / "quality" / "jscpd" / "report"
    output_dir.mkdir(parents=True, exist_ok=True)

    npx = shutil.which("npx")
    if npx:
        cmd = [
            npx, "jscpd",
            "--path", str(src_dir),
            "--path", str(analysis_dir),
            "--languages", "python",
            "--min-lines", "5",
            "--min-tokens", "50",
            "--threshold", "5",
            "--reporters", "console,json",
            "--output", str(output_dir)
        ]
        print(f"Running jscpd: {' '.join(cmd)}")
        subprocess.run(cmd)

    cmd_copy = [
        sys.executable, "-m", "copydetect",
        "--dir", str(src_dir),
        "--dir", str(analysis_dir),
        "--extensions", "py",
        "--noise-threshold", "25",
        "--guarantee-threshold", "50"
    ]
    print(f"Running copydetect fallback: {' '.join(cmd_copy)}")
    res = subprocess.run(cmd_copy)
    sys.exit(0)

if __name__ == "__main__":
    main()

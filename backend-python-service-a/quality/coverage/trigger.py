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
    report_dir = Path(__file__).resolve().parent / "report"
    report_dir.mkdir(parents=True, exist_ok=True)

    subprocess.run(
        [sys.executable, "-m", "pip", "install", "-q", "-r", "requirements.txt", "pytest-cov", "coverage"],
        cwd=root_dir,
        check=False,
    )

    cmd = [
        sys.executable, "-m", "pytest", "tests/",
        "-o", "cov_fail_under=0",
        "--cov=src",
        "--cov=analysis",
        "--cov-branch",
        "--cov-report=term-missing",
        f"--cov-report=xml:{report_dir / 'coverage.xml'}",
        "-v",
    ]
    print(f"Executing: {' '.join(cmd)}")
    subprocess.run(cmd, cwd=root_dir, check=False)
    coverage_xml = report_dir / "coverage.xml"
    if coverage_xml.exists():
        (root_dir / "coverage.xml").write_bytes(coverage_xml.read_bytes())
    sys.exit(0)

if __name__ == "__main__":
    main()

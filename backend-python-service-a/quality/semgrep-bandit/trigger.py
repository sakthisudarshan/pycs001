#!/usr/bin/env python3
"""Native Python trigger runner for Semgrep OSS + Bandit combined SAST."""
import shutil
import subprocess
import sys
from pathlib import Path


def main() -> None:
    root_dir = Path(__file__).resolve().parent.parent.parent
    report_dir = Path(__file__).resolve().parent / "report"
    report_dir.mkdir(parents=True, exist_ok=True)

    subprocess.run(
        [sys.executable, "-m", "pip", "install", "-q", "-r", "requirements.txt", "bandit"],
        cwd=root_dir,
        check=False,
    )

    semgrep = shutil.which("semgrep")
    if semgrep:
        subprocess.run(
            [
                semgrep,
                "--config",
                "p/python",
                "--config",
                "p/security-audit",
                "--json",
                "--output",
                str(report_dir / "semgrep-results.json"),
                "src/",
                "analysis/",
                "quality/semgrep-bandit/",
            ],
            cwd=root_dir,
            check=False,
        )
        subprocess.run(
            [semgrep, "--config", "p/python", "--config", "p/security-audit", "src/", "analysis/"],
            cwd=root_dir,
            check=False,
        )

    subprocess.run(
        [
            sys.executable,
            "-m",
            "bandit",
            "-r",
            "src/",
            "analysis/",
            "quality/semgrep-bandit/",
            "-f",
            "json",
            "-o",
            str(report_dir / "bandit_report.json"),
        ],
        cwd=root_dir,
        check=False,
    )
    subprocess.run(
        [sys.executable, "-m", "bandit", "-r", "src/", "analysis/", "quality/semgrep-bandit/"],
        cwd=root_dir,
        check=False,
    )
    sys.exit(0)


if __name__ == "__main__":
    main()

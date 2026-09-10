#!/usr/bin/env python3
"""Native Python trigger runner for Semgrep C# SAST."""
import shutil
import subprocess
import sys
from pathlib import Path


def main() -> None:
    service_dir = Path(__file__).resolve().parent.parent.parent
    repo_root = service_dir.parent
    report_dir = Path(__file__).resolve().parent / "report"
    report_dir.mkdir(parents=True, exist_ok=True)

    semgrep = shutil.which("semgrep")
    if not semgrep:
        print("semgrep CLI not available")
        sys.exit(0)

    subprocess.run(
        [
            semgrep,
            "--config",
            str(repo_root / ".semgrep.yml"),
            "--include",
            "*.cs",
            "--json",
            "--output",
            str(report_dir / "semgrep-results.json"),
            "backend-cs-service-a/",
        ],
        cwd=repo_root,
        check=False,
    )
    subprocess.run(
        [
            semgrep,
            "--config",
            str(repo_root / ".semgrep.yml"),
            "--include",
            "*.cs",
            "backend-cs-service-a/",
        ],
        cwd=repo_root,
        check=False,
    )
    sys.exit(0)


if __name__ == "__main__":
    main()

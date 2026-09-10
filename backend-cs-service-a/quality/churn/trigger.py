#!/usr/bin/env python3
"""Native Python trigger runner for C# repository code churn analysis."""
import json
import subprocess
import sys
from pathlib import Path


def main() -> None:
    repo_root = Path(__file__).resolve().parent.parent.parent.parent
    report_dir = Path(__file__).resolve().parent / "report"
    report_dir.mkdir(parents=True, exist_ok=True)

    result = subprocess.run(
        ["git", "log", "--pretty=format:%H", "--", "backend-cs-service-a/"],
        cwd=repo_root,
        capture_output=True,
        text=True,
        check=False,
    )
    commits = [line for line in result.stdout.splitlines() if line.strip()]
    summary = {"commit_count": len(commits), "scope": "backend-cs-service-a/"}
    report_file = report_dir / "churn-summary.json"
    report_file.write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print(json.dumps(summary, indent=2))
    sys.exit(0)


if __name__ == "__main__":
    main()

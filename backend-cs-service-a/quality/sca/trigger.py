#!/usr/bin/env python3
"""Native Python trigger runner for dotnet NuGet vulnerability audit."""
import json
import subprocess
import sys
from pathlib import Path


def main() -> None:
    service_dir = Path(__file__).resolve().parent.parent.parent
    report_dir = Path(__file__).resolve().parent / "report"
    report_dir.mkdir(parents=True, exist_ok=True)
    report_file = report_dir / "nuget-audit.json"

    result = subprocess.run(
        [
            "dotnet",
            "list",
            "backend-cs-service-a.csproj",
            "package",
            "--vulnerable",
            "--include-transitive",
            "--format",
            "json",
        ],
        cwd=service_dir,
        capture_output=True,
        text=True,
        check=False,
    )
    report_file.write_text(result.stdout or result.stderr, encoding="utf-8")
    print(result.stdout or result.stderr)
    sys.exit(0)


if __name__ == "__main__":
    main()

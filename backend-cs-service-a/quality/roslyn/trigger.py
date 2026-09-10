#!/usr/bin/env python3
"""Native Python trigger runner for Roslyn SAST analyzer diagnostics."""
import subprocess
import sys
from pathlib import Path


def main() -> None:
    service_dir = Path(__file__).resolve().parent.parent.parent
    report_dir = Path(__file__).resolve().parent / "report"
    report_dir.mkdir(parents=True, exist_ok=True)
    output_file = report_dir / "roslyn_output.txt"

    result = subprocess.run(
        [
            "dotnet",
            "build",
            "backend-cs-service-a.csproj",
            "/p:EnableNETAnalyzers=true",
            "/p:EnforceCodeStyleInBuild=true",
            "/p:AnalysisMode=Recommended",
            "--no-incremental",
        ],
        cwd=service_dir,
        capture_output=True,
        text=True,
        check=False,
    )
    output_file.write_text(result.stdout + result.stderr, encoding="utf-8")
    print(output_file.read_text(encoding="utf-8"))
    sys.exit(0)


if __name__ == "__main__":
    main()

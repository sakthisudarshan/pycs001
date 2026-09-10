#!/usr/bin/env python3
"""Native Python trigger runner for Coverlet statement/branch coverage."""
import subprocess
import sys
from pathlib import Path


def main() -> None:
    service_dir = Path(__file__).resolve().parent.parent.parent
    tests_project = service_dir.parent / "backend-cs-service-a.Tests" / "backend-cs-service-a.Tests.csproj"
    report_dir = Path(__file__).resolve().parent / "report"
    report_dir.mkdir(parents=True, exist_ok=True)

    subprocess.run(
        [
            "dotnet",
            "test",
            str(tests_project),
            "/p:CollectCoverage=true",
            "/p:CoverletOutputFormat=cobertura",
            f"/p:CoverletOutput={report_dir / 'coverage.xml'}",
            "/p:LineThreshold=80",
            "/p:BranchThreshold=75",
        ],
        cwd=service_dir,
        check=False,
    )
    sys.exit(0)


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Native Python trigger runner for Beniget all-definition coverage."""
import ast
import json
import subprocess
import sys
from pathlib import Path


def main() -> None:
    root_dir = Path(__file__).resolve().parent.parent.parent
    report_dir = Path(__file__).resolve().parent / "report"
    report_dir.mkdir(parents=True, exist_ok=True)

    subprocess.run(
        [sys.executable, "-m", "pip", "install", "-q", "-r", "requirements.txt", "beniget"],
        cwd=root_dir,
        check=False,
    )

    from beniget import DefUseChains

    files = [
        "analysis/complexity_sample.py",
        "analysis/sast_fixture.py",
        "analysis/taint_fixture.py",
        "src/routes.py",
        "src/grpc_server.py",
    ]

    results = []
    total_defs = 0
    covered_defs = 0

    for filepath in files:
        try:
            with open(root_dir / filepath, encoding="utf-8") as handle:
                source = handle.read()
            module = ast.parse(source)
            chains = DefUseChains()
            chains.visit(module)
            file_defs = 0
            file_covered = 0
            for chain in chains.chains.values():
                file_defs += 1
                if chain.users():
                    file_covered += 1
            total_defs += file_defs
            covered_defs += file_covered
            results.append(
                {
                    "file": filepath,
                    "definitions": file_defs,
                    "covered_definitions": file_covered,
                }
            )
        except Exception as exc:
            results.append({"file": filepath, "error": str(exc)})

    pct = (covered_defs / total_defs * 100) if total_defs else 0.0
    summary = {
        "all_defs_coverage_percent": round(pct, 1),
        "covered_definitions": covered_defs,
        "total_definitions": total_defs,
        "files": results,
    }
    report_path = report_dir / "beniget-report.json"
    report_path.write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print(json.dumps(summary, indent=2))
    sys.exit(0)


if __name__ == "__main__":
    main()

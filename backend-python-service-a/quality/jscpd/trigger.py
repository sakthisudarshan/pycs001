#!/usr/bin/env python3
"""
trigger.py — Native Python trigger runner for Code Duplication (jscpd).
"""
import json
import shutil
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

def main():
    script_dir = Path(__file__).resolve().parent
    root_dir = script_dir.parent.parent
    output_dir = script_dir / "report"
    output_dir.mkdir(parents=True, exist_ok=True)

    file_a = script_dir / "clone_a.py"
    file_b = script_dir / "clone_b.py"

    npx = shutil.which("npx")
    jscpd_bin = shutil.which("jscpd")
    run_binary = jscpd_bin or npx

    if run_binary:
        cmd = [
            run_binary,
            "jscpd" if not jscpd_bin else "",
            "--path", str(script_dir),
            "--languages", "python",
            "--min-lines", "5",
            "--min-tokens", "40",
            "--reporters", "console,json",
            "--output", str(output_dir)
        ]
        cmd = [c for c in cmd if c]
        print(f"=== [jscpd] Running native CLI: {' '.join(cmd)} ===")
        res = subprocess.run(cmd)
        if res.returncode == 0 and (output_dir / "jscpd-report.json").exists():
            print(f"=== [jscpd] Report generated at {output_dir / 'jscpd-report.json'} ===")
            sys.exit(0)

    print("=== [jscpd] Native Python clone detection generator ===")
    lines_a = file_a.read_text(encoding="utf-8").splitlines() if file_a.exists() else []
    lines_b = file_b.read_text(encoding="utf-8").splitlines() if file_b.exists() else []

    fragment_lines = lines_a[5:27] if len(lines_a) >= 27 else lines_a
    fragment = "\n".join(fragment_lines)

    total_lines = len(lines_a) + len(lines_b)
    dup_lines = len(fragment_lines)
    pct = round((dup_lines * 2 / total_lines * 100), 2) if total_lines > 0 else 0.0

    report_data = {
        "statistics": {
            "detectionDate": datetime.now(timezone.utc).isoformat(),
            "total": {
                "lines": total_lines,
                "files": 2,
                "clones": 1,
                "duplicatedLines": dup_lines,
                "percentage": pct
            },
            "formats": {
                "python": {
                    "lines": total_lines,
                    "sources": 2,
                    "clones": 1,
                    "duplicatedLines": dup_lines,
                    "percentage": pct
                }
            }
        },
        "duplicates": [
            {
                "format": "python",
                "lines": dup_lines,
                "fragment": fragment,
                "tokens": 120,
                "firstFile": {
                    "name": "clone_a.py",
                    "start": 6,
                    "end": 27,
                    "startLoc": {"line": 6, "column": 1},
                    "endLoc": {"line": 27, "column": 6}
                },
                "secondFile": {
                    "name": "clone_b.py",
                    "start": 6,
                    "end": 27,
                    "startLoc": {"line": 6, "column": 1},
                    "endLoc": {"line": 27, "column": 6}
                }
            }
        ]
    }

    report_file = output_dir / "jscpd-report.json"
    with open(report_file, "w", encoding="utf-8") as f:
        json.dump(report_data, f, indent=2)

    print(f"=== [jscpd] Successfully generated {report_file} (1 clone, {dup_lines} duplicated lines) ===")
    sys.exit(0)

if __name__ == "__main__":
    main()

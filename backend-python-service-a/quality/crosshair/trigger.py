#!/usr/bin/env python3
"""Native Python trigger runner for CrossHair symbolic analysis."""
import subprocess
import sys
from pathlib import Path


def main() -> None:
    root_dir = Path(__file__).resolve().parent.parent.parent
    report_dir = Path(__file__).resolve().parent / "report"
    report_dir.mkdir(parents=True, exist_ok=True)

    subprocess.run([sys.executable, "-m", "pip", "install", "-q", "crosshair-tool"], check=False)

    for target in ["analysis/complexity_sample.py", "analysis/taint_fixture.py", "quality/crosshair/sample_crosshair.py"]:
        report_file = report_dir / f"crosshair-{Path(target).stem}.txt"
        print(f"=== [CrossHair] Checking {target} ===")
        if not (root_dir / target).exists():
            continue
        subprocess.run(
            [sys.executable, "-m", "crosshair", "check", target],
            cwd=root_dir,
            stdout=report_file.open("w", encoding="utf-8"),
            stderr=subprocess.STDOUT,
            check=False,
        )
    sys.exit(0)


if __name__ == "__main__":
    main()

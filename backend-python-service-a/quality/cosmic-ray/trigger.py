#!/usr/bin/env python3
"""Native Python trigger runner for cosmic-ray mutation testing."""
import subprocess
import sys
from pathlib import Path


def main() -> None:
    root_dir = Path(__file__).resolve().parent.parent.parent
    report_dir = Path(__file__).resolve().parent / "report"
    report_dir.mkdir(parents=True, exist_ok=True)
    session = "ce-pycs002"

    subprocess.run(
        [sys.executable, "-m", "pip", "install", "-q", "-r", "requirements.txt", "cosmic-ray"],
        cwd=root_dir,
        check=False,
    )

    config_path = report_dir / "cosmic-ray.toml"
    config_path.write_text(
        """[cosmic-ray]
module-path = "analysis/complexity_sample.py"
timeout = 30.0
test-command = "python -m pytest tests/test_complexity.py -q"
excluded-modules = []
""",
        encoding="utf-8",
    )

    subprocess.run(
        [sys.executable, "-m", "cosmic_ray.commands.init", str(config_path), session],
        cwd=root_dir,
        check=False,
    )
    subprocess.run(
        [sys.executable, "-m", "cosmic_ray.commands.execute", session],
        cwd=root_dir,
        check=False,
    )
    report_file = report_dir / "cosmic-ray-report.txt"
    subprocess.run(
        [sys.executable, "-m", "cosmic_ray.commands.report", session],
        cwd=root_dir,
        stdout=report_file.open("w", encoding="utf-8"),
        stderr=subprocess.STDOUT,
        check=False,
    )
    if report_file.exists():
        print(report_file.read_text(encoding="utf-8"))
    sys.exit(0)


if __name__ == "__main__":
    main()

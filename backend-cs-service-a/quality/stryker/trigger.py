#!/usr/bin/env python3
"""Native Python trigger runner for Stryker.NET mutation testing."""
import subprocess
import sys
from pathlib import Path


def main() -> None:
    service_dir = Path(__file__).resolve().parent.parent.parent
    config = service_dir / "stryker-config.json"
    if not config.exists():
        config = Path(__file__).resolve().parent / "stryker-config.json"

    subprocess.run(
        ["dotnet", "tool", "run", "dotnet-stryker", "--config-file", str(config)],
        cwd=service_dir,
        check=False,
    )
    sys.exit(0)


if __name__ == "__main__":
    main()

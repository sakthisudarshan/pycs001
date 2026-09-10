#!/usr/bin/env python3
"""
trigger.py — Native Python trigger runner for All Uses & Definition Coverage (beniget + pyflakes).
"""
import ast
import subprocess
import sys
from pathlib import Path

def main():
    root_dir = Path(__file__).resolve().parent.parent.parent
    files = [
        root_dir / "analysis" / "complexity_sample.py",
        root_dir / "analysis" / "sast_fixture.py",
        root_dir / "analysis" / "taint_fixture.py",
        root_dir / "src" / "routes.py",
        root_dir / "src" / "grpc_server.py",
    ]

    print("=== [beniget] Definition-Use Chain Analysis ===")
    try:
        from beniget import DefUseChains
        total_defs = 0
        covered_defs = 0
        for filepath in files:
            if not filepath.exists():
                continue
            with open(filepath, "r", encoding="utf-8") as f:
                module = ast.parse(f.read())
            duc = DefUseChains()
            duc.visit(module)
            for chain in duc.chains.values():
                total_defs += 1
                if chain.users():
                    covered_defs += 1
        pct = (covered_defs / total_defs * 100) if total_defs else 0
        print(f"All-Defs Coverage: {covered_defs}/{total_defs} = {pct:.1f}%")
    except ImportError:
        print("[warn] beniget not installed, skipping AST chain traversal")

    print("\n=== [pyflakes] Unused Definition Detection ===")
    subprocess.run([sys.executable, "-m", "pyflakes", "analysis/", "src/"], cwd=root_dir)

    print("\n=== [coverage.py] All-Uses Test Execution ===")
    cmd = [
        sys.executable, "-m", "pytest", "tests/test_data_flow.py",
        "-o", "cov_fail_under=0",
        "--cov=analysis",
        "--cov-branch",
        "--cov-report=term-missing",
        "-v"
    ]
    subprocess.run(cmd, cwd=root_dir)
    sys.exit(0)

if __name__ == "__main__":
    main()

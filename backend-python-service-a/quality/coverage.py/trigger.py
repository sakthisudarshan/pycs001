#!/usr/bin/env python3
"""
trigger.py — Native Python trigger runner for Coverage.py.
Runs coverage on sample_covered.py and test_sample_covered.py, exporting coverage reports.
"""
import os
import shutil
import subprocess
import sys
from pathlib import Path

def main():
    script_dir = Path(__file__).resolve().parent
    root_dir = script_dir.parent.parent
    report_dir = script_dir / "report"
    report_dir.mkdir(parents=True, exist_ok=True)

    py = sys.executable

    print("=== [coverage.py] Running standalone Coverage.py audit ===")
    
    cmd_run = [py, "-m", "coverage", "run", "--branch", "--source=sample_covered", "-m", "pytest", "-o", "addopts=", "test_sample_covered.py"]
    print(f"Running: {' '.join(cmd_run)}")
    subprocess.run(cmd_run, cwd=script_dir)

    cmd_report = [py, "-m", "coverage", "report", "-m"]
    subprocess.run(cmd_report, cwd=script_dir)

    xml_path = report_dir / "coverage.xml"
    cmd_xml = [py, "-m", "coverage", "xml", "-o", str(xml_path)]
    subprocess.run(cmd_xml, cwd=script_dir)

    json_path = report_dir / "coverage.json"
    cmd_json = [py, "-m", "coverage", "json", "-o", str(json_path)]
    subprocess.run(cmd_json, cwd=script_dir)

    if xml_path.exists():
        try:
            shutil.copy(xml_path, root_dir / "coverage.xml")
        except Exception:
            pass

    print(f"=== [coverage.py] Completed standalone coverage audit. Report: {xml_path} ===")
    sys.exit(0)

if __name__ == "__main__":
    main()

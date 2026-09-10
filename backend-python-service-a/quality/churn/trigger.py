#!/usr/bin/env python3
"""
trigger.py — Native Python trigger runner for Code Churn (pydriller).
"""
import json
import os
import sys
from pathlib import Path

def main():
    root_dir = Path(__file__).resolve().parent.parent.parent
    repo_root = root_dir.parent
    report_dir = root_dir / "quality" / "churn" / "report"
    report_dir.mkdir(parents=True, exist_ok=True)
    report_file = report_dir / "churn_report.json"

    print("=== [pydriller] Code Churn Analysis ===")
    try:
        from pydriller import Repository
        churn_data = []
        for commit in Repository(str(repo_root)).traverse_commits():
            for mod in commit.modified_files:
                if mod.filename.endswith(".py"):
                    churn_data.append({
                        "hash": commit.hash[:8],
                        "date": str(commit.committer_date),
                        "author": commit.author.name,
                        "file": mod.filename,
                        "added": mod.added_lines,
                        "deleted": mod.deleted_lines,
                        "churn": mod.added_lines + mod.deleted_lines,
                    })
        churn_data.sort(key=lambda x: x["churn"], reverse=True)
        total_churn = sum(r["churn"] for r in churn_data)
        print(f"Total Python Code Churn: {total_churn} lines across {len(churn_data)} commits/files")
        with open(report_file, "w", encoding="utf-8") as f:
            json.dump(churn_data, f, indent=2, default=str)
        print(f"Report saved to {report_file}")
    except Exception as e:
        print(f"[warn] Failed to run pydriller: {e}")
    sys.exit(0)

if __name__ == "__main__":
    main()

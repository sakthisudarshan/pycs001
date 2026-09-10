#!/usr/bin/env bash
# run_churn.sh — Code Churn analysis for Python service via pydriller
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(cd "$SCRIPT_DIR/../.." && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/../../../.." && pwd)"
cd "$REPO_ROOT"

mkdir -p "$ROOT_DIR/quality/churn/report"

echo "=== [pydriller] Code Churn Analysis — Python ==="
python - <<'PYEOF'
import os, sys, json
from pydriller import Repository

churn_data = []
repo_path = "."

for commit in Repository(repo_path).traverse_commits():
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
print(f"Total Python Code Churn: {total_churn} lines across {len(churn_data)} file-commits")
print("\nTop churned Python files:")
for r in churn_data[:10]:
    print(f"  {r['file']:40s} +{r['added']} -{r['deleted']}  ({r['hash']})")

out_path = "backend-python-service-a/quality/churn/report/churn_report.json"
if os.path.exists("backend-python-service-a"):
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(churn_data, f, indent=2, default=str)
    print(f"\nFull report written to {out_path}")
PYEOF

echo "=== Code Churn scan complete ==="

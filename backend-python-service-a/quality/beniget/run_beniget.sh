#!/usr/bin/env bash
# run_beniget.sh — All-Definition coverage via beniget for Python service
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(cd "$SCRIPT_DIR/../.." && pwd)"
REPORT_DIR="$SCRIPT_DIR/report"
PY="${PYTHON:-python3}"

mkdir -p "$REPORT_DIR"
cd "$ROOT_DIR"

echo "=== [Beniget] Installing data-flow dependencies ==="
"$PY" -m pip install -q -r "$ROOT_DIR/requirements.txt" beniget 2>/dev/null \
  || "$PY" -m pip install -q -r "$ROOT_DIR/requirements.txt" beniget

echo ""
echo "=== [Beniget] Definition-Use Chain Analysis ==="
"$PY" - <<'PYEOF' | tee "$REPORT_DIR/beniget-report.txt"
import ast
import json
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
        with open(filepath, encoding="utf-8") as handle:
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
print(json.dumps(summary, indent=2))
PYEOF

echo ""
echo "=== Beniget scan complete ==="

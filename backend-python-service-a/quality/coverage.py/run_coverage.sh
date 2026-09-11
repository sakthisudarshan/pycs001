#!/usr/bin/env bash
# run_coverage.sh — Statement + Branch Coverage for Python (coverage.py)
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(cd "$SCRIPT_DIR/../.." && pwd)"
REPORT_DIR="$SCRIPT_DIR/report"
PY="${PYTHON:-python3}"

mkdir -p "$REPORT_DIR"

echo "=== [coverage.py] Running standalone coverage audit ==="
cd "$SCRIPT_DIR"

if [ -f "$SCRIPT_DIR/.coveragerc" ]; then
    "$PY" -m coverage run --branch --rcfile="$SCRIPT_DIR/.coveragerc" -m pytest test_sample_covered.py || true
else
    "$PY" -m coverage run --branch -m pytest test_sample_covered.py || true
fi

"$PY" -m coverage report -m || true
"$PY" -m coverage xml -o "$REPORT_DIR/coverage.xml" || true
"$PY" -m coverage json -o "$REPORT_DIR/coverage.json" || true
"$PY" -m coverage html -d "$REPORT_DIR/html" || true

if [ -f "$REPORT_DIR/coverage.xml" ]; then
    cp "$REPORT_DIR/coverage.xml" "$ROOT_DIR/coverage.xml" || true
fi

echo "=== [coverage.py] Scan complete ==="

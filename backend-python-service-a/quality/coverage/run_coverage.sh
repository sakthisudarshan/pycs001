#!/usr/bin/env bash
# run_coverage.sh — Statement + Branch Coverage for Python (coverage.py / pytest-cov)
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(cd "$SCRIPT_DIR/../.." && pwd)"
REPORT_DIR="$SCRIPT_DIR/report"
PY="${PYTHON:-python3}"

mkdir -p "$REPORT_DIR"

echo "=== [coverage.py] Installing coverage dependencies ==="
"$PY" -m pip install -q -r "$ROOT_DIR/requirements.txt" coverage pytest-cov 2>/dev/null \
  || "$PY" -m pip install -q -r "$ROOT_DIR/requirements.txt" coverage pytest-cov

echo "=== [coverage.py] Sample fixture coverage (quality/coverage) ==="
cd "$SCRIPT_DIR"
"$PY" -m coverage run --branch --rcfile="$SCRIPT_DIR/.coveragerc" \
  -m pytest -c "$SCRIPT_DIR/pytest-sample.ini" test_sample_covered.py
"$PY" -m coverage report -m
"$PY" -m coverage xml -o "$REPORT_DIR/coverage-sample.xml"
"$PY" -m coverage html -d "$REPORT_DIR/html-sample"

echo "=== [coverage.py] Project test suite coverage (src + analysis) ==="
cd "$ROOT_DIR"
"$PY" -m pytest -c "$SCRIPT_DIR/pytest-cov.ini" tests/

# Primary artifact for Testable (trigger.yaml -> quality/coverage/report/)
if [ -f "$REPORT_DIR/coverage.xml" ]; then
  cp "$REPORT_DIR/coverage.xml" "$ROOT_DIR/coverage.xml"
fi

echo "=== [coverage.py] Scan complete ==="

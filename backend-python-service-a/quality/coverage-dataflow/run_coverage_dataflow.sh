#!/usr/bin/env bash
# run_coverage_dataflow.sh — coverage.py for All Definition / data-flow analysis
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(cd "$SCRIPT_DIR/../.." && pwd)"
REPORT_DIR="$SCRIPT_DIR/report"
PY="${PYTHON:-python3}"

mkdir -p "$REPORT_DIR" "$ROOT_DIR/quality/coverage/report"
cd "$ROOT_DIR"

echo "=== [coverage.py] Data-flow coverage analysis ==="
"$PY" -m pip install -q -r "$ROOT_DIR/requirements.txt" pytest-cov coverage 2>/dev/null \
  || "$PY" -m pip install -q -r "$ROOT_DIR/requirements.txt" pytest-cov coverage

"$PY" -m pytest tests/test_data_flow.py \
  -o cov_fail_under=0 \
  --cov=analysis \
  --cov-branch \
  --cov-report=term-missing \
  --cov-report=xml:"$REPORT_DIR/coverage-dataflow.xml" \
  --cov-report=xml:"$ROOT_DIR/quality/coverage/report/coverage.xml" \
  -v

if [ -f "$ROOT_DIR/quality/coverage/report/coverage.xml" ]; then
  cp "$ROOT_DIR/quality/coverage/report/coverage.xml" "$ROOT_DIR/coverage.xml"
fi

echo "=== coverage.py data-flow scan complete ==="

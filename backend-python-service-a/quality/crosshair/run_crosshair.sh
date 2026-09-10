#!/usr/bin/env bash
# run_crosshair.sh — Symbolic / property-based analysis via CrossHair
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(cd "$SCRIPT_DIR/../.." && pwd)"
REPORT_DIR="$SCRIPT_DIR/report"
PY="${PYTHON:-python3}"

mkdir -p "$REPORT_DIR"
cd "$ROOT_DIR"

echo "=== [CrossHair] Installing symbolic analysis dependencies ==="
"$PY" -m pip install -q crosshair-tool 2>/dev/null || "$PY" -m pip install -q crosshair-tool

echo ""
echo "=== [CrossHair] Checking analysis fixtures ==="
if "$PY" -m crosshair check analysis/complexity_sample.py \
  > "$REPORT_DIR/crosshair-complexity_sample.txt" 2>&1; then
  echo "CrossHair completed for analysis/complexity_sample.py"
else
  echo "CrossHair reported findings or unavailable runtime for analysis/complexity_sample.py"
fi

if "$PY" -m crosshair check analysis/taint_fixture.py \
  > "$REPORT_DIR/crosshair-taint_fixture.txt" 2>&1; then
  echo "CrossHair completed for analysis/taint_fixture.py"
else
  echo "CrossHair reported findings or unavailable runtime for analysis/taint_fixture.py"
fi

echo ""
echo "=== CrossHair scan complete ==="

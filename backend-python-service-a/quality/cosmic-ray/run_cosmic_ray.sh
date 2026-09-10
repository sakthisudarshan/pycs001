#!/usr/bin/env bash
# run_cosmic_ray.sh — Mutation testing via cosmic-ray for Python service
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(cd "$SCRIPT_DIR/../.." && pwd)"
REPORT_DIR="$SCRIPT_DIR/report"
PY="${PYTHON:-python3}"
SESSION="ce-pycs002"

mkdir -p "$REPORT_DIR"
cd "$ROOT_DIR"

echo "=== [cosmic-ray] Installing mutation dependencies ==="
"$PY" -m pip install -q -r "$ROOT_DIR/requirements.txt" cosmic-ray 2>/dev/null \
  || "$PY" -m pip install -q -r "$ROOT_DIR/requirements.txt" cosmic-ray

cat > "$REPORT_DIR/cosmic-ray.toml" <<'EOF'
[cosmic-ray]
module-path = "analysis/complexity_sample.py"
timeout = 30.0
test-command = "python -m pytest tests/test_complexity.py -q"
excluded-modules = []
EOF

echo ""
echo "=== [cosmic-ray] Initializing mutation session ==="
"$PY" -m cosmic_ray.commands.init "$REPORT_DIR/cosmic-ray.toml" "$SESSION" \
  > "$REPORT_DIR/init.log" 2>&1 || true

echo ""
echo "=== [cosmic-ray] Executing mutation workers ==="
"$PY" -m cosmic_ray.commands.execute "$SESSION" \
  > "$REPORT_DIR/execute.log" 2>&1 || true

echo ""
echo "=== [cosmic-ray] Reporting results ==="
"$PY" -m cosmic_ray.commands.report "$SESSION" \
  > "$REPORT_DIR/cosmic-ray-report.txt" 2>&1 || true

cat "$REPORT_DIR/cosmic-ray-report.txt" 2>/dev/null || echo "cosmic-ray report unavailable"

echo "=== cosmic-ray scan complete ==="

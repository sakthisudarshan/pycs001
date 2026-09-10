#!/usr/bin/env bash
# run_semgrep_bandit.sh — Combined Semgrep OSS + Bandit SAST for Python service
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(cd "$SCRIPT_DIR/../.." && pwd)"
REPORT_DIR="$SCRIPT_DIR/report"
PY="${PYTHON:-python3}"

mkdir -p "$REPORT_DIR"
cd "$ROOT_DIR"

echo "=== [Semgrep OSS + Bandit] Installing SAST dependencies ==="
"$PY" -m pip install -q -r "$ROOT_DIR/requirements.txt" bandit 2>/dev/null \
  || "$PY" -m pip install -q -r "$ROOT_DIR/requirements.txt" bandit

echo ""
echo "=== [Semgrep OSS] Python SAST scan ==="
if command -v semgrep &>/dev/null; then
  semgrep \
    --config p/python \
    --config p/security-audit \
    --json \
    --output "$REPORT_DIR/semgrep-results.json" \
    src/ analysis/ || true

  semgrep \
    --config p/python \
    --config p/security-audit \
    src/ analysis/ || true
else
  echo "semgrep CLI not available; skipping Semgrep OSS stage"
fi

echo ""
echo "=== [Bandit] Python SAST scan ==="
"$PY" -m bandit -r src/ analysis/ \
  -f json -o "$REPORT_DIR/bandit_report.json" || true

"$PY" -m bandit -r src/ analysis/ || true

echo "=== Semgrep OSS + Bandit scan complete ==="

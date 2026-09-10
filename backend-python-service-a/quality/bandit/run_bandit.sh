#!/usr/bin/env bash
# run_bandit.sh — SAST security scanning for Python service
# Tool: bandit
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(cd "$SCRIPT_DIR/../.." && pwd)"
cd "$ROOT_DIR"

mkdir -p quality/bandit/report

echo "=== [bandit] SAST Security Analysis ==="
python -m bandit -r src/ analysis/ \
  -f json -o quality/bandit/report/bandit_report.json || true

python -m bandit -r src/ analysis/ || true

echo "=== Bandit scan complete ==="

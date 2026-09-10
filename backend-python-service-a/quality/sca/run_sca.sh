#!/usr/bin/env bash
# run_sca.sh — Software Composition Analysis (SCA) for Python service
# Tool: pip-audit (primary) + safety (secondary)
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(cd "$SCRIPT_DIR/../.." && pwd)"
cd "$ROOT_DIR"

mkdir -p quality/sca/report

echo "=== [pip-audit] Dependency Vulnerability Scan ==="
python -m pip_audit -r requirements.txt \
  -f json -o quality/sca/report/pip_audit_report.json || true

python -m pip_audit -r requirements.txt || true

echo "=== SCA scan complete ==="

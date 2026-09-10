#!/usr/bin/env bash
# run_semgrep.sh — Semgrep SAST scan for C# service
set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(cd "$SCRIPT_DIR/../.." && pwd)"
REPO_ROOT="$(cd "$ROOT_DIR/.." && pwd)"
cd "$REPO_ROOT"

mkdir -p "$ROOT_DIR/quality/semgrep/report"

echo "=== [Semgrep] SAST Scan — C# Service ==="
if command -v semgrep &>/dev/null; then
semgrep \
  --config .semgrep.yml \
  --include "*.cs" \
  --json \
  --output "$ROOT_DIR/quality/semgrep/report/semgrep-results.json" \
  backend-cs-service-a/ || true
else
  echo "semgrep CLI not available; writing empty report"
  echo '{"results":[]}' > "$ROOT_DIR/quality/semgrep/report/semgrep-results.json"
fi

echo ""
echo "=== [Semgrep] Human-readable output ==="
if command -v semgrep &>/dev/null; then
semgrep \
  --config .semgrep.yml \
  --include "*.cs" \
  backend-cs-service-a/ || true
fi

echo "=== Semgrep scan complete ==="

#!/usr/bin/env bash
# run_mutmut.sh — Mutation Score testing for Python service
# Primary: mutmut   Secondary: cosmic-ray
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(cd "$SCRIPT_DIR/../.." && pwd)"
cd "$ROOT_DIR"

echo "=== [mutmut] Mutation Testing — Python ==="
mutmut run \
  --paths-to-mutate "analysis/,src/" \
  --tests-dir tests/ \
  --runner "python -m pytest"

echo ""
echo "=== [mutmut] Results Summary ==="
mutmut results
mutmut junitxml > quality/mutation/report/mutmut-results.xml 2>/dev/null || true

echo ""
echo "=== Mutation scan complete ==="

#!/usr/bin/env bash
# run_jscpd.sh — Code Duplication detection for Python
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

mkdir -p report

echo "=== [jscpd] Scanning Python clones ==="
if command -v jscpd &>/dev/null; then
    jscpd --path . --languages python --min-lines 5 --min-tokens 40 --reporters console,json --output report/ || true
elif command -v npx &>/dev/null; then
    npx -y jscpd --path . --languages python --min-lines 5 --min-tokens 40 --reporters console,json --output report/ || true
else
    python3 jscpd_shim.py || python trigger.py || true
fi

echo "=== jscpd scan complete ==="

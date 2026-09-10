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
elif python3 -m copydetect --version &>/dev/null; then
    python3 -m copydetect --dir . --extensions py --noise-threshold 20 --guarantee-threshold 40 || true
else
    python trigger.py || true
fi

echo "=== jscpd scan complete ==="

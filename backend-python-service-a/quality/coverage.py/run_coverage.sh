#!/usr/bin/env bash
# run_coverage.sh — Statement + Branch Coverage for Python (coverage.py / pytest-cov)
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
COVERAGE_DIR="$(cd "$SCRIPT_DIR/../coverage" && pwd)"
exec bash "$COVERAGE_DIR/run_coverage.sh"

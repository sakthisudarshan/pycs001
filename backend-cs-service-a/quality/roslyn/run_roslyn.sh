#!/usr/bin/env bash
# run_roslyn.sh — Roslyn SAST lint analysis for C# service
set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(cd "$SCRIPT_DIR/../.." && pwd)"
cd "$ROOT_DIR"

echo "=== [Roslyn] Build with analyzer diagnostics ==="
dotnet build backend-cs-service-a.csproj \
  /p:EnforceCodeStyleInBuild=true \
  /p:AnalysisMode=Recommended \
  /p:EnableNETAnalyzers=true \
  --no-incremental \
  2>&1 | tee quality/roslyn/report/roslyn_output.txt

echo ""
echo "=== [SecurityCodeScan] SAST Roslyn Analyzer ==="
grep -E "(warning|error) SCS" quality/roslyn/report/roslyn_output.txt || echo "No SCS findings in output"

echo "=== Roslyn scan complete ==="

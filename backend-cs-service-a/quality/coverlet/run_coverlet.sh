#!/usr/bin/env bash
# run_coverlet.sh — Statement + Branch + Delta Coverage for C# service
set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(cd "$SCRIPT_DIR/../.." && pwd)"
TESTS_DIR="$(cd "$ROOT_DIR/../backend-cs-service-a.Tests" && pwd)"
cd "$TESTS_DIR"

mkdir -p "$ROOT_DIR/quality/coverlet/report"

echo "=== [Coverlet] Statement + Branch Coverage ==="
dotnet test \
  --collect:"XPlat Code Coverage" \
  -- DataCollectionRunSettings.DataCollectors.DataCollector.Configuration.Format=cobertura \
  -- DataCollectionRunSettings.DataCollectors.DataCollector.Configuration.Include="[BackendCsServiceA*]*" \
  -- DataCollectionRunSettings.DataCollectors.DataCollector.Configuration.Exclude="[*.Tests]*" \
  -- DataCollectionRunSettings.DataCollectors.DataCollector.Configuration.BranchesThreshold=75 \
  -- DataCollectionRunSettings.DataCollectors.DataCollector.Configuration.LineThreshold=80

echo ""
echo "=== [Coverlet] MSBuild with threshold enforcement ==="
dotnet test \
  /p:CollectCoverage=true \
  /p:CoverletOutputFormat=cobertura \
  /p:CoverletOutput="$ROOT_DIR/quality/coverlet/report/coverage.xml" \
  /p:BranchesThreshold=75 \
  /p:LineThreshold=80 \
  /p:Include="[BackendCsServiceA*]*" \
  /p:Exclude="[*.Tests]*"

echo "=== Coverlet scan complete ==="

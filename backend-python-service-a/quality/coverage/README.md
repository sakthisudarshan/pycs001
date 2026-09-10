# Coverage Trigger Fixture

## Overview
This tool fixture triggers **Coverage.py** and **pytest-cov** to measure:
- Statement Coverage %
- Branch Coverage %
- Path Coverage %
- Coverage Delta %

## Execution
Run via bash runner:
```bash
bash quality/coverage/run_coverage.sh
```
Or run directly via native Python runner:
```bash
python quality/coverage/trigger.py
```
Outputs are stored in `quality/coverage/report/`.

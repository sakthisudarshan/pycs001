# Code Duplication Trigger Fixture

## Overview
Detects source code clones and duplication metrics via **jscpd** (primary) and **copydetect** (secondary).

## Execution
Run via bash runner:
```bash
bash quality/jscpd/run_jscpd.sh
```
Or run directly via native Python runner:
```bash
python quality/jscpd/trigger.py
```
Reports are written to `quality/jscpd/report/`.

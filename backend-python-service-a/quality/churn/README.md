# Code Churn Trigger Fixture

## Overview
Calculates code churn metrics (lines added, lines deleted, churn frequency, and file instability) using **PyDriller**.

## Execution
Run via bash runner:
```bash
bash quality/churn/run_churn.sh
```
Or run directly via native Python runner:
```bash
python quality/churn/trigger.py
```
Reports are output to `quality/churn/report/churn_report.json`.

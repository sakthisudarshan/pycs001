# All-Uses & Definition Coverage Trigger Fixture

## Overview
Analyzes Definition-Use chains, Computational Use (C-Use), Predicate Use (P-Use), and Unreachable Use detection using **beniget** and **pyflakes** combined with **Coverage.py**.

## Execution
Run via bash runner:
```bash
bash quality/all_uses/run_all_uses.sh
```
Or run directly via native Python runner:
```bash
python quality/all_uses/trigger.py
```
Reports are written to `quality/all_uses/report/`.

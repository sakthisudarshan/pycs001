# Mutation Testing Trigger Fixture

## Overview
Assesses test suite sensitivity, mutation kill rate, and test rigor via **mutmut** (primary) and **cosmic-ray** (secondary).

## Execution
Run via bash runner:
```bash
bash quality/mutation/run_mutmut.sh
```
Or run directly via native Python runner:
```bash
python quality/mutation/trigger.py
```
Output results are written to `quality/mutation/report/`.

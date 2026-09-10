# Bandit SAST Trigger Fixture

## Overview
Scans for common security flaws, injection vulnerabilities, weak cryptography, and hardcoded secrets using **Bandit**.

## Execution
Run via bash runner:
```bash
bash quality/bandit/run_bandit.sh
```
Or run directly via native Python runner:
```bash
python quality/bandit/trigger.py
```
Reports are output to `quality/bandit/report/bandit_report.json`.

# Software Composition Analysis (SCA) Trigger Fixture

## Overview
Scans Python package dependencies in `requirements.txt` for known Common Vulnerabilities and Exposures (CVEs) using **pip-audit** and **safety**.

## Execution
Run via bash runner:
```bash
bash quality/sca/run_sca.sh
```
Or run directly via native Python runner:
```bash
python quality/sca/trigger.py
```
Reports are output to `quality/sca/report/pip_audit_report.json`.

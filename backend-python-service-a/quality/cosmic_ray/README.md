# Cosmic Ray Quality Trigger

This folder contains the quality trigger for **Cosmic Ray** mutation testing on Python 3.11+.

## Structure
- `trigger.yaml` — Tool configuration metadata (`tool: Cosmic Ray`).
- `cosmic-ray.toml` — Cosmic Ray configuration file specifying target module (`analysis.complexity_sample`).
- `trigger.py` — Pure Python trigger script executing Cosmic Ray mutation testing and generating `report/cosmic-ray-report.json`.

## Run Command
```bash
python quality/cosmic_ray/trigger.py
```

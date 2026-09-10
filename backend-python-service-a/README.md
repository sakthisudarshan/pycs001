# Backend Python Service A

FastAPI and gRPC backend service for the CE Platform Stack, built with Python 3.11+.

## Architecture & Responsibilities
- **Framework**: FastAPI (REST endpoints) + gRPC Servicer (`grpcio`)
- **Database**: MongoDB via `pymongo`
- **Quality Tooling**: Built-in test suite, coverage, mutation testing, AST data-flow analysis, SAST, and code churn analysis.

## Build & Dependencies
This project provides both standard Pip and UV package management configurations:
- `pyproject.toml` (standard PEP 621 configuration)
- `requirements.txt` (standard pip requirements)
- `uv.lock` (UV lockfile)

### Running Locally
```bash
# Install dependencies
pip install -r requirements.txt
# Or using uv:
uv sync

# Run tests with coverage
pytest tests/ --cov=src --cov=analysis --cov-branch -v
```

## Quality Tool Triggers
All quality tool fixtures and automated triggers are located in the `quality/` directory:
- `quality/coverage/`: Coverage.py statement, branch, path, and delta coverage.
- `quality/jscpd/`: Code duplication detection via jscpd / copydetect.
- `quality/mutation/`: Mutation testing via mutmut / cosmic-ray.
- `quality/all_uses/`: Definition-use chain and data-flow coverage via beniget + pyflakes.
- `quality/bandit/`: Security AST static analysis (SAST) via bandit.
- `quality/churn/`: Git commit history code churn analysis via pydriller.
- `quality/sca/`: Dependency vulnerability scanning (SCA) via pip-audit.

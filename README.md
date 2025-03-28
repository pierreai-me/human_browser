# human_browser
A human browsing the Internets

## Setup

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements-dev.in
pip install -e .
```

## Test

```bash
python -m pytest -vv tests/
```
# Installation

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -U pip setuptools
pip install -U -r requirenments.txt
```

Or use the provided script:

```bash
bash pip_install.sh
```

# Usage

```bash
python3 main.py
```

# Development

Pre-commit hooks (ruff + mypy) are configured:

```bash
pre-commit install
pre-commit run --all-files
```

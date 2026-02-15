# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Setup

```bash
bash pip_install.sh          # Create .venv and install dependencies
source .venv/bin/activate
pre-commit install            # Install git hooks
```

Copy `env_example` to `.env` and fill in the required values before running.

## Commands

```bash
python3 main.py               # Run the example entry point
pre-commit run --all-files    # Run all linters (Ruff + MyPy)
bash purge_cache.sh           # Clean __pycache__, .mypy_cache, .ruff_cache, etc.
```

No test suite is defined — pre-commit hooks are the primary quality gate.

## Architecture

This is a small Python library for type-safe environment variable loading. Three files form the core:

- **`settings.py`** — Pydantic `BaseModel` defining the config schema. Required fields: `APP_NAME`, `PORT`, `SECRET_KEY`, `DATABASE_URL`. Optional: `DEBUG` (default `False`). `PORT` is validated as 0 < port < 65536.
- **`env_loader.py`** — Loads `.env` via `python-dotenv`, validates against `Settings` using `model_validate()`, provides attribute access via `__getattr__`, and masks `SECRET_*` values in logs.
- **`main.py`** — Usage example; instantiates `EnvLoader` and prints config values.

Pydantic v2 is used throughout. MyPy is configured with strict settings (see `mypy.ini`) and the Pydantic plugin enabled. Ruff handles formatting, import sorting, and linting (configured in `pyproject.toml`).

## Redis

Redis runs in Docker via `docker-compose.yml` (image `redis:7-alpine`, port `6379`).

```bash
docker compose up -d          # start Redis
docker compose down           # stop Redis
```

- **`redis_client.py`** — `RedisClient` async context manager wrapping `redis.asyncio`. Supports strings, hashes, lists, sets, and pub/sub. Uses `decode_responses=True` so all values are `str`.
- **`settings.py`** — `REDIS_URL` field (default `redis://localhost:6379/0`).

`redis[hiredis]` (v5+) is required — `hiredis` is the C parser for faster decoding. Install with `pip install -U -r requirements.txt`.

#!/bin/bash
set -euo pipefail

# -----------------------------------------------------------------------------
find . -type d -name '__pycache__' -print0 | xargs -r0 rm -rf
find . -type d -name '.mypy_cache' -print0 | xargs -r0 rm -rf
find . -type d -name '.pytest_cache' -print0 | xargs -r0 rm -rf
find . -type d -name '.ruff_cache' -print0 | xargs -r0 rm -rf
find . -type f -name '.coverage' -print0 | xargs -r0 rm -rf

# -----------------------------------------------------------------------------
exit 0

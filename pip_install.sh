#!/bin/bash
set -euo pipefail

# -----------------------------------------------------------------------------
REQUIREMENTS_FILE="${1:-requirements.txt}"

# -----------------------------------------------------------------------------
python3 -m venv ./.venv
source ./.venv/bin/activate

pip install -U pip setuptools
pip install -U -r "$REQUIREMENTS_FILE"

echo
echo "Installed packages:"
echo "-------------------------------------------------------------------------------"
pip list
echo "-------------------------------------------------------------------------------"
# pip cache purge

# -----------------------------------------------------------------------------
echo
echo "All python packages are successfully installed"
exit 0

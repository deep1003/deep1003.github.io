#!/bin/zsh
set -euo pipefail

HERE="${0:A:h}"
cd "$HERE"

PYTHON="python3"
if [[ -x /opt/anaconda3/bin/python ]]; then
  PYTHON="/opt/anaconda3/bin/python"
fi

if ! "$PYTHON" -c 'import jupyterlab, pandas, pyarrow, matplotlib, pycountry' >/dev/null 2>&1; then
  echo "Installing the local notebook dependencies..."
  "$PYTHON" -m pip install --user jupyterlab pandas pyarrow matplotlib pycountry
fi

echo "Opening the full-census audit notebook in the local web browser."
exec "$PYTHON" -m jupyter lab \
  --notebook-dir="$HERE" \
  "$HERE/policycommons_full_census_audit.ipynb"

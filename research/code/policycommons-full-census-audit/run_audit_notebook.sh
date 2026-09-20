#!/bin/zsh
set -euo pipefail

HERE="${0:A:h}"
cd "$HERE"

PYTHON="python3"
if [[ -x /opt/anaconda3/bin/python ]]; then
  PYTHON="/opt/anaconda3/bin/python"
fi

if ! "$PYTHON" -c 'import nbconvert, pandas, pyarrow, matplotlib, pycountry' >/dev/null 2>&1; then
  "$PYTHON" -m pip install --user jupyter nbconvert pandas pyarrow matplotlib pycountry
fi

"$PYTHON" -m jupyter nbconvert \
  --to notebook \
  --execute "$HERE/policycommons_full_census_audit.ipynb" \
  --output "$HERE/policycommons_full_census_audit_executed.ipynb" \
  --ExecutePreprocessor.timeout=1800

echo "Executed notebook: $HERE/policycommons_full_census_audit_executed.ipynb"

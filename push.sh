#!/usr/bin/env bash
# Commit and push the personal site.
# Usage:  ./push.sh "commit message"
#         ./push.sh            (uses a default message)

set -euo pipefail

REPO="/Users/deep1003/data3/deep1003.github.io"
cd "$REPO"

MSG="${1:-Update site content ($(date +%Y-%m-%d))}"

if [[ -z "$(git status --porcelain)" ]]; then
  echo "Nothing to commit. Working tree is clean."
  exit 0
fi

echo "--- Changes to be committed ---"
git status --short
echo

git add -A
git commit -m "$MSG"
git push origin "$(git rev-parse --abbrev-ref HEAD)"

echo
echo "Pushed. GitHub Pages usually rebuilds within a minute:"
echo "  https://deep1003.github.io/"

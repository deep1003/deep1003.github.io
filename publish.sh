#!/usr/bin/env bash
#
# publish.sh — stage, commit, push and verify a deployment of this site.
#
#   ./publish.sh                          commit everything with a generated message
#   ./publish.sh "Add note on RUM-NN"     commit everything with your own message
#   ./publish.sh -y "message"             skip the confirmation prompt
#   ./publish.sh -n                       dry run: show what would happen, change nothing
#   ./publish.sh --no-verify "message"    push without waiting for the live site
#
# The script refuses to do anything surprising: it shows you the file list and
# the diff summary first, blocks obviously wrong commits (very large files,
# PDFs, stray secrets), and after pushing it polls the live site until the
# deployed bytes match what you committed — GitHub Pages needs a minute or two
# to rebuild and its CDN caches for longer, so "I pushed but the page is old"
# is normal rather than a failure.
#
set -euo pipefail

SITE_URL="https://deep1003.github.io"
VERIFY_TIMEOUT=420          # seconds to wait for the live site to catch up
VERIFY_INTERVAL=15          # seconds between polls
WARN_FILE_MB=5              # warn above this size
BLOCK_FILE_MB=50            # refuse above this size (GitHub's hard warning level)

# ── pretty output ────────────────────────────────────────────────────────────
if [ -t 1 ]; then
  B=$'\033[1m'; DIM=$'\033[2m'; R=$'\033[31m'; G=$'\033[32m'; Y=$'\033[33m'; X=$'\033[0m'
else
  B=""; DIM=""; R=""; G=""; Y=""; X=""
fi
info() { printf '%s\n' "$*"; }
step() { printf '%s\n' "${B}$*${X}"; }
warn() { printf '%s\n' "${Y}warning:${X} $*" >&2; }
die()  { printf '%s\n' "${R}error:${X} $*" >&2; exit 1; }

# ── options ──────────────────────────────────────────────────────────────────
ASSUME_YES=0; DRY_RUN=0; DO_VERIFY=1; MESSAGE=""
while [ $# -gt 0 ]; do
  case "$1" in
    -y|--yes)        ASSUME_YES=1 ;;
    -n|--dry-run)    DRY_RUN=1 ;;
    --no-verify)     DO_VERIFY=0 ;;
    -h|--help)       sed -n '2,20p' "$0" | sed 's/^# \{0,1\}//'; exit 0 ;;
    -*)              die "unknown option: $1" ;;
    *)               MESSAGE="$1" ;;
  esac
  shift
done

# ── locate the repository (works from any directory) ─────────────────────────
cd "$(dirname "${BASH_SOURCE[0]}")"
git rev-parse --is-inside-work-tree >/dev/null 2>&1 || die "not a git repository: $PWD"
cd "$(git rev-parse --show-toplevel)"
BRANCH="$(git symbolic-ref --quiet --short HEAD)" || die "detached HEAD — check out a branch first"

step "Repository"
info "  path    $PWD"
info "  branch  $BRANCH"

# git needs an identity before it will let you commit
if ! git config user.email >/dev/null 2>&1; then
  info ""
  info "  Git does not know who you are yet. Set it once:"
  info "    git config --global user.name  \"Youngsam Chun\""
  info "    git config --global user.email \"deep1003@snu.ac.kr\""
  die "git identity is not configured."
fi
info "  author  $(git config user.name) <$(git config user.email)>"

# ── is there anything to do? ─────────────────────────────────────────────────
git add -A

if git diff --cached --quiet; then
  if [ -n "$(git log --oneline "@{upstream}"..HEAD 2>/dev/null || true)" ]; then
    warn "nothing new to commit, but local commits are not pushed yet — pushing those."
    MESSAGE=""          # nothing to commit; fall through to the push
  else
    info "${G}Nothing to publish — the working tree is clean and up to date.${X}"
    exit 0
  fi
fi

# ── safety checks on what is about to be committed ───────────────────────────
STAGED="$(git diff --cached --name-only --diff-filter=ACM)"

if [ -n "$STAGED" ]; then
  step "Checks"
  problems=0
  while IFS= read -r f; do
    [ -f "$f" ] || continue
    bytes=$(wc -c < "$f" | tr -d ' ')
    mb=$(( bytes / 1048576 ))
    if [ "$mb" -ge "$BLOCK_FILE_MB" ]; then
      warn "${f} is ${mb} MB — too large for a Pages repository. Remove it or add it to .gitignore."
      problems=$((problems + 1))
    elif [ "$mb" -ge "$WARN_FILE_MB" ]; then
      warn "${f} is ${mb} MB. Consider compressing it."
    fi
    case "$f" in
      *.pdf) warn "${f} is a PDF. Only commit PDFs you have the right to redistribute." ;;
    esac
  done <<< "$STAGED"

  # never publish credentials by accident
  if echo "$STAGED" | grep -qiE '(^|/)(\.env|id_rsa|id_ed25519|.*\.pem|.*\.key|.*credential.*|.*secret.*)$'; then
    die "a file that looks like a credential is staged. Unstage it before publishing."
  fi

  [ "$problems" -gt 0 ] && die "$problems blocking issue(s) above. Nothing was committed."
  info "  ${G}ok${X} — no oversized files or credentials staged"

  step "Changes"
  git diff --cached --stat | sed 's/^/  /'
fi

# ── compose the commit message ───────────────────────────────────────────────
if [ -n "$STAGED" ] && [ -z "$MESSAGE" ]; then
  # A new note is the common case: name it directly.
  NEW_NOTE="$(git diff --cached --name-only --diff-filter=A \
              | grep -oE '^notes/[0-9]{4}-[0-9]{2}-[0-9]{2}-[^/]+/index\.html$' \
              | head -1 || true)"
  if [ -n "$NEW_NOTE" ]; then
    SLUG="$(printf '%s' "$NEW_NOTE" | sed -E 's#^notes/[0-9-]{11}##; s#/index\.html$##; s/-/ /g')"
    MESSAGE="Add research note: ${SLUG}"
  else
    COUNT="$(printf '%s\n' "$STAGED" | grep -c . || true)"
    # name the top-level areas touched; files at the repo root count as "site"
    AREA="$(printf '%s\n' "$STAGED" \
            | awk -F/ '{ print (NF > 1 ? $1 : "site") }' \
            | sort -u | paste -sd', ' -)"
    if [ "$COUNT" -eq 1 ]; then
      MESSAGE="Update $(printf '%s' "$STAGED")"
    else
      MESSAGE="Update ${AREA} (${COUNT} files)"
    fi
  fi
  info ""
  info "  commit message ${DIM}(generated)${X}: ${B}${MESSAGE}${X}"
  info "  ${DIM}pass your own as an argument: ./publish.sh \"your message\"${X}"
fi

# ── confirm ──────────────────────────────────────────────────────────────────
if [ "$DRY_RUN" -eq 1 ]; then
  info ""
  info "${Y}Dry run — nothing was committed or pushed.${X}"
  git reset --quiet
  exit 0
fi

if [ "$ASSUME_YES" -eq 0 ]; then
  info ""
  printf 'Commit and push to %s? [y/N] ' "$BRANCH"
  # Read from stdin: that is the terminal in normal interactive use, and a pipe
  # when the script is driven by another script. End of input means "no", so the
  # script can never hang or crash where there is nothing to read.
  reply=""
  read -r reply || info "(no input — treating as no; use -y to skip this prompt)"
  case "$reply" in
    [yY]|[yY][eE][sS]) ;;
    *) git reset --quiet; info "Aborted — the working tree was left unstaged."; exit 1 ;;
  esac
fi

# ── commit and push ──────────────────────────────────────────────────────────
if [ -n "$STAGED" ]; then
  step "Committing"
  git commit -q -m "$MESSAGE"
  git log --oneline -1 | sed 's/^/  /'
fi

step "Pushing"
git push origin "$BRANCH"
HEAD_SHA="$(git rev-parse --short HEAD)"

# ── verify the deployment ────────────────────────────────────────────────────
# GitHub Pages serves files byte for byte, so comparing a checksum of a changed
# HTML file against the same file fetched over HTTP tells us whether the build
# has actually landed. Only meaningful for files that are served.
if [ "$DO_VERIFY" -eq 1 ]; then
  PROBE="$(git show --name-only --diff-filter=ACM --pretty=format: HEAD \
           | grep -E '\.html$' | grep -v '^notes/_TEMPLATE\.html$' | head -1 || true)"

  if [ -z "$PROBE" ] || ! command -v curl >/dev/null 2>&1; then
    info ""
    info "${G}Pushed ${HEAD_SHA}.${X} The site rebuilds in a minute or two."
    info "  ${SITE_URL}/notes/"
    exit 0
  fi

  # index.html is served at the directory URL
  URL_PATH="$(printf '%s' "$PROBE" | sed 's#\(^\|/\)index\.html$#\1#')"
  PROBE_URL="${SITE_URL}/${URL_PATH}"
  LOCAL_SUM="$(git show "HEAD:${PROBE}" | shasum -a 256 | cut -d' ' -f1)"

  step "Verifying deployment"
  info "  probe   ${PROBE_URL}"
  info "  ${DIM}waiting for the Pages build and CDN cache (up to $((VERIFY_TIMEOUT / 60)) min)${X}"

  elapsed=0
  while [ "$elapsed" -lt "$VERIFY_TIMEOUT" ]; do
    sleep "$VERIFY_INTERVAL"
    elapsed=$((elapsed + VERIFY_INTERVAL))
    LIVE_SUM="$(curl -fsSL -H 'Cache-Control: no-cache' -H 'Pragma: no-cache' \
                "${PROBE_URL}?cb=${HEAD_SHA}$(date +%s)" 2>/dev/null \
                | shasum -a 256 | cut -d' ' -f1 || true)"
    if [ "$LIVE_SUM" = "$LOCAL_SUM" ]; then
      info ""
      info "${G}Live — ${HEAD_SHA} is deployed.${X} (${elapsed}s)"
      info "  ${SITE_URL}/notes/"
      exit 0
    fi
    printf '  %ss…\n' "$elapsed"
  done

  info ""
  warn "the live page still differs after $((VERIFY_TIMEOUT / 60)) minutes."
  info "  The push itself succeeded (${HEAD_SHA}). Either the build is queued or the"
  info "  CDN is still holding the old copy. Check the build log at:"
  info "    https://github.com/deep1003/deep1003.github.io/actions"
  info "  Then hard-reload the page (Cmd+Shift+R)."
  exit 0
fi

info ""
info "${G}Pushed ${HEAD_SHA}.${X} Verification skipped."
info "  ${SITE_URL}/notes/"

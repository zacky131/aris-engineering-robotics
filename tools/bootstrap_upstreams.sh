#!/usr/bin/env bash
# bootstrap_upstreams.sh — Fetch missing upstream dependency repositories.
#
# This script clones ARIS and Engineering Paper Skills into vendor/upstreams/
# if they are not already available as siblings or env-variable-specified paths.
#
# Usage:
#   bash tools/bootstrap_upstreams.sh
#   bash tools/bootstrap_upstreams.sh --check   # check without cloning

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

VENDOR_DIR="$REPO_ROOT/vendor/upstreams"
CHECK_ONLY=false

while [[ $# -gt 0 ]]; do
  case "$1" in
    --check) CHECK_ONLY=true; shift ;;
    *) echo "Unknown argument: $1"; exit 1 ;;
  esac
done

ARIS_URL="https://github.com/wanshuiyin/Auto-claude-code-research-in-sleep.git"
EPS_URL="https://github.com/engineering-paper-skills/engineering-paper-skills.git"

ARIS_SIBLING="$(cd "$REPO_ROOT/../Auto-claude-code-research-in-sleep" 2>/dev/null && pwd || echo "")"
EPS_SIBLING="$(cd "$REPO_ROOT/../engineering-paper-skills" 2>/dev/null && pwd || echo "")"

ARIS_VENDOR="$VENDOR_DIR/aris"
EPS_VENDOR="$VENDOR_DIR/engineering-paper-skills"

echo "=== ARIS Engineering Robotics — Upstream Bootstrap ==="
echo ""

# ── ARIS ─────────────────────────────────────────────────────────────────────
echo "--- ARIS (Auto-claude-code-research-in-sleep) ---"

if [[ -n "${ARIS_REPO:-}" && -d "$ARIS_REPO/skills" ]]; then
  echo "  STATUS: available via ARIS_REPO env var at $ARIS_REPO"
elif [[ -n "$ARIS_SIBLING" && -d "$ARIS_SIBLING/skills" ]]; then
  echo "  STATUS: available as sibling at $ARIS_SIBLING"
elif [[ -d "$ARIS_VENDOR/skills" ]]; then
  echo "  STATUS: available via vendor cache at $ARIS_VENDOR"
else
  echo "  STATUS: NOT FOUND"
  if $CHECK_ONLY; then
    echo "  ACTION NEEDED: clone $ARIS_URL"
    echo "         into $ARIS_VENDOR"
    echo "         or set: export ARIS_REPO=/path/to/Auto-claude-code-research-in-sleep"
  else
    echo "  Cloning into $ARIS_VENDOR ..."
    mkdir -p "$VENDOR_DIR"
    git clone --depth=1 "$ARIS_URL" "$ARIS_VENDOR"
    echo "  DONE: ARIS cloned to $ARIS_VENDOR"
  fi
fi

echo ""

# ── EPS ──────────────────────────────────────────────────────────────────────
echo "--- Engineering Paper Skills ---"

if [[ -n "${EPS_REPO:-}" && -d "$EPS_REPO/skills" ]]; then
  echo "  STATUS: available via EPS_REPO env var at $EPS_REPO"
elif [[ -n "$EPS_SIBLING" && -d "$EPS_SIBLING/skills" ]]; then
  echo "  STATUS: available as sibling at $EPS_SIBLING"
elif [[ -d "$EPS_VENDOR/skills" ]]; then
  echo "  STATUS: available via vendor cache at $EPS_VENDOR"
else
  echo "  STATUS: NOT FOUND"
  if $CHECK_ONLY; then
    echo "  ACTION NEEDED: clone $EPS_URL"
    echo "         into $EPS_VENDOR"
    echo "         or set: export EPS_REPO=/path/to/engineering-paper-skills"
  else
    echo "  Cloning into $EPS_VENDOR ..."
    mkdir -p "$VENDOR_DIR"
    git clone --depth=1 "$EPS_URL" "$EPS_VENDOR"
    echo "  DONE: EPS cloned to $EPS_VENDOR"
  fi
fi

echo ""
echo "=== Bootstrap complete ==="
echo ""
echo "Next step:"
echo "  bash tools/install_skills.sh --platform antigravity --project /path/to/project"

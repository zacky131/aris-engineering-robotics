#!/usr/bin/env bash
# sync_upstreams.sh — Pull latest changes from upstream repos (read-only).

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

ARIS_REPO="${ARIS_REPO:-$(cd "$REPO_ROOT/../Auto-claude-code-research-in-sleep" 2>/dev/null && pwd || echo "")}"
EPS_REPO="${EPS_REPO:-$(cd "$REPO_ROOT/../engineering-paper-skills" 2>/dev/null && pwd || echo "")}"

echo "=== Syncing upstream repositories ==="

if [[ -d "$ARIS_REPO/.git" ]]; then
  echo "Pulling ARIS..."
  git -C "$ARIS_REPO" pull --ff-only
else
  echo "SKIP: ARIS repo not found or not a git repo"
fi

if [[ -d "$EPS_REPO/.git" ]]; then
  echo "Pulling EPS..."
  git -C "$EPS_REPO" pull --ff-only
else
  echo "SKIP: EPS repo not found or not a git repo"
fi

echo ""
echo "Done. Re-run install_skills.sh to update installed skills."

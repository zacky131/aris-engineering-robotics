#!/usr/bin/env bash
# uninstall_skills.sh — Remove skills installed by install_skills.sh

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
MANIFEST="$REPO_ROOT/.aris-engineering-robotics/installed-skills.txt"

if [[ ! -f "$MANIFEST" ]]; then
  echo "No manifest found at $MANIFEST — nothing to uninstall."
  exit 0
fi

echo "=== ARIS Engineering Robotics — Uninstall ==="
echo ""

while IFS= read -r path; do
  if [[ -z "$path" ]]; then continue; fi
  if [[ -d "$path" ]]; then
    echo "  REMOVING: $path"
    rm -rf "$path"
  else
    echo "  SKIP (not found): $path"
  fi
done < "$MANIFEST"

rm -f "$MANIFEST"
echo ""
echo "Uninstall complete. Manifest cleared."

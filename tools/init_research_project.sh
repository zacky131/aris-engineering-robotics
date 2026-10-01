#!/usr/bin/env bash
# init_research_project.sh — Initialize an ARIS Engineering Robotics project structure
#
# Usage:
#   bash tools/init_research_project.sh /path/to/project
#   bash tools/init_research_project.sh --project /path/to/project
#
# This script creates the recommended research directory layout including
# anchor_papers/ and research/ directories, and copies initial templates
# without overwriting any existing user files.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

TARGET_DIR=""

while [[ $# -gt 0 ]]; do
  case "$1" in
    --project)
      TARGET_DIR="$2"
      shift 2
      ;;
    -h|--help)
      echo "Usage: bash tools/init_research_project.sh [OPTIONS] <TARGET_DIR>"
      echo ""
      echo "Options:"
      echo "  --project DIR    Target project directory (or provide as first positional argument)"
      echo "  -h, --help       Show this help message"
      exit 0
      ;;
    *)
      if [[ -z "$TARGET_DIR" ]]; then
        TARGET_DIR="$1"
        shift
      else
        echo "Unknown argument: $1"
        exit 1
      fi
      ;;
  esac
done

if [[ -z "$TARGET_DIR" ]]; then
  echo "ERROR: Target directory is required."
  echo "Usage: bash tools/init_research_project.sh /path/to/project"
  exit 1
fi

TARGET_DIR="$(mkdir -p "$TARGET_DIR" && cd "$TARGET_DIR" && pwd)"
echo "Initializing ARIS research project in: $TARGET_DIR"

# 1. Create anchor_papers directories
mkdir -p "$TARGET_DIR/anchor_papers/foundational"
mkdir -p "$TARGET_DIR/anchor_papers/closest_work"
mkdir -p "$TARGET_DIR/anchor_papers/methodology"
mkdir -p "$TARGET_DIR/anchor_papers/benchmark"
mkdir -p "$TARGET_DIR/anchor_papers/uncategorized"
mkdir -p "$TARGET_DIR/research"

# 2. Copy anchor_papers README and .gitkeep if missing
if [[ ! -f "$TARGET_DIR/anchor_papers/README.md" && -f "$REPO_ROOT/templates/anchor_papers/README.md" ]]; then
  cp "$REPO_ROOT/templates/anchor_papers/README.md" "$TARGET_DIR/anchor_papers/README.md"
  echo "  Created: anchor_papers/README.md"
else
  echo "  Preserved: anchor_papers/README.md (already exists or template missing)"
fi

for cat in foundational closest_work methodology benchmark uncategorized; do
  if [[ ! -f "$TARGET_DIR/anchor_papers/$cat/.gitkeep" ]]; then
    touch "$TARGET_DIR/anchor_papers/$cat/.gitkeep"
  fi
done

# 3. Copy starter templates only if they do not exist
copy_if_missing() {
  local src="$1"
  local dest="$2"
  local rel_name="$3"
  if [[ ! -f "$dest" ]]; then
    if [[ -f "$src" ]]; then
      cp "$src" "$dest"
      echo "  Created: $rel_name"
    fi
  else
    echo "  Preserved: $rel_name (already exists)"
  fi
}

copy_if_missing "$REPO_ROOT/templates/EXPERIMENT.yaml" "$TARGET_DIR/EXPERIMENT.yaml" "EXPERIMENT.yaml"
copy_if_missing "$REPO_ROOT/templates/EVIDENCE_LEDGER.yaml" "$TARGET_DIR/EVIDENCE_LEDGER.yaml" "EVIDENCE_LEDGER.yaml"
copy_if_missing "$REPO_ROOT/templates/CLAIM_MAP.yaml" "$TARGET_DIR/CLAIM_MAP.yaml" "CLAIM_MAP.yaml"
copy_if_missing "$REPO_ROOT/templates/RESEARCH_CONTRACT.md" "$TARGET_DIR/RESEARCH_CONTRACT.md" "RESEARCH_CONTRACT.md"

echo ""
echo "ARIS research project initialized successfully."
echo "Next steps:"
echo "  1. Drop starting papers into anchor_papers/ (e.g. anchor_papers/closest_work/)"
echo "  2. Run 'anchor-paper-intake' or 'robotics-research-router'"

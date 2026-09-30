#!/usr/bin/env bash
# install_skills.sh — Install ARIS Engineering Robotics skills
# Usage:
#   bash tools/install_skills.sh --platform codex
#   bash tools/install_skills.sh --platform codex --project /path/to/project
#   bash tools/install_skills.sh --platform claude
#   bash tools/install_skills.sh --platform codex --dry-run

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
CONFIG="$REPO_ROOT/.aris-engineering-robotics/config.yaml"

# ── Argument parsing ─────────────────────────────────────────────────────────
PLATFORM=""
PROJECT_DIR=""
DRY_RUN=false

while [[ $# -gt 0 ]]; do
  case "$1" in
    --platform) PLATFORM="$2"; shift 2 ;;
    --project)  PROJECT_DIR="$2"; shift 2 ;;
    --dry-run)  DRY_RUN=true; shift ;;
    *) echo "Unknown argument: $1"; exit 1 ;;
  esac
done

if [[ -z "$PLATFORM" ]]; then
  echo "ERROR: --platform is required. Supported: codex, claude"
  exit 1
fi

# ── Resolve upstream paths ───────────────────────────────────────────────────
ARIS_REPO="${ARIS_REPO:-$(cd "$REPO_ROOT/../Auto-claude-code-research-in-sleep" 2>/dev/null && pwd || echo "")}"
EPS_REPO="${EPS_REPO:-$(cd "$REPO_ROOT/../engineering-paper-skills" 2>/dev/null && pwd || echo "")}"

echo "=== ARIS Engineering Robotics — Skill Installer ==="
echo "Platform : $PLATFORM"
echo "Dry run  : $DRY_RUN"
echo "ARIS repo: $ARIS_REPO"
echo "EPS repo : $EPS_REPO"
echo ""

# ── Resolve install destination ──────────────────────────────────────────────
case "$PLATFORM" in
  codex)
    if [[ -n "$PROJECT_DIR" ]]; then
      DEST="$PROJECT_DIR/.codex/skills"
    else
      DEST="$HOME/.codex/skills"
    fi
    ;;
  claude)
    if [[ -n "$PROJECT_DIR" ]]; then
      DEST="$PROJECT_DIR/.claude/skills"
    else
      DEST="$HOME/.claude/skills"
    fi
    ;;
  *)
    echo "ERROR: Unknown platform '$PLATFORM'. Supported: codex, claude"
    exit 1
    ;;
esac

echo "Install destination: $DEST"
echo ""

# ── Verify upstream repos ────────────────────────────────────────────────────
MISSING=0
if [[ -z "$ARIS_REPO" || ! -d "$ARIS_REPO/skills" ]]; then
  echo "WARNING: ARIS repo not found at expected location. ARIS skills will be skipped."
  MISSING=1
fi

if [[ -z "$EPS_REPO" || ! -d "$EPS_REPO/skills" ]]; then
  echo "WARNING: EPS repo not found at expected location. EPS skills will be skipped."
  MISSING=1
fi

# ── Helper: install a skill ──────────────────────────────────────────────────
MANIFEST_FILE="$REPO_ROOT/.aris-engineering-robotics/installed-skills.txt"
MANIFEST_NEW=""

install_skill() {
  local src="$1"
  local name
  name="$(basename "$src")"
  local dst="$DEST/$name"

  if [[ ! -d "$src" ]]; then
    echo "  SKIP (not found): $name"
    return
  fi

  if $DRY_RUN; then
    echo "  DRY-RUN: would copy $name  →  $dst"
  else
    mkdir -p "$DEST"
    cp -r "$src" "$dst"
    echo "  INSTALLED: $name"
    MANIFEST_NEW+="$dst\n"
  fi
}

# ── Install new robotics skills ──────────────────────────────────────────────
echo "--- Installing new robotics skills ---"
for skill_dir in "$REPO_ROOT/skills"/*/; do
  install_skill "$skill_dir"
done

# ── Install ARIS upstream skills ─────────────────────────────────────────────
ARIS_SKILLS=(
  research-lit idea-discovery idea-discovery-robot novelty-check
  experiment-plan research-implement-feature run-experiment
  monitor-experiment training-check analyze-results ablation-planner
  experiment-audit result-to-claim paper-writing paper-claim-audit
  research-review rebuttal paper-compile research-pipeline dse-loop
  claims-drafting paper-write citation-audit formula-derivation
)

if [[ -d "$ARIS_REPO/skills" ]]; then
  echo ""
  echo "--- Installing ARIS upstream skills ---"
  for skill in "${ARIS_SKILLS[@]}"; do
    install_skill "$ARIS_REPO/skills/$skill"
  done
fi

# ── Install EPS upstream skills ──────────────────────────────────────────────
EPS_SKILLS=(
  engineering-writing engineering-polishing engineering-paper-auditor
  engineering-figure-table engineering-response engineering-validation
  engineering-paper-router engineering-paper-coach
)

if [[ -d "$EPS_REPO/skills" ]]; then
  echo ""
  echo "--- Installing EPS upstream skills ---"
  for skill in "${EPS_SKILLS[@]}"; do
    install_skill "$EPS_REPO/skills/$skill"
  done
fi

# ── Write manifest ────────────────────────────────────────────────────────────
if ! $DRY_RUN; then
  mkdir -p "$(dirname "$MANIFEST_FILE")"
  printf "%b" "$MANIFEST_NEW" > "$MANIFEST_FILE"
  echo ""
  echo "Manifest written to: $MANIFEST_FILE"
fi

echo ""
echo "=== Install complete (dry_run=$DRY_RUN) ==="
echo ""
echo "Validate with:"
echo "  python $REPO_ROOT/tools/validate_installation.py --dest $DEST"

#!/usr/bin/env bash
# install_skills.sh — Install ARIS Engineering Robotics skills
#
# Usage:
#   bash tools/install_skills.sh --platform codex
#   bash tools/install_skills.sh --platform codex --project /path/to/project
#   bash tools/install_skills.sh --platform claude
#   bash tools/install_skills.sh --platform claude --project /path/to/project
#   bash tools/install_skills.sh --platform antigravity --project /path/to/project
#   bash tools/install_skills.sh --platform antigravity   # user-wide (~/.gemini/config/skills/)
#   bash tools/install_skills.sh --platform codex --dry-run
#   bash tools/install_skills.sh --bootstrap            # fetch missing upstreams first
#   bash tools/install_skills.sh --list-platforms
#   bash tools/install_skills.sh --list-skills

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

# ── Argument parsing ─────────────────────────────────────────────────────────
PLATFORM=""
PROJECT_DIR=""
DRY_RUN=false
BOOTSTRAP=false

while [[ $# -gt 0 ]]; do
  case "$1" in
    --platform)    PLATFORM="$2"; shift 2 ;;
    --project)     PROJECT_DIR="$2"; shift 2 ;;
    --dry-run)     DRY_RUN=true; shift ;;
    --bootstrap)   BOOTSTRAP=true; shift ;;
    --list-platforms)
      echo "codex"
      echo "claude"
      echo "antigravity"
      exit 0
      ;;
    --list-skills)
      echo ""
      echo "=== ARIS Research Skills ==="
      echo "  research-lit, idea-discovery, idea-discovery-robot, novelty-check"
      echo "  experiment-plan, research-implement-feature, run-experiment"
      echo "  monitor-experiment, analyze-results, ablation-planner"
      echo "  paper-claim-audit, research-review, rebuttal, paper-compile"
      echo "  research-pipeline, dse-loop, claims-drafting, result-to-claim"
      echo "  citation-audit, formula-derivation, paper-write"
      echo ""
      echo "=== Robotics / Control Skills ==="
      echo "  robotics-research-router, robotics-experiment-plan"
      echo "  run-robotics-experiment, robotics-watchdog"
      echo "  robotics-result-analysis, controller-tuning"
      echo "  robotics-experiment-audit, simulation-validation"
      echo "  sil-hil-validation, robotics-result-to-claim"
      echo "  research-pipeline-robotics"
      echo ""
      echo "=== Engineering Paper Skills ==="
      echo "  engineering-writing, engineering-polishing, engineering-paper-auditor"
      echo "  engineering-figure-table, engineering-response, engineering-validation"
      echo "  engineering-paper-router, engineering-paper-coach"
      exit 0
      ;;
    *) echo "Unknown argument: $1"; exit 1 ;;
  esac
done

if [[ -z "$PLATFORM" ]]; then
  echo "ERROR: --platform is required."
  echo "Supported: codex, claude, antigravity"
  echo "Run with --list-platforms to see all options."
  exit 1
fi

# ── Bootstrap upstreams if requested ────────────────────────────────────────
if $BOOTSTRAP; then
  echo "--- Bootstrapping upstream dependencies ---"
  bash "$SCRIPT_DIR/bootstrap_upstreams.sh"
  echo ""
fi

# ── Resolve upstream paths (5-level priority) ─────────────────────────────
resolve_upstream() {
  local env_var="$1"
  local config_key="$2"
  local sibling_name="$3"
  local vendor_path="$4"

  # 1. Explicit environment variable
  if [[ -n "${!env_var:-}" && -d "${!env_var}" ]]; then
    echo "${!env_var}"
    return
  fi

  # 2. Repository config (YAML is simple key: path — read with grep/awk)
  local config_file="$REPO_ROOT/.aris-engineering-robotics/config.yaml"
  if [[ -f "$config_file" ]]; then
    local cfg_path
    cfg_path=$(grep "^  $config_key:" "$config_file" | awk '{print $2}' | tr -d '"')
    if [[ -n "$cfg_path" ]]; then
      # Resolve relative to repo root
      local abs_path
      abs_path="$(cd "$REPO_ROOT/$cfg_path" 2>/dev/null && pwd || echo "")"
      if [[ -n "$abs_path" && -d "$abs_path" ]]; then
        echo "$abs_path"
        return
      fi
    fi
  fi

  # 3. Existing sibling clone
  local sibling
  sibling="$(cd "$REPO_ROOT/../$sibling_name" 2>/dev/null && pwd || echo "")"
  if [[ -n "$sibling" && -d "$sibling/skills" ]]; then
    echo "$sibling"
    return
  fi

  # 4. Repository-local bootstrapped upstream
  if [[ -d "$vendor_path/skills" ]]; then
    echo "$vendor_path"
    return
  fi

  # 5. Not found
  echo ""
}

ARIS_REPO="$(resolve_upstream ARIS_REPO aris Auto-claude-code-research-in-sleep "$REPO_ROOT/vendor/upstreams/aris")"
EPS_REPO="$(resolve_upstream EPS_REPO engineering_paper_skills engineering-paper-skills "$REPO_ROOT/vendor/upstreams/engineering-paper-skills")"

# ── Resolve install destination ──────────────────────────────────────────────
resolve_antigravity_destination() {
  if [[ -n "$PROJECT_DIR" ]]; then
    echo "$PROJECT_DIR/.agents/skills"
  else
    echo "$HOME/.gemini/config/skills"
  fi
}

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
  antigravity)
    DEST="$(resolve_antigravity_destination)"
    ;;
  *)
    echo "ERROR: Unknown platform '$PLATFORM'."
    echo "Supported: codex, claude, antigravity"
    exit 1
    ;;
esac

echo "=== ARIS Engineering Robotics — Skill Installer ==="
echo "Platform  : $PLATFORM"
echo "Dry run   : $DRY_RUN"
echo "Destination: $DEST"
echo ""
echo "Upstream resolution:"
if [[ -n "$ARIS_REPO" ]]; then
  echo "  ARIS repo: $ARIS_REPO"
else
  echo "  ARIS repo: NOT FOUND (ARIS skills will be skipped)"
  echo "             Fix: export ARIS_REPO=/path/to/Auto-claude-code-research-in-sleep"
  echo "             Or:  bash tools/bootstrap_upstreams.sh"
fi
if [[ -n "$EPS_REPO" ]]; then
  echo "  EPS repo : $EPS_REPO"
else
  echo "  EPS repo : NOT FOUND (EPS skills will be skipped)"
  echo "             Fix: export EPS_REPO=/path/to/engineering-paper-skills"
  echo "             Or:  bash tools/bootstrap_upstreams.sh"
fi
echo ""

# ── Manifest (structured YAML) ────────────────────────────────────────────────
MANIFEST_DIR="$REPO_ROOT/.aris-engineering-robotics"
MANIFEST_FILE="$MANIFEST_DIR/installed-manifest.yaml"
MANIFEST_LEGACY="$MANIFEST_DIR/installed-skills.txt"

# ── Helper: copy a single skill ──────────────────────────────────────────────
INSTALLED_SKILLS=()

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
    echo "  DRY-RUN: would install $name → $dst"
  else
    mkdir -p "$DEST"
    if [[ -d "$dst" ]]; then
      rm -rf "$dst"
    fi
    cp -r "$src" "$dst"
    echo "  INSTALLED: $name"
    INSTALLED_SKILLS+=("$name")
  fi
}

# ── Helper: copy a shared dependency directory ────────────────────────────────
INSTALLED_SHARED=()

install_shared() {
  local src="$1"
  local name
  name="$(basename "$src")"
  local dst="$DEST/$name"

  if [[ ! -d "$src" ]]; then
    echo "  SKIP shared (not found): $name"
    return
  fi

  if $DRY_RUN; then
    echo "  DRY-RUN: would install shared/$name → $dst"
  else
    mkdir -p "$DEST"
    if [[ -d "$dst" ]]; then
      rm -rf "$dst"
    fi
    cp -r "$src" "$dst"
    echo "  INSTALLED shared: $name"
    INSTALLED_SHARED+=("$name")
  fi
}

# ── Install new robotics skills ───────────────────────────────────────────────
echo "--- Installing robotics/control skills ---"
for skill_dir in "$REPO_ROOT/skills"/*/; do
  install_skill "$skill_dir"
done

# ── Install ARIS upstream skills + shared dependencies ──────────────────────
ARIS_SKILLS=(
  research-lit idea-discovery idea-discovery-robot novelty-check
  experiment-plan research-implement-feature run-experiment
  monitor-experiment training-check analyze-results ablation-planner
  experiment-audit result-to-claim paper-writing paper-claim-audit
  research-review rebuttal paper-compile research-pipeline dse-loop
  claims-drafting paper-write citation-audit formula-derivation
)

if [[ -n "$ARIS_REPO" && -d "$ARIS_REPO/skills" ]]; then
  echo ""
  echo "--- Installing ARIS upstream skills ---"
  for skill in "${ARIS_SKILLS[@]}"; do
    install_skill "$ARIS_REPO/skills/$skill"
  done
  # Install ARIS shared-references dependency
  echo ""
  echo "--- Installing ARIS shared dependencies ---"
  install_shared "$ARIS_REPO/skills/shared-references"
fi

# ── Install EPS upstream skills + shared dependencies ────────────────────────
EPS_SKILLS=(
  engineering-writing engineering-polishing engineering-paper-auditor
  engineering-figure-table engineering-response engineering-validation
  engineering-paper-router engineering-paper-coach
)

if [[ -n "$EPS_REPO" && -d "$EPS_REPO/skills" ]]; then
  echo ""
  echo "--- Installing EPS upstream skills ---"
  for skill in "${EPS_SKILLS[@]}"; do
    install_skill "$EPS_REPO/skills/$skill"
  done
  # Install EPS _shared dependency
  echo ""
  echo "--- Installing EPS shared dependencies ---"
  install_shared "$EPS_REPO/skills/_shared"
fi

# ── Antigravity-specific: AGENTS.md + workflows ────────────────────────────────
INSTALLED_AGENTS_MD=false
INSTALLED_WORKFLOWS=()

if [[ "$PLATFORM" == "antigravity" && -n "$PROJECT_DIR" ]] && ! $DRY_RUN; then
  AGENTS_DIR="$PROJECT_DIR/.agents"
  AGENTS_MD="$AGENTS_DIR/AGENTS.md"
  AGENTS_TEMPLATE="$REPO_ROOT/templates/antigravity/AGENTS.md"
  MANAGED_BEGIN="<!-- BEGIN ARIS-ENGINEERING-ROBOTICS -->"
  MANAGED_END="<!-- END ARIS-ENGINEERING-ROBOTICS -->"

  mkdir -p "$AGENTS_DIR"

  if [[ ! -f "$AGENTS_MD" ]]; then
    cp "$AGENTS_TEMPLATE" "$AGENTS_MD"
    echo ""
    echo "INSTALLED: .agents/AGENTS.md"
    INSTALLED_AGENTS_MD=true
  else
    # Safe patch: replace managed block or append
    if grep -q "$MANAGED_BEGIN" "$AGENTS_MD"; then
      # Replace existing managed block
      python3 - <<'PYEOF' "$AGENTS_MD" "$AGENTS_TEMPLATE" "$MANAGED_BEGIN" "$MANAGED_END"
import sys
target = sys.argv[1]; tmpl = sys.argv[2]
begin = sys.argv[3]; end = sys.argv[4]

with open(target) as f: existing = f.read()
with open(tmpl) as f: managed = f.read()

# Extract just the managed block from template
start = managed.find(begin)
stop = managed.find(end) + len(end)
new_block = managed[start:stop]

# Replace block in target
idx_s = existing.find(begin)
idx_e = existing.find(end) + len(end)
updated = existing[:idx_s] + new_block + existing[idx_e:]

with open(target, 'w') as f: f.write(updated)
print("  UPDATED: .agents/AGENTS.md (managed block replaced)")
PYEOF
    else
      # Append managed block
      python3 - <<'PYEOF' "$AGENTS_MD" "$AGENTS_TEMPLATE" "$MANAGED_BEGIN" "$MANAGED_END"
import sys
target = sys.argv[1]; tmpl = sys.argv[2]
begin = sys.argv[3]; end = sys.argv[4]

with open(tmpl) as f: managed = f.read()
start = managed.find(begin)
stop = managed.find(end) + len(end)
new_block = "\n\n---\n\n" + managed[start:stop]

with open(target, 'a') as f: f.write(new_block)
print("  APPENDED: .agents/AGENTS.md (managed block added)")
PYEOF
    fi
    INSTALLED_AGENTS_MD=true
  fi

  # Install workflows
  WF_DEST="$AGENTS_DIR/workflows"
  mkdir -p "$WF_DEST"
  echo ""
  echo "--- Installing Antigravity workflows ---"
  for wf in "$REPO_ROOT/templates/antigravity/workflows/"*.md; do
    wf_name="$(basename "$wf")"
    cp "$wf" "$WF_DEST/$wf_name"
    echo "  INSTALLED workflow: $wf_name"
    INSTALLED_WORKFLOWS+=("$wf_name")
  done

elif [[ "$PLATFORM" == "antigravity" ]] && $DRY_RUN; then
  echo ""
  echo "DRY-RUN: would install .agents/AGENTS.md (safe patch)"
  echo "DRY-RUN: would install .agents/workflows/ (4 workflow files)"
fi

# ── Write structured manifest ─────────────────────────────────────────────────
if ! $DRY_RUN; then
  mkdir -p "$MANIFEST_DIR"

  # Write structured YAML manifest
  {
    echo "# ARIS Engineering Robotics — install manifest"
    echo "# Generated: $(date -Iseconds)"
    echo "platform: $PLATFORM"
    echo "destination: $DEST"
    if [[ -n "$PROJECT_DIR" ]]; then
      echo "project: $PROJECT_DIR"
    fi
    echo ""
    echo "managed:"
    echo "  skills:"
    for s in "${INSTALLED_SKILLS[@]}"; do
      echo "    - $s"
    done
    echo "  shared:"
    for s in "${INSTALLED_SHARED[@]}"; do
      echo "    - $s"
    done
    echo "  agents_md: $INSTALLED_AGENTS_MD"
    echo "  workflows:"
    for w in "${INSTALLED_WORKFLOWS[@]}"; do
      echo "    - $w"
    done
  } > "$MANIFEST_FILE"

  # Write legacy flat manifest for backward compatibility
  {
    for s in "${INSTALLED_SKILLS[@]}"; do
      echo "$DEST/$s"
    done
    for s in "${INSTALLED_SHARED[@]}"; do
      echo "$DEST/$s"
    done
  } > "$MANIFEST_LEGACY"

  echo ""
  echo "Manifest written to: $MANIFEST_FILE"
fi

echo ""
echo "=== Install complete (platform=$PLATFORM dry_run=$DRY_RUN) ==="
echo ""
echo "Validate with:"
echo "  python3 $REPO_ROOT/tools/validate_installation.py --platform $PLATFORM --dest $DEST"

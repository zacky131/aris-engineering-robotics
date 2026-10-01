#!/usr/bin/env bash
# sync_upstreams.sh — Pull latest changes from upstream repos and sync bundled skills.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

ARIS_REPO="${ARIS_REPO:-$(cd "$REPO_ROOT/../Auto-claude-code-research-in-sleep" 2>/dev/null && pwd || echo "")}"
EPS_REPO="${EPS_REPO:-$(cd "$REPO_ROOT/../engineering-paper-skills" 2>/dev/null && pwd || echo "")}"

# If not sibling, check vendor
if [[ -z "$ARIS_REPO" && -d "$REPO_ROOT/vendor/upstreams/Auto-claude-code-research-in-sleep" ]]; then
  ARIS_REPO="$REPO_ROOT/vendor/upstreams/Auto-claude-code-research-in-sleep"
fi
if [[ -z "$EPS_REPO" && -d "$REPO_ROOT/vendor/upstreams/engineering-paper-skills" ]]; then
  EPS_REPO="$REPO_ROOT/vendor/upstreams/engineering-paper-skills"
fi

echo "=== Syncing upstream repositories ==="

if [[ -n "$ARIS_REPO" && -d "$ARIS_REPO/.git" ]]; then
  echo "Pulling ARIS ($ARIS_REPO)..."
  git -C "$ARIS_REPO" pull --ff-only || echo "  Warning: could not pull ARIS (dirty or detached)"
fi

if [[ -n "$EPS_REPO" && -d "$EPS_REPO/.git" ]]; then
  echo "Pulling EPS ($EPS_REPO)..."
  git -C "$EPS_REPO" pull --ff-only || echo "  Warning: could not pull EPS (dirty or detached)"
fi

echo "Syncing updated skills into skills/ and shared/..."
# Sync ARIS skills
if [[ -n "$ARIS_REPO" && -d "$ARIS_REPO/skills" ]]; then
  for s in research-lit idea-discovery idea-discovery-robot novelty-check \
           experiment-plan research-implement-feature run-experiment \
           monitor-experiment training-check analyze-results ablation-planner \
           experiment-audit result-to-claim paper-writing paper-claim-audit \
           research-review rebuttal paper-compile research-pipeline dse-loop \
           claims-drafting paper-write citation-audit formula-derivation \
           research-refine arxiv alphaxiv deepxiv openalex semantic-scholar shared-references; do
    if [[ -d "$ARIS_REPO/skills/$s" ]]; then
      cp -r "$ARIS_REPO/skills/$s" "$REPO_ROOT/skills/"
    fi
  done
  if [[ -d "$ARIS_REPO/skills/shared-references" ]]; then
    cp -r "$ARIS_REPO/skills/shared-references" "$REPO_ROOT/shared/"
  fi
fi

# Sync EPS skills
if [[ -n "$EPS_REPO" && -d "$EPS_REPO/skills" ]]; then
  for s in engineering-writing engineering-polishing engineering-paper-auditor \
           engineering-figure-table engineering-response engineering-validation \
           engineering-paper-router engineering-paper-coach _shared; do
    if [[ -d "$EPS_REPO/skills/$s" ]]; then
      cp -r "$EPS_REPO/skills/$s" "$REPO_ROOT/skills/"
    fi
  done
  if [[ -d "$EPS_REPO/skills/_shared" ]]; then
    cp -r "$EPS_REPO/skills/_shared" "$REPO_ROOT/shared/"
  fi
fi

echo "Done. Bundled skills updated."

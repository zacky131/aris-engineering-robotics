# Migration and Update Guide

## Updating upstream repositories

```bash
bash tools/sync_upstreams.sh   # pulls upstream repos
bash tools/install_skills.sh --platform codex  # reinstall to pick up changes
```

## Updating aris-engineering-robotics

```bash
git -C /path/to/aris-engineering-robotics pull --ff-only
bash tools/install_skills.sh --platform codex
```

## Migrating from ARIS alone

If you were using `Auto-claude-code-research-in-sleep` alone for robotics research:

1. Keep all existing ARIS skills — they are still installed.
2. Add the new robotics layer skills on top.
3. Use `robotics-research-router` as the new entry point for experiment tasks.
4. Adopt `EVIDENCE_LEDGER.yaml` and `CLAIM_MAP.yaml` for claim governance.

## Migrating from engineering-paper-skills alone

If you were using `engineering-paper-skills` alone:

1. EPS skills remain installed and unchanged.
2. Add the robotics experiment layer to manage pre-paper evidence.
3. Run `robotics-result-to-claim` before `engineering-paper-auditor`.

## Known incompatibilities

- ARIS GPU/cloud skills (`vast-gpu`, `serverless-modal`, `feishu-notify`) are
  not installed by default. Add them manually if needed.
- If ARIS or EPS update their skill directory names, update `install_skills.sh`
  accordingly and re-run.

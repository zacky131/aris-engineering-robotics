# Installation Guide

## Prerequisites

- Both upstream repositories cloned as siblings:
  ```
  parent/
  ├── Auto-claude-code-research-in-sleep/
  ├── engineering-paper-skills/
  └── aris-engineering-robotics/
  ```
- Bash ≥ 4
- Python ≥ 3.9
- One of: Codex CLI, Claude Code

## Quick install

```bash
bash tools/install_skills.sh --platform codex
python tools/validate_installation.py
```

## Options

| Option | Description |
|---|---|
| `--platform codex` | Install to `~/.codex/skills/` |
| `--platform claude` | Install to `~/.claude/skills/` |
| `--project /path` | Install to project-local `.codex/skills/` |
| `--dry-run` | Preview without installing |

## Custom upstream paths

If your repos are not siblings, set environment variables:

```bash
export ARIS_REPO=/absolute/path/to/Auto-claude-code-research-in-sleep
export EPS_REPO=/absolute/path/to/engineering-paper-skills
bash tools/install_skills.sh --platform codex
```

Or edit `.aris-engineering-robotics/config.yaml`.

## Uninstall

```bash
bash tools/uninstall_skills.sh
```

Only removes skills tracked in the manifest. Unrelated user skills are preserved.

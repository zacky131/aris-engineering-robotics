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

## Project-Local Install (Recommended)

```bash
# For Google Antigravity
bash tools/install_skills.sh --platform antigravity --project /path/to/my_robotics_project

# For OpenAI Codex CLI
bash tools/install_skills.sh --platform codex --project /path/to/my_robotics_project

# For Claude Code
bash tools/install_skills.sh --platform claude --project /path/to/my_robotics_project
```

## User-Wide (Global) Install

```bash
# For Google Antigravity
bash tools/install_skills.sh --platform antigravity

# For OpenAI Codex CLI
bash tools/install_skills.sh --platform codex

# For Claude Code
bash tools/install_skills.sh --platform claude
```

Validate installation:
```bash
python3 tools/validate_installation.py
```

## Options

| Option | Description |
|---|---|
| `--platform antigravity` | Install for Google Antigravity (`.agents/skills/`, `.agents/AGENTS.md`, workflows) |
| `--platform codex` | Install for OpenAI Codex CLI |
| `--platform claude` | Install for Anthropic Claude Code |
| `--project /path` | Install to project-local directory (recommended) |
| `--dry-run` | Preview actions without copying files |

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

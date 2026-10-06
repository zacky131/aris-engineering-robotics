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

### Linux / macOS / WSL / Git Bash
```bash
# For Google Antigravity
bash tools/install_skills.sh --platform antigravity --project /path/to/my_robotics_project

# For OpenAI Codex CLI
bash tools/install_skills.sh --platform codex --project /path/to/my_robotics_project

# For Claude Code
bash tools/install_skills.sh --platform claude --project /path/to/my_robotics_project
```

### Windows (PowerShell)
```powershell
# For Google Antigravity
powershell -ExecutionPolicy Bypass -File tools\install_skills.ps1 -Platform antigravity -Project C:\path\to\my_robotics_project

# For OpenAI Codex CLI
powershell -ExecutionPolicy Bypass -File tools\install_skills.ps1 -Platform codex -Project C:\path\to\my_robotics_project

# For Claude Code
powershell -ExecutionPolicy Bypass -File tools\install_skills.ps1 -Platform claude -Project C:\path\to\my_robotics_project
```

### Windows / Cross-Platform (Python — CMD / Terminal / PowerShell)
```cmd
# For Google Antigravity
python tools\install_skills.py --platform antigravity --project C:\path\to\my_robotics_project

# For OpenAI Codex CLI
python tools\install_skills.py --platform codex --project C:\path\to\my_robotics_project

# For Claude Code
python tools\install_skills.py --platform claude --project C:\path\to\my_robotics_project
```

## User-Wide (Global) Install

**Linux / macOS:**
```bash
bash tools/install_skills.sh --platform antigravity
bash tools/install_skills.sh --platform codex
bash tools/install_skills.sh --platform claude
```

**Windows (PowerShell / Python):**
```powershell
# PowerShell
powershell -ExecutionPolicy Bypass -File tools\install_skills.ps1 -Platform antigravity
powershell -ExecutionPolicy Bypass -File tools\install_skills.ps1 -Platform codex
powershell -ExecutionPolicy Bypass -File tools\install_skills.ps1 -Platform claude

# Python
python tools\install_skills.py --platform antigravity
python tools\install_skills.py --platform codex
python tools\install_skills.py --platform claude
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

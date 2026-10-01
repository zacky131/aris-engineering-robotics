# Platform Compatibility

ARIS Engineering Robotics supports three AI coding agent platforms.

---

## Platform Summary

| Platform | Skill directory | Global path | Install command |
|---|---|---|---|
| Codex CLI | `.codex/skills/` | `~/.codex/skills/` | `--platform codex` |
| Claude Code | `.claude/skills/` | `~/.claude/skills/` | `--platform claude` |
| Google Antigravity | `.agents/skills/` | `~/.gemini/config/skills/` | `--platform antigravity` |

---

## Capability Matrix

| Capability | Codex | Claude Code | Antigravity | Notes |
|---|:---:|:---:|:---:|---|
| **Native robotics skills** | ✓ | ✓ | ✓ | Plain `SKILL.md` — platform-neutral |
| **Project-local skills** | ✓ `.codex/skills/` | ✓ `.claude/skills/` | ✓ `.agents/skills/` | All supported |
| **User-wide (global) skills** | ✓ `~/.codex/skills/` | ✓ `~/.claude/skills/` | ✓ `~/.gemini/config/skills/` | All supported |
| **ARIS research front skills** | ✓ | ✓ | ✓ | Requires ARIS repo or bootstrap |
| **EPS writing skills** | ✓ | ✓ | ✓ | Requires EPS repo or bootstrap |
| **EPS `_shared` dependencies** | ✓ | ✓ | ✓ | Installed automatically by installer |
| **ARIS shared-references** | ✓ | ✓ | ✓ | Installed automatically by installer |
| **AGENTS.md / project rules** | via AGENTS.md | via AGENTS.md | ✓ native | Antigravity reads `.agents/AGENTS.md` natively |
| **Workflow files** | via SKILL.md | via SKILL.md | ✓ `.agents/workflows/` | Antigravity supports workflow discovery |
| **ROS 2 experiment execution** | ✓† | ✓† | ✓† | †Requires ROS 2 installed on host |
| **PX4 SITL** | ✓† | ✓† | ✓† | †Requires PX4 environment on host |
| **Gazebo simulation** | ✓† | ✓† | ✓† | †Requires Gazebo installed |
| **Physical hardware actuation** | 🔒 GATED | 🔒 GATED | 🔒 GATED | Explicit human approval required |
| **GPU training (ML)** | ⚙ optional | ⚙ optional | ⚙ optional | Use ARIS `vast-gpu` / `serverless-modal` |
| **Codex cross-model review** | ✓ native | via MCP | via MCP | Optional; see ARIS MCP docs |
| **Gemini reviewer** | via MCP | via MCP | ✓ native | Optional; see ARIS gemini-review MCP |
| **Bootstrap upstream fetch** | ✓ | ✓ | ✓ | `bash tools/bootstrap_upstreams.sh` |
| **Structured manifest** | ✓ | ✓ | ✓ | `.aris-engineering-robotics/installed-manifest.yaml` |
| **Dry-run install** | ✓ | ✓ | ✓ | `--dry-run` flag |
| **Safe idempotent reinstall** | ✓ | ✓ | ✓ | Skills overwritten; AGENTS.md block patched |
| **Selective uninstall** | ✓ | ✓ | ✓ | `bash tools/uninstall_skills.sh` |

---

## Skill File Compatibility

All skills use:
- Plain Markdown (`SKILL.md`)
- YAML frontmatter with `name`, `description`, `platforms`
- No platform-specific syntax in skill bodies

The `platforms` frontmatter is informational only. All three platforms read
`SKILL.md` files identically.

---

## Shared Dependencies

Some upstream skills require co-located shared content:

| Dependency | Source | Required by |
|---|---|---|
| `_shared/` | `engineering-paper-skills/skills/_shared/` | All EPS writing skills |
| `shared-references/` | `Auto-claude-code-research-in-sleep/skills/shared-references/` | Some ARIS skills |

The installer copies these automatically alongside their dependent skills.

---

## Known Differences

| Feature | Codex | Claude Code | Antigravity |
|---|---|---|---|
| Cross-model reviewer integration | Native spawn-agent | MCP | MCP (gemini-review optional) |
| Plugin manifest format | `plugin.json` | Claude plugin schema | `.agents/` directory |
| Workflow discovery | SKILL.md references | SKILL.md references | `.agents/workflows/` native |
| Persistent project rules | AGENTS.md (manual) | AGENTS.md | AGENTS.md native |

---

## What Is NOT Implemented

| Feature | Status |
|---|---|
| Automatic physical robot arming | NOT IMPLEMENTED — human gated |
| GPU cloud provisioning | NOT IMPLEMENTED in robotics layer (use ARIS skills directly) |
| Codex MCP auto-configuration | NOT IMPLEMENTED — manual config required |
| Gemini MCP auto-configuration | NOT IMPLEMENTED — manual config required |
| Automatic `~/.gemini/settings.json` modification | NOT IMPLEMENTED — documented only |

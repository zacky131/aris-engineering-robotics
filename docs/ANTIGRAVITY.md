# ARIS Engineering Robotics for Google Antigravity

ARIS Engineering Robotics is natively compatible with **Google Antigravity**
(Antigravity IDE and Antigravity CLI).

Skills are plain Markdown files — no platform-specific syntax is required.

---

## Quick Installation

### Step 1 — Clone the repository

```bash
git clone https://github.com/zacky131/aris-engineering-robotics.git
cd aris-engineering-robotics
```

### Step 2 — Bootstrap upstream dependencies

```bash
bash tools/bootstrap_upstreams.sh
```

This checks whether the upstream ARIS and EPS repositories are available.
If not found as siblings, it clones them into `vendor/upstreams/` automatically.

### Step 3 — Install skills into your research project

```bash
bash tools/install_skills.sh \
    --platform antigravity \
    --project ~/my_robotics_project
```

This installs to:
```
~/my_robotics_project/.agents/skills/
~/my_robotics_project/.agents/workflows/
~/my_robotics_project/.agents/AGENTS.md
```

### Step 4 — Validate

```bash
python3 tools/validate_installation.py \
    --platform antigravity \
    --dest ~/my_robotics_project/.agents/skills \
    --project ~/my_robotics_project
```

---

## Skill Install Paths

| Mode | Destination |
|---|---|
| Project-local (recommended) | `<project>/.agents/skills/<skill-name>/SKILL.md` |
| User-wide (global) | `~/.gemini/config/skills/<skill-name>/SKILL.md` |

**Project-local is recommended** because it is version-controllable and
portable across machines.

### User-wide install

```bash
bash tools/install_skills.sh --platform antigravity
```

This installs to `~/.gemini/config/skills/`, which applies to all
Antigravity workspaces on this machine.

---

## Open Your Research Project in Antigravity

After installation, open your project:

```
Open ~/my_robotics_project in Antigravity IDE
```

or from the terminal:

```bash
cd ~/my_robotics_project
agy  # or open in Antigravity IDE
```

---

## Verify Skills Are Available

In the Antigravity chat:

```
What robotics research skills are available in this workspace?
```

Expected response: Antigravity lists skills from `.agents/skills/` including
`robotics-research-router`, `robotics-experiment-plan`, etc.

You can also inspect:

```bash
ls ~/my_robotics_project/.agents/skills/
```

---

## Natural-Language Usage (Recommended)

Antigravity discovers skills automatically from `.agents/skills/`.
You can invoke them with natural language:

### Example — Experiment design

```
I am developing an NMPC controller for a PX4 UAV landing on a moving UGV.
Design a rigorous experiment plan covering tracking performance, UWB delay,
measurement noise, computation time, and failure envelope.
```

Expected routing:
```
robotics-research-router → classical_control + px4_uav profiles
→ robotics-experiment-plan → Q1–Q6 experiment matrix
```

### Example — Result analysis

```
Analyze the completed experiment results and determine what claims are
supported by the current evidence.
```

Expected routing:
```
robotics-result-analysis → robotics-experiment-audit → robotics-result-to-claim
```

### Example — Paper writing

```
Revise the Results and Discussion sections based only on supported claims
from CLAIM_MAP.yaml.
```

Expected routing:
```
engineering-paper-auditor → engineering-writing
```

---

## Explicit Skill Usage

You can also call skills directly:

```
Use the robotics-experiment-plan skill to design the experiment matrix.
```

```
Use the sil-hil-validation skill to classify the evidence level.
```

```
Use the research-pipeline-robotics skill for the full research workflow.
```

---

## Workflow Usage

Installed workflows provide step-by-step guidance for common tasks.

| Workflow file | Purpose |
|---|---|
| `research-robotics.md` | Literature → novelty → experiment plan |
| `experiment-robotics.md` | Run → monitor → analyse → audit → claims |
| `analyze-robotics.md` | Result analysis and claim mapping |
| `write-engineering-paper.md` | Manuscript writing with claim governance |

Invoke:
```
Use the research-robotics workflow for my IMM-MPC UAV research.
```

---

## Example Research Workflows

### Example 1 — Classical Control / UAV (IMM-MPC)

```
Topic: Entropy-adaptive IMM-MPC for UAV interception
Profiles: classical_control + px4_uav
Evidence target: L3 (PX4 SITL)
```

```
Use the research-robotics workflow for:
"Entropy-adaptive IMM estimator combined with NMPC for UAV target interception.
Evaluate tracking accuracy, robustness to maneuver transitions, and real-time feasibility."
```

### Example 2 — ROS 2 + PX4 System

```
Topic: UAV landing on moving UGV under UWB delay and measurement noise
Profiles: ros2_robotics + px4_uav + classical_control
```

```
Use the experiment-robotics workflow for EXP001.yaml
(ROS 2 + PX4 SITL landing on simulated moving UGV with 50ms UWB delay)
```

### Example 3 — MARL Multi-UAV

```
Topic: Multi-UAV defense using MAPPO vs IPPO
Profiles: multi_robot + learning_robotics
```

For learning-based training, use ARIS `run-experiment` skill (handles GPU/training loop),
then use `robotics-result-analysis` for mission-level evaluation metrics.

---

## AGENTS.md — Persistent Instructions

The installer copies `templates/antigravity/AGENTS.md` to
`<project>/.agents/AGENTS.md`.

This file gives Antigravity persistent operating rules for the project:
- Research routing guidance
- Scientific integrity rules (never fabricate results)
- Physical robot safety constraints
- Evidence artifact locations

**Re-running the installer is safe**: it updates only the managed block
(between `<!-- BEGIN ARIS-ENGINEERING-ROBOTICS -->` and
`<!-- END ARIS-ENGINEERING-ROBOTICS -->`) and preserves any user content.

---

## Cross-Model Review (Advanced / Optional)

ARIS supports cross-model review where the executor and reviewer use
different model families. This is optional — the basic robotics skills
work without it.

ARIS upstream includes a Gemini-based reviewer MCP server at:
```
Auto-claude-code-research-in-sleep/mcp-servers/gemini-review/
```

When running on Antigravity, review tasks may use:
- The Gemini reviewer MCP (if configured)
- Or ARIS `auto-review-loop-llm` skill as a fallback

See upstream ARIS documentation for MCP configuration.
Do not configure `~/.gemini/settings.json` automatically — use placeholders.

---

## Capability Status

| Capability | Status |
|---|---|
| Antigravity skill discovery | **SUPPORTED** |
| Project-local skills | **SUPPORTED** (`.agents/skills/`) |
| Global user-wide skills | **SUPPORTED** (`~/.gemini/config/skills/`) |
| AGENTS.md persistent rules | **SUPPORTED** |
| Antigravity workflows | **SUPPORTED** |
| ARIS research front skills | **SUPPORTED** (if ARIS repo available) |
| EPS writing skills | **SUPPORTED** (if EPS repo available) |
| EPS `_shared` dependencies | **SUPPORTED** (installed automatically) |
| ROS 2 experiment execution | **SUPPORTED IF ROS 2 installed on host** |
| PX4 SITL | **SUPPORTED IF PX4 environment exists** |
| Codex cross-model review | **OPTIONAL** (requires Codex MCP) |
| Physical UAV actuation | **HUMAN GATED** (explicit approval required) |
| GPU training | **OPTIONAL** (use ARIS `vast-gpu` / `serverless-modal`) |

---

## Troubleshooting

### Upstream repos not found

```
ARIS repo: NOT FOUND
```

Run:
```bash
bash tools/bootstrap_upstreams.sh
```

Or manually set:
```bash
export ARIS_REPO=/path/to/Auto-claude-code-research-in-sleep
export EPS_REPO=/path/to/engineering-paper-skills
bash tools/install_skills.sh --platform antigravity --project /path/to/project
```

### Skills not loading in Antigravity

Verify the install path:
```bash
ls ~/my_project/.agents/skills/
```

Each skill directory must contain `SKILL.md`.

### AGENTS.md already exists in project

The installer safely patches the managed block without overwriting user content.
See the managed markers in `templates/antigravity/AGENTS.md`.

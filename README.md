# ARIS Engineering Robotics

> **Research orchestration × robotics/control engineering × engineering paper skills — unified.**

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

---

## What is this?

**ARIS Engineering Robotics** is an integration repository that combines the strongest capabilities of two sibling repositories:

| Source | Focus |
|---|---|
| [`Auto-claude-code-research-in-sleep`](../Auto-claude-code-research-in-sleep) (ARIS) | Research orchestration, literature, idea discovery, experiment planning, result-to-claim |
| [`engineering-paper-skills`](../engineering-paper-skills) (EPS) | Engineering-paper writing, auditing, evidence governance, reviewer response, submission validation |

It adds a new **Robotics / Control Research Layer** between them that neither upstream repository provides:

- ROS 2 / Gazebo / PX4 experiment lifecycle management
- Controller tuning and design-space exploration
- SIL / HIL evidence classification (L0–L6)
- Robotics-domain result analysis and metric catalogues
- Simulation integrity auditing
- Evidence ledger and claim-map governance artifacts

---

## Architecture

```
ARIS Research Layer
  research-lit · idea-discovery · novelty-check · experiment-plan
  research-implement-feature · paper-claim-audit · research-review · rebuttal
        │
        ▼
Robotics / Control Layer  (NEW — this repository)
  robotics-research-router · robotics-experiment-plan
  run-robotics-experiment · robotics-watchdog
  robotics-result-analysis · controller-tuning
  robotics-experiment-audit · simulation-validation · sil-hil-validation
  robotics-result-to-claim · research-pipeline-robotics
        │
        ▼
Engineering Paper Layer
  engineering-writing · engineering-polishing · engineering-paper-auditor
  engineering-figure-table · engineering-response · engineering-validation
```

See [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md) for Mermaid diagrams.

---

## Supported Research Domains

- Classical control: PID, LQR, MPC, NMPC, SMC, adaptive control
- State estimation: Kalman filter, EKF, UKF, IMM
- ROS 2 robotics: Nav2, SLAM, sensor fusion
- PX4 / UAV: SITL, offboard, MAVLink, uXRCE-DDS
- Multi-robot / MARL: MAPPO, IPPO, cooperative control
- Hybrid AI-control: learned + classical architectures
- Trajectory planning, guidance, coverage

---

## Installation

### Prerequisites

- Both sibling repositories cloned at peer level:
  ```
  parent/
  ├── Auto-claude-code-research-in-sleep/
  ├── engineering-paper-skills/
  └── aris-engineering-robotics/   ← this repo
  ```
- Bash ≥ 4
- Python ≥ 3.9 (for validation scripts)
- Codex CLI or Claude Code configured

### Install skills (Codex, user-wide)

```bash
bash tools/install_skills.sh --platform codex
```

### Install skills (Codex, project-local)

```bash
bash tools/install_skills.sh --platform codex --project /path/to/your/project
```

### Install skills (Claude)

```bash
bash tools/install_skills.sh --platform claude
```

### Validate installation

```bash
python tools/validate_installation.py
```

### Dry run (no changes made)

```bash
bash tools/install_skills.sh --platform codex --dry-run
```

---

## Quick Start

See [`docs/QUICKSTART.md`](docs/QUICKSTART.md) for full walkthroughs.

### MPC UAV interception experiment (Example A)

```
1. Open Codex or Claude in your project directory.
2. Call: robotics-research-router
   → profile detected: classical_control + px4_uav
3. Call: robotics-experiment-plan
   → experiment matrix generated
4. Fill in: templates/EXPERIMENT.yaml
5. Call: run-robotics-experiment
6. Call: robotics-watchdog  (monitor)
7. Call: robotics-result-analysis
8. Call: robotics-experiment-audit
9. Call: robotics-result-to-claim  → CLAIM_MAP.yaml updated
10. Call: engineering-paper-auditor
11. Call: engineering-writing
```

---

## Usage Instructions

### How to Use This System

This integration exposes its capabilities as **skills** — plain-Markdown instruction files
loaded by your AI coding agent (Codex CLI or Claude Code).

#### Step 1 — Install skills

Run the installer once:

```bash
bash tools/install_skills.sh --platform codex
```

This places skill files into `~/.codex/skills/` (user-wide) or `.codex/skills/` (project-local).

#### Step 2 — Open your AI agent in your research project

Navigate to your robotics research project in VS Code / terminal, then open Codex or Claude.

#### Step 3 — Call skills by name

In the agent chat, reference a skill by its directory name:

```
Use the robotics-research-router skill to classify my research context.
```

```
Use the robotics-experiment-plan skill to design an MPC robustness experiment.
```

```
Use the robotics-result-to-claim skill to convert my simulation results to claims.
```

```
Use the engineering-writing skill to draft the Results section.
```

#### Step 4 — Use the evidence artifacts

Your research project should maintain:

- `EXPERIMENT.yaml` — per-experiment configuration
- `EVIDENCE_LEDGER.yaml` — all verified result records
- `CLAIM_MAP.yaml` — link claims to evidence
- `RESULT_SUMMARY.yaml` — summary of each experiment run

Copy templates from [`templates/`](templates/) to get started.

#### Step 5 — Validate before writing

Always run the experiment audit and result-to-claim skills before drafting manuscript sections.
This prevents inflated claims.

---

## Evidence and Claim Governance

The integration enforces a strict evidence model.

Evidence levels:

| Level | Type |
|---|---|
| L0 | Theoretical / analytical |
| L1 | Numerical simulation |
| L2 | Physics simulation (Gazebo, etc.) |
| L3 | Software-in-the-loop (SIL) |
| L4 | Hardware-in-the-loop (HIL) |
| L5 | Controlled physical experiment |
| L6 | Operational / field environment |

Claims may not exceed the level of evidence produced.

See [`docs/EVIDENCE_MODEL.md`](docs/EVIDENCE_MODEL.md) for details.

---

## Limitations

- Physical robot actuation always requires explicit human approval. The framework prepares commands but does not autonomously arm or move real robots.
- GPU-accelerated training is not the default experiment backend. Use ARIS `vast-gpu` or `serverless-modal` directly if needed.
- The installer assumes upstream repos are peer siblings unless the config file is edited.
- SIL/HIL automation requires a working local ROS 2 / Gazebo / PX4 installation.
- Real-time factor tracking requires the experiment runner to capture timing data.

---

## Attribution

- **ARIS / Auto-claude-code-research-in-sleep** — © 2026 wanshuiyin. MIT License.
- **engineering-paper-skills** — © 2026 Engineering Paper Skills contributors. MIT License. Includes adapted material from phd-writing (© 2026 Yuqi Cheng, MIT).

See [`NOTICE.md`](NOTICE.md) for full third-party notices.

---

## License

MIT — see [`LICENSE`](LICENSE).

---
name: robotics-research-router
description: >
  Detect the robotics/control research profile for the current project and
  route to the appropriate experiment, analysis, and paper-writing skills.
  Entry point for all robotics research tasks.
platforms:
  - codex
  - claude
  - antigravity
---

# Skill: robotics-research-router

## Purpose

Classify the user's research context into one or more profiles and recommend
the correct downstream skills. This skill is the entry point for all robotics
and control research tasks.

## Supported Profiles

| Profile | Key indicators |
|---|---|
| `classical_control` | PID, LQR, MPC, NMPC, SMC, adaptive, robust, observer, EKF, UKF, IMM |
| `ros2_robotics` | ROS 2, Gazebo, Nav2, SLAM, rosbag, TF, sensor fusion |
| `px4_uav` | PX4, SITL, MAVLink, uXRCE-DDS, offboard control, UAV, guidance |
| `multi_robot` | MARL, swarm, coordination, task allocation, multi-UAV |
| `learning_robotics` | PPO, SAC, TD3, MAPPO, IPPO, imitation, learned policy |
| `hybrid_ai_control` | learned + classical mixed architecture |

Multiple profiles may be active simultaneously (e.g., `px4_uav + classical_control`).

## Instructions

### Step 1 — Inspect research context

Read the following if present:
- `anchor_papers/` — check whether this directory exists and contains PDFs (either at root or in `foundational/`, `closest_work/`, `methodology/`, `benchmark/`, `uncategorized/`).
  Check if `research/ANCHOR_MANIFEST.yaml` exists and whether all anchor PDFs are already processed and unchanged.
- `RESEARCH_CONTRACT.md` or equivalent problem statement
- Any `EXPERIMENT.yaml` or experiment configuration files
- Any existing code (`*.py`, `*.cpp`, `*.launch.py`, `*.yaml`)
- Paper draft if available

### Step 2 — Extract keywords and architecture

Look for:
- Controller type (PID, MPC, RL policy, etc.)
- Middleware (ROS 2, MATLAB, Simulink, Python, etc.)
- Simulator (Gazebo, Isaac, PyBullet, MATLAB, etc.)
- Autopilot (PX4, ArduPilot, etc.)
- Robot type (UAV, UGV, manipulator, mobile, multi-robot)
- Learning method if any

### Step 3 — Classify profile(s)

Assign one or more profiles from the table above.

State your confidence:
- HIGH: clear indicator keywords present
- MEDIUM: contextual evidence but no explicit keyword
- LOW: assumption based on research direction

### Step 4 — Recommend skills

**Anchor Paper Check (Stage 0):**
- If `anchor_papers/` contains PDFs and either outputs (`research/ANCHOR_PAPER_SYNTHESIS.md`, etc.) are missing or PDFs have changed:
  Route first to `anchor-paper-intake`. Broad literature search, novelty checking, and experiment design must NOT proceed until anchor intake is complete.
- If anchor outputs already exist and PDFs are unchanged, anchor intake is complete; proceed to next recommended skills.
- If no anchor papers exist, proceed directly with standard research flow.

**Downstream Skills:**
Based on profile and context, recommend the next skills in order:

1. `anchor-paper-intake` (if anchor papers present and unindexed)
2. `robotics-experiment-plan` — design the experiment
3. `run-robotics-experiment` — execute it
4. `robotics-watchdog` — monitor health
5. `robotics-result-analysis` — analyse results
6. `robotics-experiment-audit` — audit integrity
7. `robotics-result-to-claim` — generate claims
8. `engineering-paper-auditor` — audit manuscript
9. `engineering-writing` — draft/revise

For paper-only tasks:
- Route directly to `engineering-paper-router`

For literature/novelty tasks:
- Route to ARIS `research-lit`, `idea-discovery`, `novelty-check` (consuming `LITERATURE_SEARCH_PLAN.md` if anchor papers were processed)

### Step 5 — Report

Output:

```yaml
anchor_papers:
  detected: true          # or false
  count: 3                # number of anchor PDFs found
  processed: false        # true if ANCHOR_MANIFEST.yaml is up-to-date
  required_next_skill: anchor-paper-intake   # omitted or null if already processed

detected_profiles:
  - classical_control     # HIGH
  - px4_uav               # HIGH

recommended_skills_in_order:
  1. anchor-paper-intake   # if unindexed anchor papers exist
  2. robotics-experiment-plan
  3. run-robotics-experiment
  4. robotics-watchdog
  5. robotics-result-analysis
  6. robotics-experiment-audit
  7. robotics-result-to-claim
  8. engineering-paper-auditor
  9. engineering-writing

profile_notes: >
  MPC controller targeting UAV interception. PX4 SITL + Gazebo stack
  detected. Recommend px4_uav profile for metric set and watchdog checks.

active_shared_rules:
  - shared/evidence-boundary.md
  - shared/claim-strength.md
  - shared/control-metrics.md
  - shared/timing-and-realtime.md
```

## Constraints

- Do not assume a profile without evidence.
- A project may have multiple active profiles; list all of them.
- Do not route paper tasks to robotics experiment skills.
- If `anchor_papers/` contains PDFs that are unindexed or modified, `anchor-paper-intake` must precede broad search or experiment planning.
- If no profile can be detected, ask the user one clarifying question.

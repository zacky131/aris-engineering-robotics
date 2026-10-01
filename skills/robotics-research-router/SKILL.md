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

Based on profile, recommend the next skills in order:

1. `robotics-experiment-plan` — design the experiment
2. `run-robotics-experiment` — execute it
3. `robotics-watchdog` — monitor health
4. `robotics-result-analysis` — analyse results
5. `robotics-experiment-audit` — audit integrity
6. `robotics-result-to-claim` — generate claims
7. `engineering-paper-auditor` — audit manuscript
8. `engineering-writing` — draft/revise

For paper-only tasks:
- Route directly to `engineering-paper-router`

For literature/novelty tasks:
- Route to ARIS `research-lit`, `idea-discovery`, `novelty-check`

### Step 5 — Report

Output:

```yaml
detected_profiles:
  - classical_control     # HIGH
  - px4_uav               # HIGH

recommended_skills_in_order:
  1. robotics-experiment-plan
  2. run-robotics-experiment
  3. robotics-watchdog
  4. robotics-result-analysis
  5. robotics-experiment-audit
  6. robotics-result-to-claim
  7. engineering-paper-auditor
  8. engineering-writing

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
- If no profile can be detected, ask the user one clarifying question.

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
| `learning_control` | DRL, PPO, SAC, TD3, REDQ, offline RL, sim-to-real, domain randomization, RMA |
| `ai_control` | Neural ODE, PINN, physics-informed, learned dynamics, Neural MPC, GP-MPC, residual RL, residual control |
| `safe_sota_control` | Control Barrier Functions, CBF, CLF-CBF, safety filter, QP shield, forward invariance, safety certificate |
| `vla_robotics` | VLA, Vision-Language-Action, OpenVLA, Octo, RT-1, RT-2, pi0, SmolVLA, ACT, action chunking, LIBERO, SIMPLER, ManiSkill, CALVIN |
| `ros2_robotics` | ROS 2, Gazebo, Nav2, SLAM, rosbag, TF, sensor fusion |
| `px4_uav` | PX4, SITL, MAVLink, uXRCE-DDS, offboard control, UAV, guidance |
| `multi_robot` | MARL, swarm, coordination, task allocation, multi-UAV |
| `learning_robotics` | General learning-based robotics (alias/superset of learning_control) |
| `hybrid_ai_control` | Mixed learned + classical architecture (alias/superset of ai_control) |

Multiple profiles may be active simultaneously (e.g., `vla_robotics + safe_sota_control` or `px4_uav + classical_control`).

## Instructions

### Step 1 — Inspect research context

Read the following if present:
- `anchor_papers/` — check whether this directory exists and contains PDFs (either at root or in `foundational/`, `closest_work/`, `methodology/`, `benchmark/`, `uncategorized/`).
  Check if `research/ANCHOR_MANIFEST.yaml` exists and whether all anchor PDFs are already processed and unchanged.
- `RESEARCH_CONTRACT.md` or equivalent problem statement
- Any `EXPERIMENT.yaml`, `VLA_EVALUATION.yaml`, or `LEARNING_EXPERIMENT.yaml` configuration files
- Any existing code (`*.py`, `*.cpp`, `*.launch.py`, `*.yaml`)
- Paper draft if available

### Step 2 — Extract keywords and architecture

Look for:
- VLA / Embodied AI (OpenVLA, Octo, RT-1/2, pi0, SmolVLA, ACT, Diffusion Policy, LIBERO, SIMPLER, ManiSkill)
- Learning algorithm (PPO, SAC, TD3, Dreamer, DAgger, RMA, domain randomization)
- AI / Physics-Informed model (Neural ODE, PINN, Neural MPC, GP-MPC, residual network)
- Safety certification (CBF, Control Barrier Function, safety filter, QP shield)
- Classical controller (PID, MPC, LQR, SMC, etc.)
- Middleware (ROS 2, MATLAB, Simulink, Python, etc.)
- Simulator (SIMPLER, LIBERO, ManiSkill, Isaac Lab/Orbit, Gazebo, MuJoCo, PyBullet)
- Autopilot (PX4, ArduPilot, etc.)
- Robot type (manipulator, UAV, UGV, humanoid, mobile, multi-robot)

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
Based on profile and context, recommend specialized skills:

1. `anchor-paper-intake` (if unindexed anchor papers exist)
2. **Experiment Planning**:
   - For all profiles: `robotics-experiment-plan`
3. **Execution & Specialized Evaluation**:
   - For VLA / Embodied AI: `vla-robotics` → `safety-filter-cbf` → `run-robotics-experiment`
   - For Learning-Based Control: `run-robotics-experiment` → `learning-control-eval` → `safety-filter-cbf`
   - For AI / Residual / Classical Control: `run-robotics-experiment` → `controller-tuning` → `simulation-validation`
4. **Monitoring**: `robotics-watchdog` (monitors RTF, VLA inference latency, QP feasibility, state divergence)
5. **Analysis**: `robotics-result-analysis` (computes RMSE, success rate, IQM, jerk, latency)
6. **Audit & Integrity**: `robotics-experiment-audit` (verifies seeds, OOD splits, baseline fairness)
7. **Claims & Writing**: `robotics-result-to-claim` → `engineering-paper-auditor` → `engineering-writing`

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
  - vla_robotics          # HIGH
  - safe_sota_control     # HIGH

recommended_skills_in_order:
  1. anchor-paper-intake  # if unindexed anchor papers exist
  2. robotics-experiment-plan
  3. vla-robotics
  4. safety-filter-cbf
  5. run-robotics-experiment
  6. robotics-watchdog
  7. robotics-result-analysis
  8. robotics-experiment-audit
  9. robotics-result-to-claim
  10. engineering-paper-auditor
  11. engineering-writing

profile_notes: >
  Vision-Language-Action manipulation task targeting LIBERO benchmark with
  real-time CBF safety shield. Recommended vla_robotics + safe_sota_control.

active_shared_rules:
  - shared/vla-standards.md
  - shared/safety-cbf-standards.md
  - shared/learning-control-standards.md
  - shared/ai-control-realtime.md
  - shared/evidence-boundary.md
  - shared/claim-strength.md
```

## Constraints

- Do not assume a profile without evidence.
- A project may have multiple active profiles; list all of them.
- Do not route paper tasks to robotics experiment skills.
- If `anchor_papers/` contains PDFs that are unindexed or modified, `anchor-paper-intake` must precede broad search or experiment planning.
- If no profile can be detected, ask the user one clarifying question.

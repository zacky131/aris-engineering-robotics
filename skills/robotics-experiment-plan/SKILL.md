---
name: robotics-experiment-plan
description: >
  Design a rigorous robotics/control experiment plan answering Q1–Q6.
  Generates a run matrix, maps each experiment to claims, and classifies
  experiments as MUST_RUN / SHOULD_RUN / NICE_TO_HAVE.
platforms:
  - codex
  - claude
  - antigravity
---

# Skill: robotics-experiment-plan

## Purpose

Design a rigorous experiment plan for robotics and control research.
Every plan must address the core research questions and map experiments to claims.

## Core Research Questions

Not all six questions apply to every project. Explicitly classify which apply:

| ID | Question | Classical / UAV focus | Learning / AI Control focus | VLA / Embodied AI focus |
|---|---|---|---|---|
| Q1 | PERFORMANCE | Tracking error, rise time, overshoot | Sample efficiency, reward, IQM | Task success rate, subtask completion |
| Q2 | MECHANISM | Operating condition concentration | State visitation, value convergence | Visual / language / spatial OOD generalization |
| Q3 | COMPONENT | Observer, cost terms, constraint tuning | Loss terms, domain randomization, teacher-student | Vision backbone, chunk horizon $H$, safety shield |
| Q4 | ROBUSTNESS | Wind, measurement noise, delay | Parametric mismatch, sim-to-real gap | Visual distractors, lighting, camera shift |
| Q5 | COMPUTATION | Solver time (acados/CasADi), RTF | Neural inference latency, memory | VLA tokenization, model FPS, QP solve time |
| Q6 | FAILURE ENVELOPE | Stability boundary, actuator saturation | Distribution shift, reward exploitation | Workspace violation, collision rate, hallucination |

## Instructions

### Step 1 — Read research context

Load if present:
- `research/ANCHOR_PAPER_SYNTHESIS.md` — synthesized methods, baselines, and evaluation protocols
- `research/RESEARCH_GAP_MAP.md` — verified gap states and closest prior works
- `RESEARCH_CONTRACT.md`
- `CLAIM_MAP.yaml` (initial claims if drafted)
- `profiles/*.yaml` for the active profile
- Any existing experiment scripts or configs

### Step 2 — Anchor & literature alignment check

If anchor paper outputs or literature records are present, report explicitly:
- **Baseline provenance**: which baseline choices came from anchor papers vs current literature
- **Community metrics**: which metrics appear to be standard across the anchor papers and field
- **Gap alignment**: which experiment scenarios test the verified gaps in `RESEARCH_GAP_MAP.md`
- **Novelty distinction**: which specific experiments directly compare and distinguish the proposed method from the closest anchor paper(s)
- **Scientific rigor invariant**: Do NOT blindly copy weak protocols or flawed assumptions from anchor papers (e.g., inadequate repetitions, absence of disturbances, or uncalibrated sensors). Upgrade to standard scientific evaluation rigor.

### Step 3 — List candidate experiments

For each research question that applies:
- Define one or more candidate experiments
- State what it tests (method, baseline, condition)
- State what metric it produces
- State which claim(s) it supports

### Step 4 — Classify each experiment

Assign priority:
- `MUST_RUN` — paper cannot be submitted without this
- `SHOULD_RUN` — significantly strengthens claims
- `NICE_TO_HAVE` — additional evidence; run if time/resources allow

### Step 5 — Assess feasibility

For each MUST_RUN experiment:
- Is the simulator available?
- Is the baseline implementable?
- Is the hardware required?
- What is the estimated compute budget?
- Is manual hardware interaction required? (if so, flag as HARDWARE_GATE)

### Step 6 — Generate run matrix

| ExpID | Name | Question | Platform | Baseline | Repetitions | MUST/SHOULD/NICE | Claim | Output metric |
|---|---|---|---|---|---|---|---|---|

### Step 7 — Identify missing capabilities

List any:
- missing implementation components
- missing baselines
- missing simulator configurations
- hardware dependencies not yet met

### Step 8 — Output

Produce:
1. The run matrix table above
2. A filled `EXPERIMENT.yaml` draft for each MUST_RUN experiment (using template)
3. Anchor and literature provenance summary (baselines, community metrics, gap alignment)
4. A risk and dependency log
3. A risk and dependency log

## Example partial plan

```
Q1 PERFORMANCE
  EXP001: MPC vs PID tracking on constant-velocity target — MUST_RUN → C001
  EXP002: MPC vs PID tracking on maneuver-transition target — MUST_RUN → C001

Q4 ROBUSTNESS
  EXP003: MPC with wind disturbance (0.5 m/s, 1 m/s, 2 m/s) — MUST_RUN → C002
  EXP004: MPC with measurement noise scaling — SHOULD_RUN → C002

Q5 COMPUTATION
  EXP005: MPC solver time across horizon lengths — MUST_RUN → C003

Q6 FAILURE ENVELOPE
  EXP006: MPC with 2× model mismatch — NICE_TO_HAVE → C002
```

## Constraints

- Never fabricate a baseline that has not been confirmed implementable.
- Mark HARDWARE_GATE on any experiment requiring physical actuation.
- Do not assume GPU availability for non-learning experiments.
- Do not plan more than a researcher can realistically run given the time budget.
- If no time budget is specified, ask before generating a NICE_TO_HAVE list.

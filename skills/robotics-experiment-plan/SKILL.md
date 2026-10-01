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

Not all six questions apply to every project. Explicitly classify which apply.

| ID | Question | Domain focus |
|---|---|---|
| Q1 | PERFORMANCE — Does the method improve the primary task metric? | All |
| Q2 | MECHANISM — Under which condition is the improvement concentrated? | All |
| Q3 | COMPONENT — Which component supports which contribution? | All |
| Q4 | ROBUSTNESS — How does performance change under disturbances/uncertainty? | Control, estimation |
| Q5 | COMPUTATION — Can the approach satisfy real-time constraints? | Control, embedded |
| Q6 | FAILURE ENVELOPE — Where does the method cease to work reliably? | Safety-critical |

## Instructions

### Step 1 — Read research context

Load if present:
- `RESEARCH_CONTRACT.md`
- `CLAIM_MAP.yaml` (initial claims if drafted)
- `profiles/*.yaml` for the active profile
- Any existing experiment scripts or configs

### Step 2 — List candidate experiments

For each research question that applies:
- Define one or more candidate experiments
- State what it tests (method, baseline, condition)
- State what metric it produces
- State which claim(s) it supports

### Step 3 — Classify each experiment

Assign priority:
- `MUST_RUN` — paper cannot be submitted without this
- `SHOULD_RUN` — significantly strengthens claims
- `NICE_TO_HAVE` — additional evidence; run if time/resources allow

### Step 4 — Assess feasibility

For each MUST_RUN experiment:
- Is the simulator available?
- Is the baseline implementable?
- Is the hardware required?
- What is the estimated compute budget?
- Is manual hardware interaction required? (if so, flag as HARDWARE_GATE)

### Step 5 — Generate run matrix

| ExpID | Name | Question | Platform | Baseline | Repetitions | MUST/SHOULD/NICE | Claim | Output metric |
|---|---|---|---|---|---|---|---|---|

### Step 6 — Identify missing capabilities

List any:
- missing implementation components
- missing baselines
- missing simulator configurations
- hardware dependencies not yet met

### Step 7 — Output

Produce:
1. The run matrix table above
2. A filled `EXPERIMENT.yaml` draft for each MUST_RUN experiment (using template)
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

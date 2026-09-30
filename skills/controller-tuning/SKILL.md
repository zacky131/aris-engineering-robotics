---
name: controller-tuning
description: >
  Controller parameter design-space exploration (DSE) for robotics/control research.
  Supports MPC, PID, SMC, IMM, and trajectory planners. Adapted from ARIS dse-loop
  for control domains. Outputs a tuning record and Pareto analysis.
platforms:
  - codex
  - claude
---

# Skill: controller-tuning

## Purpose

Systematically explore controller parameter space to find configurations that
minimise a declared objective subject to hard constraints.

This is adapted from the ARIS `dse-loop` pattern.

## Supported Controllers

| Controller | Key parameters |
|---|---|
| MPC / NMPC | Q (state weight), R (control weight), prediction horizon N, control horizon Nc, constraints, solver tolerance |
| PID | Kp, Ki, Kd, anti-windup limit |
| SMC | switching gain, boundary layer thickness |
| LQR | Q, R matrices |
| IMM estimator | transition probability matrix, model noise Q_i, measurement noise R |
| Trajectory planner | speed, lookahead distance, penalty weights |

## Supported Search Strategies

| Strategy | When to use |
|---|---|
| `grid_search` | Small parameter space (≤ 3 dimensions); exhaustive coverage |
| `structured_sweep` | One parameter at a time while fixing others |
| `coordinate_search` | Iterative 1-D searches along each axis |
| `random_search` | High-dimensional space; broad exploration |
| `local_refinement` | After coarse search; fine-tune best candidates |
| `pareto_analysis` | Multi-objective; identify trade-off frontier |

## Instructions

### Step 1 — Read tuning specification

Load from user or `EXPERIMENT.yaml`:

```yaml
tuning:
  controller: mpc
  strategy: structured_sweep

  objectives:
    primary: position_rmse   # minimise
    secondary: control_effort  # minimise
    tertiary: computation_time_p99  # minimise

  hard_constraints:
    constraint_violations: 0
    computation_time_p99_ms: {max: 20}  # control period

  parameters:
    Q_position: [1, 5, 10, 50]
    Q_velocity: [0.1, 1, 5]
    R_input: [0.01, 0.1, 1]
    horizon_N: [10, 20, 30]
```

### Step 2 — Generate parameter sweep plan

List all parameter combinations to evaluate.
For grid_search: enumerate the full Cartesian product.
For structured_sweep: list one-at-a-time scans.
State the total number of configurations.

### Step 3 — Execute sweep

For each configuration:
1. Modify controller parameters in the experiment config or code
2. Run experiment (or instruct user to run `run-robotics-experiment`)
3. Record result metrics

**HARDWARE_GATE**: If `platform.type == real`, stop and request manual execution for each configuration.

### Step 4 — Filter by hard constraints

Discard configurations that violate any hard constraint.

### Step 5 — Rank by objectives

Rank surviving configurations by primary objective, then secondary, etc.

### Step 6 — Pareto analysis (if multi-objective)

Identify the Pareto frontier across two or more objectives.
Report Pareto-optimal configurations.

### Step 7 — Output

```yaml
tuning_record:
  controller: mpc
  strategy: structured_sweep
  total_configs_evaluated: 48
  configs_passed_constraints: 31

  best_config:
    Q_position: 10
    Q_velocity: 1
    R_input: 0.1
    horizon_N: 20
    position_rmse_m: 0.29
    control_effort: 10.4
    computation_time_p99_ms: 14.2

  pareto_frontier:
    - {Q_position: 10, R_input: 0.1, rmse: 0.29, effort: 10.4}
    - {Q_position: 50, R_input: 0.01, rmse: 0.21, effort: 18.7}

  recommendation: >
    Config with Q_position=10, R_input=0.1, N=20 offers best trade-off
    between tracking accuracy and control smoothness within timing constraint.
```

## Constraints

- Do not exceed the declared time budget.
- Do not skip constraint evaluation.
- Do not claim "globally optimal" from a finite grid search.
- State the search strategy and its limitations in the output.
- Do not change safety-critical parameters (e.g., emergency stop logic, geofence) during tuning.

---
name: robotics-result-analysis
description: >
  Analyse robotics and control experiment results using domain-appropriate metrics.
  Covers tracking, control effort, transient response, estimation, planning,
  mission, real-time timing, and robustness. Produces RESULT_SUMMARY.yaml.
platforms:
  - codex
  - claude
---

# Skill: robotics-result-analysis

## Purpose

Load experiment result files and compute domain-appropriate metrics.
Produce a structured summary ready for `robotics-experiment-audit` and
`robotics-result-to-claim`.

## Metric Catalogue

### Tracking

| Metric | Formula / definition |
|---|---|
| `position_rmse` | √(mean(‖p_ref − p‖²)) |
| `position_mae` | mean(‖p_ref − p‖) |
| `position_max_error` | max(‖p_ref − p‖) |
| `terminal_error` | ‖p_ref(T) − p(T)‖ at mission end |
| `relative_position_error` | ‖p_chaser − p_target‖ |
| `relative_velocity_error` | ‖v_chaser − v_target‖ |

### Control effort

| Metric | Definition |
|---|---|
| `total_control_effort` | Σ‖u(t)‖² Δt |
| `input_smoothness` | Σ‖Δu(t)‖² Δt (jerk proxy) |
| `actuator_saturation_fraction` | fraction of time at limits |
| `constraint_violations` | count of hard constraint breaches |

### Transient response

| Metric | Definition |
|---|---|
| `rise_time_s` | Time to first reach 90% of step target |
| `settling_time_s` | Time to stay within 2% of target |
| `overshoot_pct` | 100 × (peak − final) / final |
| `steady_state_error` | mean error after settling |

### Estimation

| Metric | Definition |
|---|---|
| `position_rmse_est` | RMSE of state estimate vs ground truth |
| `velocity_rmse_est` | |
| `orientation_error_deg` | |
| `normalized_innovation_squared` | NIS (χ² consistency test) |
| `normalized_estimation_error_squared` | NEES (χ² consistency) |

### Planning

| Metric | Definition |
|---|---|
| `path_length_m` | total trajectory arc length |
| `planning_time_s` | time to produce plan |
| `min_clearance_m` | minimum obstacle clearance |
| `replanning_rate` | replans per second |

### Mission

| Metric | Definition |
|---|---|
| `success_rate` | fraction of trials meeting success criterion |
| `collision_rate` | fraction of trials with collision |
| `completion_time_s` | mean time to mission success |
| `energy_J` | estimated energy consumption |
| `mission_timeout_rate` | fraction timed out |

### Real-time

| Metric | Definition |
|---|---|
| `computation_time_mean_ms` | |
| `computation_time_median_ms` | |
| `computation_time_p95_ms` | 95th percentile |
| `computation_time_p99_ms` | 99th percentile |
| `computation_time_max_ms` | |
| `deadline_miss_rate` | fraction exceeding control period |
| `solver_iterations_mean` | (MPC / optimisation-based controllers) |

### Robustness

| Metric | Definition |
|---|---|
| `noise_sensitivity` | metric degradation vs noise scaling |
| `delay_sensitivity` | metric degradation vs delay |
| `dropout_sensitivity` | metric degradation vs packet loss |
| `model_mismatch_sensitivity` | metric degradation vs model error |
| `disturbance_rejection` | RMSE at max tested disturbance |
| `wind_sensitivity` | (UAV / outdoor robotics) |
| `initial_condition_sensitivity` | metric variance across ICs |

## Instructions

### Step 1 — Load result files

Read from `EXPERIMENT.yaml`:
- `logging.csv` path
- `logging.rosbag` path (if present, extract relevant topics)
- `metrics` list

Inspect actual file content and verify metric columns exist.

### Step 2 — Select applicable metrics

Based on active profile (from `robotics-research-router`) and experiment type:
- Always include metrics specified in `EXPERIMENT.yaml`
- Add profile-recommended metrics from `profiles/*.yaml`

### Step 3 — Compute statistics

For **single-run** experiments: report raw values.

For **repeated trials** (repetitions > 1):
- mean, std, min, max
- 95% confidence interval if N ≥ 5
- Median and IQR if distribution is non-Gaussian

**Do not assert statistical significance** without a justified test.
State the test, p-value, and effect size if one is run.

### Step 4 — Flag anomalies

- NaN / Inf in any metric
- Actuator saturation > 5% of time (flag, do not fail)
- Constraint violations > 0
- RTF < 0.9 (flag simulation timing issue)
- Deadline miss rate > 1%

### Step 5 — Produce RESULT_SUMMARY.yaml

```yaml
experiment_id: EXP001
result_files:
  - results/EXP001/run_001.csv
metrics:
  position_rmse_m: {mean: 0.34, std: 0.04, n: 20}
  control_effort: {mean: 12.3, std: 1.1, n: 20}
  computation_time_p99_ms: {value: 8.2}
  success_rate: {value: 0.95, n: 20}
anomalies: []
evidence_level: L2  # from sil-hil-validation
next_skill: robotics-experiment-audit
```

## Constraints

- Never fabricate metric values.
- Never compute a metric from data that does not exist in the result files.
- Always state N (number of trials) for any aggregate statistic.
- Do not round aggressively; preserve enough decimal places to be scientifically meaningful.

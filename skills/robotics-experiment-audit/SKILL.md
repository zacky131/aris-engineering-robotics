---
name: robotics-experiment-audit
description: >
  Audit robotics experiment integrity: artifact existence, metric traceability,
  baseline fairness, simulation integrity, real-time integrity, scope, and
  claim-scope mismatch. Produces an audit report ready for robotics-result-to-claim.
platforms:
  - codex
  - claude
  - antigravity
---

# Skill: robotics-experiment-audit

## Purpose

Verify that experiment results are trustworthy before they are used as evidence.
Combines ARIS experiment-integrity patterns with robotics-specific checks.

## Audit Sections

### 1 — Artifact integrity

```
□ Result files listed in EXPERIMENT.yaml exist on disk
□ Metric values in RESULT_SUMMARY.yaml are present in source result files
□ Scripts that generated results are identified and present
□ Experiment status is marked complete (not in-progress or failed)
□ No result file has a modification timestamp after the experiment end time
```

### 2 — Baseline fairness

```
□ Same initial conditions (position, velocity, orientation)
□ Same reference trajectory or target motion
□ Same measurement noise model and seed
□ Same communication delay model
□ Same external disturbances (wind, payload)
□ Same constraint set
□ Same control rate
□ Same estimator (if comparison targets controller, not estimator)
□ Same hardware/simulator configuration
```

### 3 — Simulation integrity

```
□ Same physics step size for method and baseline
□ Same vehicle dynamics model
□ Same sensor model
□ Same collision model
□ Same Gazebo world / environment
```

### 4 — Real-time integrity

```
□ Solver computation time measured and logged
□ Communication overhead identified
□ Deadline miss behaviour documented
□ RTF ≥ threshold during experiment
```

### 5 — Scope

```
□ Number of trials documented
□ Number of random seeds documented
□ Scenario diversity assessed (one scenario vs. diverse?)
□ Platform count (one robot, one simulation world?)
□ Environment diversity (one initial condition, one disturbance level?)
```

### 6 — Claim-scope mismatch check

Flag examples:

| Observed | Prohibited claim |
|---|---|
| Simulation only | "real-world robustness" |
| One robot type | "general robotics" |
| One controller scenario | "fully robust" |
| One disturbance level | "arbitrary disturbance" |
| Workflow diagram in paper | "experimental validation" |
| Single successful demo | "deployment readiness" |
| One initial condition | "initial-condition agnostic" |

## Instructions

### Step 1 — Load audit context

Read:
- `EXPERIMENT.yaml`
- `RESULT_SUMMARY.yaml`
- `EVIDENCE_LEDGER.yaml`
- `CLAIM_MAP.yaml`

### Step 2 — Run each audit section

For each check:
- PASS: verified
- WARNING: minor concern; note action
- FAIL: integrity issue; block advancement to claim
- NOT_VERIFIABLE: data not available to check

### Step 3 — Block advancement if FAIL exists

If any check returns FAIL:
- Do not proceed to `robotics-result-to-claim`.
- List required corrective actions.

### Step 4 — Output audit report

```yaml
experiment_audit:
  experiment_id: EXP001
  overall: PASS  # PASS | CONDITIONAL | BLOCKED

  artifact_integrity:
    result_files_exist: PASS
    metrics_match_source: PASS
    scripts_identified: WARNING
    note: "run_experiment.sh identified but commit hash not recorded"

  baseline_fairness:
    shared_initial_conditions: PASS
    shared_noise_seed: PASS
    shared_disturbance: FAIL
    fail_detail: "PID baseline ran without wind; MPC ran with wind=0.5m/s"

  simulation_integrity:
    physics_step: PASS
    collision_model: PASS

  real_time_integrity:
    computation_time_logged: PASS
    rtf_ok: PASS

  scope:
    trials: {status: PASS, n: 20}
    seeds: {status: PASS, n: 5}
    scenarios: {status: WARNING, note: "Single scenario type; Q2 mechanism not tested"}

  claim_mismatch:
    - {claim: C002, issue: "simulation → real-world robustness claim", action: "Downgrade or add L5 evidence"}

  required_actions:
    - "Apply same wind disturbance to PID baseline runs"
    - "Add result script commit hash to EVIDENCE_LEDGER"
    - "Revise C002 claim language"
```

## Constraints

- Never mark `overall: PASS` if any FAIL is present.
- Never mark a check PASS without verifying the underlying artifact.
- Do not invent file content that has not been read.

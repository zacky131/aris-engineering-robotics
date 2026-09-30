---
name: simulation-validation
description: >
  Audit whether simulation results are scientifically interpretable.
  Checks physics configuration, real-time factor, baseline fairness, and
  shared experimental conditions. Flags any asymmetry that would invalidate
  a comparison.
platforms:
  - codex
  - claude
---

# Skill: simulation-validation

## Purpose

Before results are used as evidence, verify that the simulation was
configured in a way that makes results scientifically interpretable.

A simulation result is scientifically valid only when:
1. The configuration faithfully represents the intended scenario.
2. All methods and baselines were tested under identical conditions.
3. The simulation fidelity is appropriate for the claims made.

## Instructions

### Step 1 — Load configuration

Read:
- `EXPERIMENT.yaml`
- Simulator configuration files (world files, launch arguments)
- Controller launch files for method and baseline

### Step 2 — Physics fidelity checks

```
□ physics_step_ms: documented and appropriate for the dynamics
□ control_sampling_rate_hz: consistent with real system requirements
□ sensor_update_rate_hz: consistent with claimed sensor type
□ real_time_factor: ≥ 0.95 for claimed timing results
□ vehicle_dynamics: appropriate model (rigid body, aerodynamics level)
□ actuator_limits: match real system specification
□ collision_model: enabled and appropriate
□ latency_ms: modelled if claimed in system
□ dropout: modelled if claimed in system
```

### Step 3 — Baseline fairness checks

For each comparison experiment:

```
□ Same initial condition (position, velocity, orientation, state estimate)
□ Same reference trajectory / target
□ Same sensor noise model and seed
□ Same disturbance model and seed
□ Same delay model
□ Same scenario duration
□ Same control sampling rate
□ Same estimator (if comparison targets controller, not estimator)
□ Same physical constraints
□ Same collision model
□ Same random seed policy (shared or documented)
```

Flag any asymmetry.

### Step 4 — Seed and reproducibility check

```
□ Random seeds documented
□ Seed policy explicit: fixed | random | matched-across-methods
□ Results reproducible from documented seeds
```

### Step 5 — Scope and fidelity assessment

Classify:

| Claim type | Required minimum fidelity |
|---|---|
| "Method improves tracking in simulation" | L2 physics simulation |
| "Method is robust to wind" | L2 + disturbance model |
| "Method meets real-time constraint" | L3 (SIL) or L4 (HIL) |
| "Method works on real robot" | L5 |
| "Method ready for deployment" | L5 or L6 |

Flag any mismatch between claim scope and achieved fidelity.

### Step 6 — Output

```yaml
simulation_validation:
  experiment_id: EXP001
  overall: VALID  # VALID | CONDITIONALLY_VALID | INVALID

  physics_checks:
    physics_step_ms: {status: PASS, value: 2.0}
    real_time_factor: {status: PASS, value: 0.97}
    actuator_limits: {status: PASS}
    latency_modeled: {status: WARNING, note: "No latency model; claimed latency insensitivity unvalidated"}

  fairness_checks:
    shared_initial_conditions: {status: PASS}
    shared_noise_seed: {status: PASS}
    shared_disturbance: {status: FAIL, note: "Method tested with wind; baseline without wind"}

  scope_assessment:
    evidence_level: L2
    claims_within_scope: [C001]
    claims_exceeding_scope: [C002]
    note: "C002 claims real-world robustness; only L2 evidence available"

  required_actions:
    - "Apply same wind disturbance to baseline runs"
    - "Downgrade or remove C002 real-world robustness claim"
```

## Constraints

- Never mark `overall: VALID` if any FAIL is present in fairness_checks.
- Do not invent simulator configuration that is not documented.
- If configuration files are missing, report as `NOT_VERIFIABLE` not `PASS`.

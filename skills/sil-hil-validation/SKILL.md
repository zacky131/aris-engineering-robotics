---
name: sil-hil-validation
description: >
  Classify the evidence level of robotics research results using the L0–L6
  hierarchy. Prevent manuscripts from claiming higher evidence than produced.
  Outputs evidence level per experiment and per claim.
platforms:
  - codex
  - claude
  - antigravity
---

# Skill: sil-hil-validation

## Purpose

Classify what evidence level has actually been produced by each experiment,
and verify that manuscript claims do not exceed the highest evidence level obtained.

## Evidence Level Hierarchy

| Level | Name | Description | Example |
|---|---|---|---|
| L0 | Theoretical / analytical | Mathematical proof, stability analysis, BIBO, Lyapunov | Stability theorem, convergence proof |
| L1 | Numerical simulation | ODE solver, no physics engine | MATLAB ode45, scipy.integrate |
| L2 | Physics simulation | Physics engine with rigid body, collision, aerodynamics | Gazebo, Isaac, PyBullet |
| L3 | Software-in-the-loop | Real controller code running against simulated plant | PX4 SITL, ArduPilot SITL |
| L4 | Hardware-in-the-loop | Real hardware components (sensors, MCU) in simulated plant loop | HIL bench, dSPACE HIL |
| L5 | Controlled physical experiment | Full physical system in controlled indoor/outdoor environment | Lab flight test, indoor arena |
| L6 | Operational / field | Uncontrolled real environment, operational conditions | Outdoor field, industrial site |

## Instructions

### Step 1 — Map each experiment to its evidence level

For each experiment in `EXPERIMENT.yaml` or `EVIDENCE_LEDGER.yaml`:

Read `platform.type` and `platform.simulator`:

| platform.type | platform.autopilot | Assigned level |
|---|---|---|
| `numerical_simulation` | — | L1 |
| `simulation` | — | L2 |
| `simulation` | `px4` | L3 (SITL) |
| `simulation` | `ardupilot` | L3 (SITL) |
| `hil` | any | L4 |
| `real` | any | L5 or L6 (ask user to confirm environment) |

If `platform.type` is not set, ask the user to confirm.

### Step 2 — Determine project evidence level

The project-level evidence level is the **maximum** level achieved across all completed experiments.

### Step 3 — Audit manuscript claims

For each claim in `CLAIM_MAP.yaml`:

Check the claim language for:

| Forbidden at level | Claim phrase |
|---|---|
| L2 and below | "real-world robustness" |
| L2 and below | "deployment ready" |
| L2 and below | "field proven" |
| L3 and below | "hardware validated" |
| L4 and below | "operationally tested" |
| L5 | "generalises to arbitrary environments" |

Flag any mismatch.

### Step 4 — Assign permitted claim language per evidence level

| Level | Permitted verbs | Typical scope |
|---|---|---|
| L0 | "proves", "guarantees" (scope: mathematical) | Theoretical properties only |
| L1–L2 | "indicates", "suggests", "supports" | Simulation only |
| L3 | "indicates in SIL context", "demonstrates in software-in-the-loop" | Code correctness + simulation |
| L4 | "demonstrates in HIL", "supports hardware feasibility" | Hardware timing + integration |
| L5 | "demonstrates in physical experiment", "shows" | Controlled lab environment |
| L6 | "demonstrates operationally", "confirms" | Field environment |

### Step 5 — Output

```yaml
sil_hil_report:
  experiments:
    EXP001: {level: L2, basis: "Gazebo physics simulation, PX4 SITL"}
    EXP002: {level: L3, basis: "PX4 SITL with real flight controller code"}
    EXP003: {level: L3, basis: "PX4 SITL"}

  project_evidence_level: L3

  claims_audit:
    C001:
      text: "MPC reduces tracking error under the evaluated scenarios"
      level_required: L2
      level_available: L3
      status: WITHIN_SCOPE
      permitted_verbs: [indicates, supports, demonstrates in SIL]

    C002:
      text: "The system is robust to real-world wind disturbances"
      level_required: L5
      level_available: L3
      status: EXCEEDS_SCOPE
      required_action: "Revise claim to 'simulation indicates robustness to modelled wind disturbances'"
```

## Constraints

- Never upgrade an evidence level without actual evidence.
- If `platform.type == real` but no hardware experiment log exists, classify as `NOT_VERIFIED`.
- A figure generated from simulation data does not elevate evidence to L5.
- Paper text must not use higher-level language than the project's evidence level permits.

---
name: robotics-result-to-claim
description: >
  Convert robotics/control experiment results into evidence-calibrated claims.
  Extends ARIS result-to-claim with L0–L6 evidence levels, platform scope,
  scenario scope, simulation-vs-real scope, and real-time scope. Updates CLAIM_MAP.yaml.
platforms:
  - codex
  - claude
  - antigravity
---

# Skill: robotics-result-to-claim

## Purpose

Given a verified `RESULT_SUMMARY.yaml` and passed `robotics-experiment-audit`,
generate or update manuscript claims with precisely calibrated language that
does not exceed the evidence produced.

## Prerequisites

- `robotics-experiment-audit` must return `overall: PASS` or `overall: CONDITIONAL`
- `sil-hil-validation` evidence level must be assigned
- `RESULT_SUMMARY.yaml` must be present and verified

## Instructions

### Step 1 — Load evidence context

Read:
- `RESULT_SUMMARY.yaml` (metrics)
- `sil-hil-validation` output (evidence level L0–L6)
- `robotics-experiment-audit` output (scope, fairness, mismatch flags)
- `CLAIM_MAP.yaml` (existing claims to update)
- Active profile (for domain context)

### Step 2 — For each claim candidate, assess

For each metric or finding:

**Evidence scope dimensions:**

| Dimension | Question |
|---|---|
| Platform scope | Was this tested on one robot type, multiple types? |
| Scenario scope | One scenario, diverse scenarios? |
| Condition scope | One disturbance level, multiple? |
| Statistical scope | One trial, N trials with statistics? |
| Simulation vs real | L1/L2/L3 vs L5/L6? |
| Real-time scope | Timing measured? On what hardware? |
| Failure envelope | Where does the method stop working? |

### Step 3 — Select permitted claim verbs

Match to evidence level:

| Evidence level | Permitted verbs |
|---|---|
| L1 | "suggests (numerically)" |
| L2 | "indicates", "suggests" |
| L3 | "supports", "indicates (in SIL)" |
| L4 | "demonstrates (HIL)", "supports hardware feasibility" |
| L5 | "shows", "demonstrates" |
| L6 | "confirms", "demonstrates operationally" |

Never use: "proves" (unless L0 analytical), "guarantees", "fully robust",
"generalises", "real-world ready", "industry ready", "state of the art" —
unless evidence specifically supports that claim.

### Step 4 — Write calibrated claims

For each claim:

```yaml
C001:
  text: >
    The proposed MPC controller indicates improved tracking accuracy
    compared to the PID baseline under the evaluated maneuver-transition
    scenarios in Gazebo simulation.
  evidence:
    - E001
    - E002
  evidence_level: L2
  status: supported
  permitted_language: [indicates, supports]
  platform_scope: "Single UAV type (Iris quadrotor)"
  scenario_scope: "Two scenario types: constant-velocity, maneuver-transition"
  statistical_scope: "N=20 trials per condition"
  real_time_scope: "Computation time measured in SIL; not on target embedded hardware"
  prohibited_extensions:
    - real-world generalization
    - hardware validation
    - arbitrary maneuver robustness
  missing_evidence:
    - Physical experiment (L5)
    - Diverse vehicle types
    - Larger scenario set
  next_experiments:
    - EXP_HIL: HIL validation on Pixhawk
    - EXP_FIELD: Lab flight test
```

### Step 5 — Identify missing evidence

For each MUST claim (core contribution):
- Is the current evidence sufficient to support the claim?
- If not: specify exactly what additional experiment is needed.

### Step 6 — Update CLAIM_MAP.yaml

Write updated claims to `CLAIM_MAP.yaml`.

### Step 7 — Output summary

```yaml
result_to_claim_summary:
  claims_supported: [C001, C003]
  claims_partial: [C002]
  claims_unsupported: []
  missing_evidence_for_partial:
    C002: ["Physical experiment at tested disturbance levels"]
  recommended_next_skills:
    - engineering-paper-auditor  # if claims are sufficient
    - robotics-experiment-plan   # if additional experiments needed
```

## Constraints

- Never write a claim that is not supported by verified results.
- Never upgrade evidence level beyond what `sil-hil-validation` assigned.
- Never remove scope qualifiers from claims.
- If audit returned BLOCKED, do not proceed to claim generation.

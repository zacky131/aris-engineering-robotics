# Robotics Experiment Model

## Experiment Contract

Every experiment is described by `EXPERIMENT.yaml` (schema: `schemas/experiment.schema.json`).

Key sections:
- `experiment`: ID, name, domain, priority, linked claims
- `platform`: simulation/SIL/HIL/real + middleware + simulator + autopilot
- `system`: robot, controller, estimator
- `scenario`: name, duration, repetitions, seed policy
- `disturbance`: wind, noise, latency, dropout
- `logging`: rosbag, CSV, stdout
- `metrics`: list of metrics to compute

## Hardware Safety Boundary

**Physical actuation always requires human approval.**

The `run-robotics-experiment` skill will stop with `HARDWARE_GATE` for:
- `platform.type: real`
- `platform.type: hil`

The skill may prepare commands and configs but will not autonomously:
- Arm a UAV
- Start motors
- Move a physical robot
- Disable emergency stops or geofencing

## Evidence Lifecycle

```
EXPERIMENT.yaml filled
     ↓
run-robotics-experiment
     ↓
robotics-watchdog (monitoring)
     ↓
result files on disk
     ↓
robotics-result-analysis → RESULT_SUMMARY.yaml
     ↓
robotics-experiment-audit
     ↓
sil-hil-validation → evidence level assigned
     ↓
robotics-result-to-claim → CLAIM_MAP.yaml updated
     ↓
validate_evidence_ledger.py → verified: true
```

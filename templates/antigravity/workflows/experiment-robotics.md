# Workflow: Experiment Robotics

**Purpose**: Execute, monitor, analyse, and audit a robotics experiment,
then convert verified results into evidence-calibrated claims.

**Invoke with**: An existing `EXPERIMENT.yaml`, e.g.
```
Use the experiment-robotics workflow for EXP001.
```

---

## Pre-conditions

Before starting, verify:
- `EXPERIMENT.yaml` exists and is valid
- `EVIDENCE_LEDGER.yaml` exists (copy from `templates/` if absent)
- `CLAIM_MAP.yaml` exists (copy from `templates/` if absent)

---

## Stage 1 — Experiment planning (if not already done)

**Skill**: `robotics-experiment-plan`

Skip this stage if `EXPERIMENT.yaml` is already filled and reviewed.

Verify:
- All MUST_RUN experiments are defined
- Each experiment is mapped to one or more claims

## Stage 2 — Implementation check (if needed)

**Skill**: `research-implement-feature`

Check whether required code/integration is in place:
- Controller node
- Estimator node
- ROS 2 launch files
- Gazebo world file
- PX4 parameter configuration (if PX4 platform)

Skip if implementation is complete.

## Stage 3 — Run experiment

**Skill**: `run-robotics-experiment`

Load `EXPERIMENT.yaml` and execute.

**HARDWARE_GATE**: If `platform.type: real` or `platform.type: hil` —
**STOP**. Output the manual step. Do not autonomously actuate hardware.

For simulation platforms (`simulation`, `sil`), execute the launch sequence.

Track all started PIDs. Only manage those PIDs.

## Stage 4 — Monitor health

**Skill**: `robotics-watchdog`

Monitor for:
- Process failures
- ROS topic frequency issues
- TF availability
- Estimator divergence (NaN/Inf)
- Real-time factor
- Solver feasibility
- Logging active

Report `HEALTHY` / `DEGRADED` / `FAILED`.

## Stage 5 — Analyse results

**Skill**: `robotics-result-analysis`

Load result files from `EXPERIMENT.yaml` → `logging.output_dir`.
Compute domain-appropriate metrics.
Produce `RESULT_SUMMARY.yaml`.

Do not fabricate metrics. Only compute from actual result files.

## Stage 6 — Audit experiment integrity

**Skill**: `robotics-experiment-audit`

Check:
- Source files exist
- Metrics match sources
- Baseline fairness (shared conditions, seeds, noise)
- Simulation integrity
- Real-time integrity

If any check returns `FAIL` → stop and list required corrections before advancing.

## Stage 7 — Classify evidence level

**Skill**: `sil-hil-validation`

Assign L0–L6 evidence level based on `platform.type`.
Update `EVIDENCE_LEDGER.yaml` with the evidence level.

## Stage 8 — Map results to claims

**Skill**: `robotics-result-to-claim`

Generate evidence-calibrated claims.
Update `CLAIM_MAP.yaml` with:
- Supported / partial / unsupported status
- Permitted language (from evidence level)
- Missing evidence
- Next experiments needed

---

## Output

At the end:
- `RESULT_SUMMARY.yaml` — filled metrics
- `EVIDENCE_LEDGER.yaml` — updated with verified evidence
- `CLAIM_MAP.yaml` — updated claim status
- List of any corrective actions needed

Do not advance to paper writing until all MUST claims are `supported` or `partial`
with a clear plan for missing evidence.

---
name: research-pipeline-robotics
description: >
  Full orchestration pipeline for robotics/control research. Stages 1–21 from
  research question to submission validation. Includes explicit stopping criteria
  and hardware safety gates. Does not self-loop indefinitely.
platforms:
  - codex
  - claude
---

# Skill: research-pipeline-robotics

## Purpose

Orchestrate a complete robotics research workflow from research question to
submission-ready manuscript.

This skill coordinates other skills and tracks pipeline state. It does **not**
implement each stage itself — it calls the appropriate skill for each stage.

## Stopping Criteria

The pipeline stops when any of the following conditions is met:

| Condition | Action |
|---|---|
| `max_experiment_iterations` reached (default: 3) | Stop, report remaining gaps |
| `max_tuning_budget` reached | Stop tuning, proceed with best config |
| `claim_evidence_complete` for all MUST claims | Advance to paper stage |
| `no_additional_experiment_justified` | Advance to paper stage |
| `HARDWARE_GATE` triggered | Stop, output manual step instructions |
| `time_budget` reached | Stop, report status |
| User manual stop | Stop immediately |

**The pipeline never loops indefinitely.**

## Pipeline Stages

### Stage 1 — Understand research question

Skills: ARIS `research-lit`, user clarification
- Confirm research domain, problem, gap, proposed method
- Confirm evaluation scope

### Stage 2 — Select robotics/control profile

Skill: `robotics-research-router`
- Detect profile(s)
- Load appropriate metrics and watchdog checks

### Stage 3 — Literature search

Skill: ARIS `research-lit`
- Domain-specific papers
- Baseline methods
- Benchmark scenarios

### Stage 4 — Gap and novelty analysis

Skill: ARIS `novelty-check`
- Confirm method is distinct from prior work

### Stage 5 — Research refinement

Skill: ARIS `research-refine`
- Sharpen research question and contribution

### Stage 6 — Define initial claims

Skill: ARIS `claims-drafting`
- Draft placeholder claims to guide experiment design

### Stage 7 — Design experiment plan

Skill: `robotics-experiment-plan`
- Q1–Q6 experiment design
- Run matrix generation
- Claim-to-experiment mapping

### Stage 8 — Implement missing functionality

Skill: ARIS `research-implement-feature`
- Implement controller, estimator, or integration gaps
- Confirm ROS 2 / Gazebo / PX4 integration

### Stage 9 — Run experiments

Skill: `run-robotics-experiment`
- Execute MUST_RUN experiments
- Respect HARDWARE_GATE

### Stage 10 — Monitor experiment health

Skill: `robotics-watchdog`
- Detect failures early
- Log all anomalies

### Stage 11 — Analyse results

Skill: `robotics-result-analysis`
- Compute domain metrics
- Produce RESULT_SUMMARY.yaml

### Stage 12 — Audit experiment integrity

Skill: `robotics-experiment-audit`
- Verify artifact integrity
- Verify baseline fairness
- Detect claim mismatch

### Stage 13 — Map results to claims

Skill: `robotics-result-to-claim`
- Update CLAIM_MAP.yaml
- Assign evidence levels

### Stage 14 — Detect missing evidence

Read CLAIM_MAP.yaml:
- Is any MUST claim still `status: partial` or `status: unsupported`?
- If yes and iteration budget remains: plan additional experiment (Stage 7)
- If no or budget exhausted: advance

### Stage 15 — Run additional experiments if justified

Conditional stage. Skipped if:
- All MUST claims are supported, or
- Experiment iteration budget exhausted, or
- Only HARDWARE_GATE experiments remain

### Stage 16 — Freeze evidence ledger

- Mark `EVIDENCE_LEDGER.yaml` as frozen (no further edits without audit)

### Stage 17 — Audit paper story

Skill: EPS `engineering-paper-auditor`
- Check story spine
- Check claim-evidence alignment

### Stage 18 — Write/revise manuscript

Skill: EPS `engineering-writing`
- Draft or revise sections

### Stage 19 — Audit figures/tables

Skill: EPS `engineering-figure-table`
- Trace source data to figure values
- Trace figure to caption to claim

### Stage 20 — Polish

Skill: EPS `engineering-polishing`
- Language, terminology, flow

### Stage 21 — Validate submission package

Skill: EPS `engineering-validation`
- Format, completeness, venue requirements

## State Tracking

The pipeline writes its state to `RESEARCH_CONTRACT.md`:

```yaml
pipeline_state:
  current_stage: 11
  experiment_iteration: 1
  max_experiment_iterations: 3
  claims_supported: [C001]
  claims_partial: [C002]
  last_updated: "2026-09-30"
  next_action: "Analyse EXP001 results"
```

## Output on Completion

```
Pipeline complete.

Stages completed: 1–21
Claims supported: C001, C002, C003
Evidence level: L3 (SIL)
Manuscript status: ready for submission validation

Commands:
  bash tools/install_skills.sh --platform codex
  python tools/validate_installation.py
  python tools/validate_evidence_ledger.py
```

## Constraints

- Do not advance past Stage 16 if any MUST claim is unsupported.
- Do not re-run failed experiments more than `max_experiment_iterations` times.
- Always stop at HARDWARE_GATE and clearly describe the manual step.
- Do not skip Stage 12 (audit) before Stage 13 (result-to-claim).
- Do not skip Stage 13 before Stage 18 (writing).

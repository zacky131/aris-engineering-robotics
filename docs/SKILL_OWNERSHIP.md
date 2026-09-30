# Skill Ownership

This document resolves skill routing ambiguity across ARIS, Engineering Paper Skills,
and the new Robotics/Control layer.

When a task can be handled by more than one skill, the **Primary** skill owns the task.
The **Secondary** skill may be consulted for supplementary guidance.

---

## Routing Table

| Task | Primary Skill | Secondary Skill | Notes |
|---|---|---|---|
| Literature search | ARIS `research-lit` | — | Domain-agnostic; works for all robotics subfields |
| Idea discovery (general) | ARIS `idea-discovery` | — | |
| Idea discovery (robotics) | ARIS `idea-discovery-robot` | robotics router | Robotics-specific variant already in ARIS |
| Novelty assessment | ARIS `novelty-check` | engineering evidence rules | |
| Research question refinement | ARIS `research-refine` | — | |
| Formula derivation | ARIS `formula-derivation` | — | |
| Implementation planning | ARIS `research-implement-feature` | robotics profile | Profile provides domain-specific constraints |
| ML experiment execution | ARIS `run-experiment` | robotics result analysis | GPU-based; not default for robotics |
| **ROS 2 / Gazebo / PX4 experiment** | `run-robotics-experiment` | `robotics-watchdog` | New skill owns robotics experiment lifecycle |
| Experiment planning (general) | ARIS `experiment-plan` | — | Use for ML / general |
| **Experiment planning (robotics)** | `robotics-experiment-plan` | ARIS `experiment-plan` | Q1–Q6 robotics framework; owns robotics domain |
| Experiment health monitoring (ML) | ARIS `monitor-experiment` | — | GPU/loss curve monitoring |
| **Experiment health monitoring (robotics)** | `robotics-watchdog` | — | ROS2 topics, TF, Gazebo, PX4, timing |
| **Controller parameter tuning** | `controller-tuning` | ARIS `dse-loop` | DSE patterns reused from ARIS |
| General result analysis | ARIS `analyze-results` | — | |
| **Robotics result analysis** | `robotics-result-analysis` | ARIS `analyze-results` | Domain-aware metrics (RMSE, timing, mission) |
| Ablation design | ARIS `ablation-planner` | — | |
| **Experiment integrity audit (robotics)** | `robotics-experiment-audit` | ARIS `experiment-audit` | Robotics-specific + baseline fairness |
| **Simulation scientific validity** | `simulation-validation` | — | Physics step, RTF, shared conditions |
| **SIL/HIL evidence classification** | `sil-hil-validation` | — | L0–L6 classification |
| General result → claim | ARIS `result-to-claim` | — | Use for ML / general |
| **Robotics result → claim** | `robotics-result-to-claim` | ARIS `result-to-claim` | Adds L0–L6, scope, platform boundary |
| Profile detection | `robotics-research-router` | — | Entry point for all robotics research tasks |
| Full pipeline (general) | ARIS `research-pipeline` | — | |
| **Full pipeline (robotics)** | `research-pipeline-robotics` | ARIS `research-pipeline` | Robotics-adapted orchestration with stopping criteria |
| Paper structure / writing | EPS `engineering-writing` | ARIS `paper-write` | EPS is primary for engineering papers |
| Paper coaching | EPS `engineering-paper-coach` | — | |
| Manuscript full audit | EPS `engineering-paper-auditor` | ARIS `paper-claim-audit` | EPS is primary |
| Claim-evidence alignment check | EPS `engineering-paper-auditor` | ARIS `paper-claim-audit` | |
| Initial claim drafting | ARIS `claims-drafting` | `robotics-result-to-claim` | Generate claims from results |
| Figures and tables | EPS `engineering-figure-table` | — | |
| Language polishing | EPS `engineering-polishing` | — | |
| Reviewer response | EPS `engineering-response` | ARIS `rebuttal` | EPS is primary for engineering venues |
| Submission validation | EPS `engineering-validation` | — | |
| Citation audit | ARIS `citation-audit` | — | |
| Paper compilation | ARIS `paper-compile` | EPS `engineering-validation` | |
| Peer review simulation | ARIS `research-review` | — | |
| Task routing (paper layer) | EPS `engineering-paper-router` | `robotics-research-router` | EPS router for paper tasks; robotics router for experiment tasks |

---

## Routing Decision Logic

```
User request received
        │
        ▼
Is this about paper writing, auditing, figures, or reviewer response?
  YES → engineering-paper-router → EPS skill
  NO  ↓

Is this a robotics/control experiment task?
  YES → robotics-research-router → robotics skill
  NO  ↓

Is this a research-front task (literature, ideas, novelty)?
  YES → ARIS skill directly
  NO  ↓

Is this a full research pipeline?
  YES → research-pipeline-robotics (robotics) or research-pipeline (general)
```

---

## Notes

- Do not invoke two skills that own the same task in parallel for the same artifact.
- When the primary skill is unavailable (not installed), fall back to the secondary.
- Always check `CLAIM_MAP.yaml` status before advancing from experiment to paper layer.

# Architecture

## Overview

ARIS Engineering Robotics is a three-layer integration system.

```mermaid
flowchart TD
    A["ARIS Research Layer\nresearch-lit · idea-discovery · novelty-check\nexperiment-plan · research-implement-feature\npaper-claim-audit · research-review · rebuttal"]
    B["Robotics / Control Layer (NEW)\nrobotics-research-router · robotics-experiment-plan\nrun-robotics-experiment · robotics-watchdog\nrobotics-result-analysis · controller-tuning\nrobotics-experiment-audit · simulation-validation\nsil-hil-validation · robotics-result-to-claim\nresearch-pipeline-robotics"]
    C["Engineering Paper Layer\nengineering-writing · engineering-polishing\nengineering-paper-auditor · engineering-figure-table\nengineering-response · engineering-validation"]
    D["Evidence Artifacts\nEVIDENCE_LEDGER.yaml\nCLAIM_MAP.yaml\nRESULT_SUMMARY.yaml"]

    A --> B
    B --> D
    D --> C
    B --> C
```

---

## Layer Responsibilities

### ARIS Research Layer

Primary source: `Auto-claude-code-research-in-sleep`

| Responsibility | Skill |
|---|---|
| Literature search | `research-lit` |
| Idea discovery | `idea-discovery`, `idea-discovery-robot` |
| Novelty assessment | `novelty-check` |
| Experiment planning (general) | `experiment-plan` |
| Implementation | `research-implement-feature` |
| Results analysis (general) | `analyze-results` |
| Ablation design | `ablation-planner` |
| Claim-evidence audit | `paper-claim-audit` |
| Peer-review of own paper | `research-review` |
| Reviewer response | `rebuttal` |
| Claim drafting | `claims-drafting` |

### Robotics / Control Layer

Primary source: this repository

| Responsibility | Skill |
|---|---|
| Profile detection and routing | `robotics-research-router` |
| Robotics experiment design | `robotics-experiment-plan` |
| Experiment execution | `run-robotics-experiment` |
| Experiment health monitoring | `robotics-watchdog` |
| Result analysis | `robotics-result-analysis` |
| Controller parameter tuning | `controller-tuning` |
| Experiment integrity audit | `robotics-experiment-audit` |
| Simulation validity | `simulation-validation` |
| SIL/HIL evidence classification | `sil-hil-validation` |
| Result → claim generation | `robotics-result-to-claim` |
| Full pipeline orchestration | `research-pipeline-robotics` |

### Engineering Paper Layer

Primary source: `engineering-paper-skills`

| Responsibility | Skill |
|---|---|
| Manuscript writing | `engineering-writing` |
| Language polishing | `engineering-polishing` |
| Full paper audit | `engineering-paper-auditor` |
| Figure/table generation + tracing | `engineering-figure-table` |
| Reviewer response | `engineering-response` |
| Submission validation | `engineering-validation` |
| Task routing | `engineering-paper-router` |

---

## Evidence Flow

```mermaid
flowchart LR
    R["Raw result files\n(CSV, rosbag, log)"]
    RA["robotics-result-analysis"]
    EA["robotics-experiment-audit"]
    RC["robotics-result-to-claim"]
    EL["EVIDENCE_LEDGER.yaml"]
    CM["CLAIM_MAP.yaml"]
    PA["engineering-paper-auditor"]
    EW["engineering-writing"]
    FT["engineering-figure-table"]
    EP["engineering-polishing"]
    EV["engineering-validation"]

    R --> RA --> EA --> RC --> EL --> CM
    CM --> PA --> EW --> FT --> EP --> EV
```

---

## Profiles

Research profiles activate the correct metric sets, watchdog checks, and
experiment templates.

```mermaid
flowchart TD
    Router["robotics-research-router"]
    Router --> P1["classical_control\nPID · LQR · MPC · SMC\nKalman · EKF · UKF · IMM"]
    Router --> P2["ros2_robotics\nROS 2 · Nav2 · SLAM\nsensor fusion · rosbag"]
    Router --> P3["px4_uav\nPX4 SITL · MAVLink\nuXRCE-DDS · offboard"]
    Router --> P4["multi_robot\nMARL · coordination\ncollision · coverage"]
    Router --> P5["learning_robotics\nPPO · SAC · TD3\nMARL · imitation"]
    Router --> P6["hybrid_ai_control\nlearned + classical\nmixed metrics"]
```

---

## Evidence Level Hierarchy

```mermaid
flowchart BT
    L0["L0: Theoretical / analytical"]
    L1["L1: Numerical simulation"]
    L2["L2: Physics simulation (Gazebo)"]
    L3["L3: Software-in-the-loop (SIL)"]
    L4["L4: Hardware-in-the-loop (HIL)"]
    L5["L5: Controlled physical experiment"]
    L6["L6: Operational / field"]

    L0 --> L1 --> L2 --> L3 --> L4 --> L5 --> L6
```

Claims may not exceed the level of evidence produced.

---

## Upstream Reference Strategy

Skills from ARIS and EPS are **referenced, not vendored**.

```
aris-engineering-robotics/         ← this repo
    tools/install_skills.sh        ← copies or symlinks upstream skills
    .aris-engineering-robotics/
        config.yaml                ← configurable upstream paths
        installed-skills.txt       ← manifest of what was installed
```

No upstream repository is modified.

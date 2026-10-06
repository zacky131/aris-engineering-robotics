# ARIS Engineering Robotics

<!-- BEGIN ARIS-ENGINEERING-ROBOTICS -->

This project uses **ARIS Engineering Robotics** for research in robotics,
control, autonomous systems, and engineering-paper workflows.

Skills are available in `.agents/skills/`. Call them by name in your prompts.

---

## Anchor Papers

If `anchor_papers/` contains PDF files, process them with
`anchor-paper-intake` before starting broad literature search,
novelty analysis, idea generation, or experiment planning.

Anchor-paper limitations are hypotheses, not confirmed current research gaps.
Verify them independently against recent literature.

---

## Research Routing

**For unfamiliar robotics/control research tasks:**
```
Use the robotics-research-router skill.
```

**For literature and novelty:**
```
Use the research-lit skill.
Use the idea-discovery skill.
Use the novelty-check skill.
```

**For experiment design:**
```
Use the robotics-experiment-plan skill.
```

**For Vision-Language-Action & Embodied AI:**
```
Use the vla-robotics skill.
Use the safety-filter-cbf skill.
```

**For Learning-Based & AI Control:**
```
Use the learning-control-eval skill.
Use the safety-filter-cbf skill.
```

**For experiment execution:**
```
Use the run-robotics-experiment skill.
```

**For experiment health monitoring:**
```
Use the robotics-watchdog skill.
```

**For result analysis → evidence → claims:**
```
Use the robotics-result-analysis skill.
Then: robotics-experiment-audit
Then: robotics-result-to-claim
```

**For paper writing:**
```
Use the engineering-paper-auditor skill.
Then: engineering-writing
Then: engineering-figure-table
Then: engineering-polishing
Then: engineering-validation
```

**For the full end-to-end pipeline:**
```
Use the research-pipeline-robotics skill.
```

---

## Scientific Integrity (mandatory)

Never invent or fabricate:
- experiments
- trials
- result values or metrics
- baselines
- statistical significance
- hardware test results
- citations or references
- manuscript changes

All claims must trace to real result files in `EVIDENCE_LEDGER.yaml`.

Maintain the research story spine:
```
problem → gap → insight → method → evidence → boundary → implication
```

Simulation evidence (Gazebo, PX4 SITL) must never be described as
real-world physical evidence.

---

## Evidence Artifacts

Use these files when present:
- `EXPERIMENT.yaml` — experiment configuration
- `EVIDENCE_LEDGER.yaml` — verified result records
- `CLAIM_MAP.yaml` — evidence-calibrated claims
- `RESULT_SUMMARY.yaml` — per-experiment metric summary

Copy them from `templates/` (in the aris-engineering-robotics repo) if absent.

---

## Physical Robot Safety

**Never autonomously:**
- arm a UAV
- start motors
- move a physical robot
- disable collision protection
- disable geofencing
- bypass an emergency stop
- command safety-critical hardware

Physical actuation always requires explicit human approval.
The `run-robotics-experiment` skill enforces `HARDWARE_GATE` for real/HIL platforms.

---

## Supported Profiles

The `robotics-research-router` skill detects your research context and activates
the correct metric set and watchdog checks:

| Profile | Typical methods/stack |
|---|---|
| `classical_control` | PID, LQR, MPC, NMPC, SMC, EKF, UKF, IMM |
| `learning_control` | DRL, PPO, SAC, TD3, RMA, domain randomization, sim-to-real |
| `ai_control` | Neural ODE, PINN, Neural MPC, GP-MPC, residual control |
| `safe_sota_control` | Control Barrier Functions (CBF), QP safety filter / shield |
| `vla_robotics` | OpenVLA, Octo, RT-1/2, pi0, SmolVLA, ACT, LIBERO, SIMPLER |
| `ros2_robotics` | ROS 2, Gazebo, Nav2, SLAM, TF, rosbag |
| `px4_uav` | PX4 SITL, MAVLink, uXRCE-DDS, offboard |
| `multi_robot` | MARL, MAPPO, IPPO, coordination |
| `learning_robotics` | PPO, SAC, TD3, imitation learning |
| `hybrid_ai_control` | Learned + classical mixed architecture |

<!-- END ARIS-ENGINEERING-ROBOTICS -->

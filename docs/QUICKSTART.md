# Quick Start

Three worked examples for ARIS Engineering Robotics.

---

## Example A — MPC UAV Interception (classical_control + px4_uav)

**Research question**: Does an IMM-enhanced MPC controller reduce tracking error
compared to a PID baseline during maneuver-transition interception scenarios?

### Step 1 — Install skills

**Linux / macOS / WSL:**
```bash
# For Google Antigravity
bash tools/install_skills.sh --platform antigravity --project ~/my_project

# For OpenAI Codex CLI
bash tools/install_skills.sh --platform codex --project ~/my_project

# For Claude Code
bash tools/install_skills.sh --platform claude --project ~/my_project
```

**Windows (PowerShell / Python):**
```powershell
# PowerShell
powershell -ExecutionPolicy Bypass -File tools\install_skills.ps1 -Platform antigravity -Project C:\path\to\my_project

# Python (works on CMD, PowerShell, or Git Bash)
python tools\install_skills.py --platform antigravity --project C:\path\to\my_project
```

### Step 2 — Copy templates to your project

```bash
cp templates/EXPERIMENT.yaml      ~/my_project/
cp templates/EVIDENCE_LEDGER.yaml ~/my_project/
cp templates/CLAIM_MAP.yaml       ~/my_project/
cp templates/RESEARCH_CONTRACT.md ~/my_project/
```

### Step 3 — Open Codex in your project and run the pipeline

```
Use the robotics-research-router skill.
```

Expected output: profiles `classical_control`, `px4_uav` detected.

```
Use the robotics-experiment-plan skill to design an MPC robustness experiment for UAV interception.
```

Expected output: Q1–Q5 experiment matrix; MUST_RUN experiments mapped to claims C001–C003.

### Step 4 — Fill in EXPERIMENT.yaml

Edit the generated `EXPERIMENT.yaml`:
- Set `platform.autopilot: px4`
- Set `platform.simulator: gazebo`
- Set `scenario.repetitions: 20`
- Set `scenario.seed_policy: explicit`

### Step 5 — Run and monitor

```
Use the run-robotics-experiment skill.
```

```
Use the robotics-watchdog skill.
```

### Step 6 — Analyse and validate

```
Use the robotics-result-analysis skill.
Use the robotics-experiment-audit skill.
Use the sil-hil-validation skill.
Use the robotics-result-to-claim skill.
```

### Step 7 — Write paper

```
Use the engineering-paper-auditor skill.
Use the engineering-writing skill.
```

---

## Example B — ROS 2 + PX4 UAV Landing on Moving UGV (ros2_robotics + px4_uav)

**Research question**: Can a vision-guided PX4 UAV land precisely on a moving UGV
using a ROS 2 visual servoing controller?

### Key experiment design notes

- Profile: `ros2_robotics` + `px4_uav`
- Evidence target: L3 (PX4 SITL + Gazebo) before requesting L5 lab tests
- Key metrics: terminal landing error (m), mission success rate, computation time

### Workflow

```
1. robotics-research-router   → ros2_robotics + px4_uav profiles
2. robotics-experiment-plan   → Q1 (landing accuracy), Q2 (UGV speed sensitivity), Q5 (computation)
3. run-robotics-experiment    → PX4 SITL + Gazebo + ROS 2 launch
4. robotics-watchdog          → monitor PX4 heartbeat, TF, visual servo topic
5. robotics-result-analysis   → terminal_error, success_rate
6. simulation-validation      → confirm shared UGV velocity seeds
7. robotics-experiment-audit
8. sil-hil-validation         → assign L3
9. robotics-result-to-claim
10. engineering-writing
```

### Hardware gate

Physical lab test on real UAV/UGV requires explicit human approval.
The pipeline will stop at `HARDWARE_GATE` and output the manual step.

---

## Example C — MAPPO Multi-UAV Defense (learning_robotics + multi_robot)

**Research question**: Does MAPPO achieve higher interception success than IPPO
in a 3v3 cooperative UAV defense scenario?

### Key experiment design notes

- Profile: `learning_robotics` + `multi_robot`
- Evidence target: L2 (physics simulation)
- ARIS `run-experiment` handles training; `robotics-result-analysis` evaluates policy
- Key metrics: team success rate, collision rate, policy inference time

### Workflow

```
1. robotics-research-router   → learning_robotics + multi_robot
2. research-lit               → MARL for robotics literature
3. novelty-check
4. robotics-experiment-plan   → Q1 (success rate), Q3 (component: communication), Q5 (inference time)
5. ARIS run-experiment        → MAPPO vs IPPO training (GPU if available)
6. robotics-result-analysis   → success_rate, collision_rate, inference_time_ms
7. ablation-planner           → communication range ablation
8. robotics-experiment-audit
9. robotics-result-to-claim   → evidence L2; "indicates" language
10. engineering-paper-auditor
11. engineering-writing
```

### Note on GPU

If GPU is not available locally, use ARIS `vast-gpu` or `serverless-modal`
skills for training, then download results and continue with the robotics
analysis pipeline locally.

---

## Common Commands Reference

| Action | Command |
|---|---|
| Install (Codex, user-wide) | `bash tools/install_skills.sh --platform codex` |
| Install (Codex, project) | `bash tools/install_skills.sh --platform codex --project /path` |
| Install (Claude) | `bash tools/install_skills.sh --platform claude` |
| Dry run | `bash tools/install_skills.sh --platform codex --dry-run` |
| Validate install | `python tools/validate_installation.py` |
| Validate evidence | `python tools/validate_evidence_ledger.py EVIDENCE_LEDGER.yaml` |
| Validate result record | `python tools/validate_result_record.py RESULT_SUMMARY.yaml` |
| Uninstall | `bash tools/uninstall_skills.sh` |
| Sync upstreams | `bash tools/sync_upstreams.sh` |
| Run tests | `python -m pytest tests/ -v` |

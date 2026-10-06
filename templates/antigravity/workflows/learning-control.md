# Workflow: Learning-Based & AI Control

**Purpose**: Guide deep reinforcement learning, imitation learning, and AI-based robotics control research from formulation to statistical multi-seed benchmarking and sim-to-real transfer.

**Invoke with**: A learning control topic, e.g.:
```
/learning-control "Train and evaluate SAC-Lagrangian quadruped locomotion with domain randomization"
```
or natural language:
```
Use the learning-control workflow for my reinforcement learning manipulator.
```

---

## Stage 1 — Problem Formulation & Algorithm Selection

**Skills**: `robotics-research-router`, ARIS `research-lit`
- Select algorithm: PPO, SAC, TD3, DreamerV3, IQL, DAgger, RMA, or Neural MPC.
- Select simulation environment: Isaac Lab, Isaac Gym, MuJoCo, ManiSkill, or PyBullet.
- Define state space, action space, reward structure, and constraint limits.

## Stage 2 — Experiment Design with Multi-Seed Protocol

**Skill**: `robotics-experiment-plan`
- Enforce $\ge 10$ evaluation seeds for simulation, $\ge 5$ seeds for hardware.
- Define domain randomization parameter distributions (mass, friction, damping, delay).
- Generate `LEARNING_EXPERIMENT.yaml`.

## Stage 3 — Execution & Training Monitoring

**Skills**: `run-robotics-experiment`, `robotics-watchdog`
- Run training rollouts and evaluation checkpoints.
- Monitor for training instability, catastrophic forgetting, reward hacking, and actuator chatter.

## Stage 4 — Statistical Aggregate Analysis (rliable)

**Skill**: `learning-control-eval`
- Compute Interquartile Mean (IQM) across all seeds.
- Compute 95% stratified bootstrap confidence intervals.
- Generate Dolan-Moré performance profile curves.
- Quantify sim-to-real performance degradation $\Delta_{\text{gap}}\%$.

## Stage 5 — SOTA Safety Shielding (if applicable)

**Skill**: `safety-filter-cbf`
- Verify that CBF safety filter prevents state and obstacle constraint violations ($h(x) \ge 0$).
- Measure filter intervention rate (% of steps nominal policy was altered).

## Stage 6 — Result Audit & Evidence Governance

**Skills**: `robotics-experiment-audit` → `robotics-result-to-claim`
- Verify no single-seed cherry-picking occurred.
- Confirm baseline fairness (identical seeds, disturbances, and evaluation budgets).
- Append verified metrics to `EVIDENCE_LEDGER.yaml` and update `CLAIM_MAP.yaml`.

---

## Output

Produce:
1. `LEARNING_EXPERIMENT.yaml` configuration.
2. Statistical evaluation report with IQM and 95% bootstrap CIs.
3. Updated `EVIDENCE_LEDGER.yaml` and `CLAIM_MAP.yaml`.

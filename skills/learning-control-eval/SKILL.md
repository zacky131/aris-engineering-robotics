---
name: learning-control-eval
description: >
  Evaluate and benchmark learning-based robotics policies and deep reinforcement learning
  controllers (PPO, SAC, TD3, Dreamer, DAgger, RMA). Computes multi-seed statistical
  aggregates (IQM, 95% bootstrap CIs), Dolan-Moré performance profiles, sim-to-real
  transfer degradation, and domain randomization robustness.
platforms:
  - codex
  - claude
  - antigravity
---

# Skill: learning-control-eval

## Purpose

Enforce rigorous scientific evaluation of learning-based control and reinforcement learning policies, preventing single-seed cherry-picking and unsubstantiated generalization claims.

---

## Instructions

### Step 1 — Verify Multi-Seed Protocol

Confirm that evaluations fulfill minimum seed requirements:
- Simulation environments: **$\ge 10$ independent random seeds**.
- Complex physics / Real robot: **$\ge 5$ independent evaluation seeds**.

Reject any single-seed result table as scientifically inconclusive.

### Step 2 — Compute Statistical Metrics (rliable standard)

Rather than raw sample mean (susceptible to outliers):
1. **Interquartile Mean (IQM)**:
   Discard the bottom 25% and top 25% of scores across seeds and calculate the mean of the remaining middle 50%.
2. **Stratified Bootstrap Confidence Intervals**:
   Compute 95% bootstrap confidence intervals using 2000+ resamples.
3. **Performance Profiles**:
   Plot the cumulative probability of achieving normalized score $\tau \in [0, 1]$ across all tasks and runs:
   $$P(\text{score} \ge \tau)$$

### Step 3 — Sim-to-Real Transfer Evaluation

When evaluating policies across simulation and hardware:
1. **Transfer Degradation**:
   $$\Delta_{\text{gap}} = \frac{\text{Success}_{\text{sim}} - \text{Success}_{\text{real}}}{\text{Success}_{\text{sim}}} \times 100\%$$
2. **Domain Randomization Sensitivity**:
   Evaluate policies under stress-tested physical parameter extremes (mass $\pm 20\%$, friction $\mu \in [0.1, 1.5]$, actuator latency $\tau \in [0, 30]\text{ ms}$).
3. **Tracking & Smoothness Metrics**:
   - Tracking RMSE against target reference.
   - Mean absolute jerk $\|\dddot{q}\|$ and energy/effort expenditure $\int \|u(t)\|^2 dt$.

### Step 4 — Detect Failure Modes & Reward Exploitation

Audit logs for:
- **Actuator Chattering**: High-frequency control reversals indicating unnatural reward exploitation.
- **Distribution Shift**: State visitation expanding beyond training replay buffer boundaries.
- **Constraint Violations**: Torques, velocities, or joint limits exceeding robot safety boundaries.

### Step 5 — Output Report

```yaml
learning_evaluation_summary:
  algorithm: "SAC-Lagrangian"
  environment: "Franka-Impedance-Wiping"
  seeds_evaluated: 10
  sample_efficiency_steps_to_threshold: 4.5e5
  metrics:
    iqm_normalized_score: 0.89
    ci_95_low: 0.84
    ci_95_high: 0.92
    sim_to_real_success_drop_pct: 7.2
    mean_jerk_rad_s3: 14.2
  domain_randomization_robustness:
    friction_variation_pass_rate: 0.91
    mass_variation_pass_rate: 0.88
    latency_variation_pass_rate: 0.84
  verdict: "STATISTICALLY_VALID"
```

---

## Constraints

- Never average cherry-picked runs.
- Distinguish between simulated randomized performance and un-randomized nominal performance.

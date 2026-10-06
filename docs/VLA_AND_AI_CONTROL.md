# Vision-Language-Action (VLA), Learning-Based, and AI/SOTA Control Guide

## Overview

`aris-engineering-robotics` extends classic automated robotics research to encompass modern **Embodied AI**, **Learning-Based Control**, and **Physics-Informed AI / SOTA Safety Filters**.

This guide outlines the specialized paradigms, profiles, standards, and end-to-end evaluation workflows supported by the repository.

---

## 1. Supported Paradigms & Profiles

| Profile | Key Indicator Keywords | Primary Skills | Evaluation Artefacts |
|---|---|---|---|
| **`vla_robotics`** | OpenVLA, Octo, RT-1, RT-2, π0, SmolVLA, ACT, Diffusion Policy, LIBERO, SIMPLER Env, ManiSkill, CALVIN | `vla-robotics`<br>`safety-filter-cbf`<br>`robotics-watchdog` | `VLA_EVALUATION.yaml`<br>`schemas/vla-evaluation.schema.json` |
| **`learning_control`** | PPO, SAC, TD3, Offline RL (CQL/IQL), Sim-to-Real, Domain Randomization, RMA, Privileged Teacher | `learning-control-eval`<br>`run-robotics-experiment`<br>`robotics-result-analysis` | `LEARNING_EXPERIMENT.yaml`<br>`schemas/learning-control.schema.json` |
| **`ai_control`** | Neural ODE, PINN, Physics-Informed, Neural MPC, GP-MPC, Deep Koopman, Residual RL | `controller-tuning`<br>`simulation-validation`<br>`robotics-watchdog` | `EXPERIMENT.yaml` (domain: `ai_control`) |
| **`safe_sota_control`** | Control Barrier Function (CBF), CLF-CBF, QP Safety Shield, Forward Invariance, Safety Certificate | `safety-filter-cbf`<br>`robotics-watchdog` | Safety violation audit logs, QP feasibility ratios |

---

## 2. Vision-Language-Action (VLA) in Robotics

### Architecture & Frequency Decoupling
VLA policies process multi-modal tokens (high-resolution camera feeds and text instructions) which typically execute at **3–10 Hz**, whereas robotic low-level joint/torque controllers require **100–500 Hz**.

1. **High-Level Asynchronous VLA Loop (5–10 Hz)**:
   - Receives RGB images (wrist + static over-the-shoulder views) and natural language goals.
   - Generates action chunks (horizon $H \in [8, 64]$) in Tool Frame Cartesian delta $(\Delta x, \Delta y, \Delta z, \Delta \text{roll}, \Delta \text{pitch}, \Delta \text{yaw}, \text{gripper})$.
2. **Action Interpolation & Low-Level Tracking (100–500 Hz)**:
   - Applies temporal ensembling over overlapping predicted action chunks:
     $$a_t = \frac{\sum_{i=1}^K w_i \hat{a}_{t|t-i}}{\sum_{i=1}^K w_i}, \quad w_i = \exp(-m \cdot i)$$
   - Low-level Cartesian impedance or Operational Space Control (OSC) tracks the trajectory.
3. **Safety Cage & Guard**:
   - Hard workspace bounding box: $[x_{\min}, x_{\max}] \times [y_{\min}, y_{\max}] \times [z_{\min}, z_{\max}]$.
   - Per-step delta clipping: $\|\Delta p\| \le \Delta_{\max}$.
   - Emergency fallback gate on OOD detection or camera stream freeze.

### Standard Benchmarks
- **SIMPLER Env**: Evaluates Google Robot and WidowX policies with visual/physical digital twins.
- **LIBERO**: 130+ manipulation tasks partitioned into `LIBERO-Spatial`, `LIBERO-Object`, `LIBERO-Goal`, `LIBERO-100`.
- **ManiSkill / CALVIN**: Complex articulated and multi-turn sequential language manipulation.

---

## 3. Learning-Based Control & Sim-to-Real

### Multi-Seed & Statistical Integrity (Agarwal et al. 2021)
Single-run or single-seed evaluations are prohibited. The repository enforces:
- **$\ge 10$ Independent Evaluation Seeds** for model-free RL; $\ge 5$ seeds for heavy visual training.
- **Interquartile Mean (IQM)** instead of raw mean to eliminate outlier bias.
- **Stratified Bootstrap Confidence Intervals (95% CI)** with 2,000 bootstrap resamples.
- **Performance Profiles**: Cumulative distribution functions of normalized scores against baselines.

### Sim-to-Real Protocol
- Explicit specification of domain randomization ranges (friction, payload mass, link inertia, center of mass, actuator delay, sensor noise).
- Two-stage RMA (Rapid Motor Adaptation) validation: privileged teacher policy vs. student adaptation network.
- Hardware transfer metrics: Success rate degradation $\le 15\%$, zero catastrophic safety interlock trips.

---

## 4. Physics-Informed AI Control & Neural MPC

### Hybrid & Physics-Preserving Models
- **PINNs & Neural ODEs**: Enforce Hamiltonian or Lagrangian conservation laws:
  $$\dot{x} = f_{\text{known}}(x, u) + g_{\theta}(x, u)$$
- **Residual RL**: Classical base controller (LQR/feedback linearization) provides nominal stability while a neural policy learns unmodeled nonlinear aerodynamic/friction residuals.

### Real-Time Latency Budgets
- In Neural MPC and learned dynamics loops, 99th percentile inference time ($P99$) must strictly remain below the sampling period:
  $$T_{\text{infer}}^{P99} < T_s$$
- A deterministic fallback controller (e.g., standard PID / passivity control) is automatically triggered if neural evaluation exceeds budget.

---

## 5. Control Barrier Functions (CBF) & QP Safety Shields

### Mathematical Formulation
Given safe set $\mathcal{C} = \{x : h(x) \ge 0\}$, a continuously differentiable barrier function $h(x)$ ensures forward invariance via the condition:
$$\dot{h}(x, u) \ge -\alpha(h(x)), \quad \alpha \in \mathcal{K}_{\infty}$$

The safety filter solves a quadratic program (QP) in real time:
$$\min_{u} \frac{1}{2} \|u - u_{\text{nominal}}\|^2$$
$$\text{subject to } L_f h(x) + L_g h(x) u + \alpha(h(x)) \ge 0$$
$$u_{\min} \le u \le u_{\max}$$

Where $u_{\text{nominal}}$ is supplied by the VLA model, Deep RL policy, or human operator.

### Feasibility & Solver Fallbacks
- Embedded QP solvers supported: `OSQP`, `qpOASES`, `Clarabel`.
- Soft relaxation slack variables $\epsilon \ge 0$ with high penalty $M \gg 1$:
  $$\min_{u, \epsilon} \frac{1}{2} \|u - u_{\text{nominal}}\|^2 + M \epsilon^2$$
- If the QP fails or times out, the watchdog intervenes with a safe braking or passive hold control.

---

## 6. End-to-End Workflow Examples

### Antigravity Workflow
To execute a VLA benchmark evaluation inside Antigravity IDE:
```markdown
/workflow vla-robotics
```
Or execute a reinforcement learning multi-seed campaign:
```markdown
/workflow learning-control
```

### CLI / Agent Workflow (Claude Code & Codex)
1. **Intake & Route**:
   ```
   "Route research for OpenVLA fine-tuning on Franka Panda in LIBERO"
   -> Matches profile: vla_robotics
   ```
2. **Plan**:
   ```
   "Create an evaluation plan using templates/VLA_EVALUATION.yaml"
   -> Invokes robotics-experiment-plan
   ```
3. **Execute & Shield**:
   ```
   "Execute VLA test suite with CBF safety filter"
   -> Invokes vla-robotics, safety-filter-cbf, robotics-watchdog
   ```
4. **Statistical Analysis**:
   ```
   "Analyze evaluation runs across seeds and benchmark splits"
   -> Invokes robotics-result-analysis (IQM, bootstrap CI, subtask progression)
   ```
5. **Claims & Paper Drafting**:
   ```
   "Map validated empirical metrics to paper claims and draft section"
   -> Invokes robotics-result-to-claim, engineering-writing
   ```

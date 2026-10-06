# Shared Rule: SOTA Safety-Critical Control & Barrier Certificates

## 1. Scope & Purpose

This document governs research utilizing **Control Barrier Functions (CBFs)**, **Control Lyapunov Functions (CLFs)**, and **Quadratic Programming (QP) Safety Shields** for robotic systems, particularly when filtering actions from unconstrained neural policies (RL, VLA, imitation learning).

---

## 2. Safety Filter Formulation

Given an unconstrained or learned nominal action $u_{\text{nom}}$ (from a DRL policy or VLA model) and a safe set defined by the zero-superlevel set of a continuously differentiable barrier function $h(x)$:
$$\mathcal{C} = \{x \in \mathcal{X} \mid h(x) \ge 0\}$$

The safety filter projects $u_{\text{nom}}$ into the admissible safe control set by solving the real-time Quadratic Program:

$$\min_{u \in \mathcal{U}} \frac{1}{2} \|u - u_{\text{nom}}\|^2 + \frac{\gamma}{2} \delta^2$$
$$\text{subject to } \dot{h}(x, u) \ge -\alpha(h(x)) - \delta$$

where:
- $\dot{h}(x, u) = \nabla h(x) \cdot f(x) + \nabla h(x) \cdot g(x) u$ for affine dynamics $\dot{x} = f(x) + g(x)u$.
- $\alpha(\cdot)$ is an extended class-$\mathcal{K}$ function (commonly linear: $\alpha(h) = \alpha_0 h$).
- $\delta \ge 0$ is a soft slack variable permitted only if hard constraint feasibility guarantees cannot be proven analytically.

---

## 3. Mandatory Reporting for Safety-Shielded Research

1. **Zero-Violation Invariant**:
   - For all simulated and physical trials within the validated safe set $\mathcal{C}$, the safety violation count must be **identically zero**:
     $$\min_{t} h(x(t)) \ge 0$$
2. **Intervention Rate**:
   - Report the percentage of timesteps where the safety shield actively modified the nominal policy:
     $$\text{Intervention Rate} = \frac{1}{T} \sum_{t=1}^T \mathbb{I}(\|u(t) - u_{\text{nom}}(t)\| > \epsilon) \times 100\%$$
3. **Solver Performance & Infeasibility Protocol**:
   - Report solver time percentiles (p50, p95, max) using fast QP solvers (e.g., OSQP, qpOASES, ProxQP).
   - Infeasibility Handler: If the QP is infeasible (e.g., due to model mismatch or out-of-bounds disturbance), specify the failsafe action (e.g., maximum braking torque, emergency hover, or zero-velocity command).

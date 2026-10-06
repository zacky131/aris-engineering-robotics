---
name: safety-filter-cbf
description: >
  Formulate, verify, and benchmark Control Barrier Function (CBF) safety filters
  and Quadratic Programming (QP) safety shields. Projects unconstrained actions
  from deep RL, VLA foundation models, or neural policies onto certified safe sets
  with formal forward-invariance guarantees.
platforms:
  - codex
  - claude
  - antigravity
---

# Skill: safety-filter-cbf

## Purpose

Provide certified safety guarantees for robotics control systems by designing and auditing **Control Barrier Functions (CBFs)** and real-time **QP Safety Shields**.

The safety filter sits between the high-level policy (e.g., VLA model, RL policy, or trajectory planner) and the low-level actuator layer, modifying control commands only when necessary to prevent safety violations:

$$\min_{u \in \mathcal{U}} \frac{1}{2} \|u - u_{\text{nominal}}\|^2 \quad \text{s.t.} \quad L_f h(x) + L_g h(x) u \ge -\alpha(h(x))$$

---

## Instructions

### Step 1 — Define Safe Set & Barrier Function Candidates

1. Specify the system state $x \in \mathbb{R}^n$, control input $u \in \mathcal{U}$, and control-affine dynamics $\dot{x} = f(x) + g(x)u$.
2. Formulate the zero-superlevel safe set $\mathcal{C} = \{x \in \mathbb{R}^n \mid h(x) \ge 0\}$.
   Common robotics barrier formulations:
   - **Collision Avoidance**: $h_{\text{obs}}(p) = \|p - p_{\text{obs}}\|^2 - r_{\text{safe}}^2 \ge 0$.
   - **Workspace Envelope**: $h_{\text{cage}}(p) = d_{\max}^2 - \|p - p_{\text{center}}\|^2 \ge 0$.
   - **Velocity / Attitude Limit**: $h_{\text{tilt}}(R) = \cos(\theta_{\max}) - e_3^T R e_3 \ge 0$.
   - **Control Barrier with High Relative Degree**: Formulate High-Order CBF (HOCBF) if relative degree $r \ge 2$.

### Step 2 — Construct Real-Time QP Safety Filter

Formulate the QP optimization problem:
$$\min_{u \in \mathcal{U}, \delta \ge 0} \frac{1}{2} \|u - u_{\text{nominal}}\|^2 + \frac{\gamma}{2} \delta^2$$
$$\text{s.t.} \quad \nabla h(x)^T (f(x) + g(x)u) \ge -\alpha_0 h(x) - \delta$$
$$u_{\min} \le u \le u_{\max}$$

Where $\delta$ is a soft slack variable used only when combining safety with performance objectives (e.g., CLF-CBF-QP) to prevent infeasibility. For pure hard safety constraints, $\delta \equiv 0$.

### Step 3 — Select & Configure Fast Solver

Choose a real-time embedded QP solver:
- **OSQP**: Operator Splitting QP solver (handles box constraints efficiently).
- **qpOASES**: Active-set solver with fast warm-starting across consecutive timesteps.
- **ProxQP**: State-of-the-art proximal method with exceptional numerical stability.

Verify solver execution time is bounded:
$$\text{Solve Time} \le 2.0\text{ ms} \quad (\text{for } 100\text{--}500\text{ Hz control loops})$$

### Step 4 — Audit Safety Shield Performance

Analyze rollout telemetry and evaluate:
1. **Safety Invariant**:
   $$\min_{t \in [0, T]} h(x(t)) \ge 0 \quad (\text{Must be exactly } 0 \text{ violations})$$
2. **Intervention Rate**:
   $$\text{Intervention Rate} = \frac{1}{T} \sum_{t=1}^T \mathbb{I}(\|u(t) - u_{\text{nominal}}(t)\| > \epsilon) \times 100\%$$
   - Low intervention ($< 5\%$): High-level policy naturally respects safety.
   - High intervention ($> 30\%$): High-level policy actively aggressive or unsafe; shield provides critical intervention.
3. **Infeasibility Handling**:
   Document the deterministic failsafe action if QP fails to find a feasible solution (e.g. emergency braking torque, hover, or impedance release).

### Step 5 — Output Report

```yaml
safety_filter_report:
  barrier_type: "HOCBF_relative_degree_2"
  safe_set_definition: "Obstacle standoff radius >= 0.25m and z >= 0.10m"
  qp_solver: "OSQP"
  trials_audited: 50
  results:
    violations: 0
    minimum_margin_h: 0.042
    mean_intervention_rate_pct: 12.4
    max_solver_time_ms: 1.45
    p95_solver_time_ms: 0.82
  failsafe_triggered_count: 0
  status: "VERIFIED_SAFE"
```

---

## Constraints

- Hard safety constraints must never permit safety violations.
- Infeasibility protocols must be documented and tested under adversarial corner cases.

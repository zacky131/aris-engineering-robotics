# Shared Rule: Learning-Based Control & DRL Standards

## 1. Scope & Purpose

This document governs research in **Reinforcement Learning (RL)**, **Imitation Learning (IL)**, and **Sim-to-Real Transfer** for robotic systems.

---

## 2. Statistical Significance Protocols

Single-seed evaluation is strictly prohibited in learning-based robotics. Due to high variance in policy optimization, researchers must follow the **rliable** statistical standard:

1. **Seed Count**:
   - Minimum **10 independent random seeds** for simulation benchmarks.
   - Minimum **5 independent seeds** for computationally intensive physics simulation or real-robot evaluations.
2. **Aggregated Performance Metrics**:
   - Report **Interquartile Mean (IQM)** rather than mean alone (IQM trims the top and bottom 25% of runs, mitigating outliers).
   - Report **95% Stratified Bootstrap Confidence Intervals (CIs)**.
   - Present **Performance Profiles** (fraction of runs achieving a normalized score $\tau$).
3. **Training Curve Transparency**:
   - Show shaded interquartile regions (25th to 75th percentiles) across seeds over timesteps.

---

## 3. Sim-to-Real Transfer & Domain Randomization Reporting

When evaluating policies trained in simulation for real-world deployment:

1. **Explicit Randomization Ranges**:
   Every randomized parameter must be documented in an explicit table:
   - Rigid body mass: $m \sim \mathcal{U}(0.85 m_0, 1.15 m_0)$
   - Link center of mass: $\Delta r \sim \mathcal{U}(-0.02, 0.02)\text{ m}$
   - Friction coefficient: $\mu \sim \mathcal{U}(0.2, 1.2)$
   - Actuator latency / communication delay: $\tau_{\text{delay}} \sim \mathcal{U}(0, 20)\text{ ms}$
   - Motor damping and armature inertia variations.
2. **Teacher-Student Privileged Distillation (RMA / Expressive Distillation)**:
   - Clearly document which privileged environment states (ground-truth friction, payload mass, external forces) are provided to the teacher policy.
   - Specify the adaptation module architecture (1D temporal CNN, Transformer, or MLP) and the historical proprioceptive buffer size $T_{\text{hist}}$.
3. **Sim-to-Real Degradation Quantification**:
   - Report the Sim-to-Real gap explicitly:
     $$\Delta_{\text{transfer}} = \frac{\text{Metric}_{\text{real}} - \text{Metric}_{\text{sim}}}{\text{Metric}_{\text{sim}}} \times 100\%$$

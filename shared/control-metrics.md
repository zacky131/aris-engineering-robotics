# Control Metrics Reference

Metrics specific to classical and modern control theory research.

---

## Stability

| Claim | Required evidence |
|---|---|
| Lyapunov stability | Analytical proof; L0 |
| Asymptotic stability | Proof + bounded trajectories in simulation |
| Input-to-state stability (ISS) | Analytical ISS bound |
| BIBO stability | Analytical bound |
| Closed-loop poles in LHP | Eigenvalue analysis |
| Empirical stability (not provable) | No divergence across N trials; state bounded |

Never claim "stable" from a single simulation run.

---

## Transient Performance (Step Response)

| Metric | Symbol | Unit |
|---|---|---|
| Rise time (10%–90%) | t_r | s |
| Peak time | t_p | s |
| Overshoot | MP | % |
| Settling time (2% band) | t_s | s |
| Steady-state error | e_ss | (variable unit) |

Report for each significant input type (step, ramp, sinusoidal).

---

## Frequency Domain

| Metric | Symbol | Unit |
|---|---|---|
| Gain margin | GM | dB |
| Phase margin | PM | deg |
| Bandwidth (−3 dB) | ω_BW | rad/s |
| Crossover frequency | ω_c | rad/s |
| Sensitivity peak (H∞) | ‖S‖_∞ | — |

---

## MPC / NMPC Specific

| Metric | Symbol | Notes |
|---|---|---|
| Prediction horizon | N | control steps |
| Control horizon | Nc | ≤ N |
| Constraint satisfaction rate | — | fraction of steps with all constraints met |
| Terminal constraint active | — | indicates feasibility near boundary |
| Warm-start convergence | Ī_sol | mean solver iterations |
| Infeasibility events | N_inf | count of solver failures |
| Computation time (see timing) | — | |

---

## Disturbance Rejection

| Test type | How to report |
|---|---|
| Step disturbance | RMSE and settling time after disturbance onset |
| Sinusoidal disturbance | Attenuation at each frequency (dB or ratio) |
| Wind disturbance (UAV) | RMSE vs wind speed at each tested level |
| Model uncertainty | Metric vs uncertainty level ε |

Always report the tested disturbance magnitude range explicitly.

---

## Constraint Handling

| Report | Description |
|---|---|
| Hard constraints | Binary: violated or not (any violation is a failure) |
| Soft constraints | Violation magnitude and frequency |
| Actuator limits | Fraction of time at saturation per actuator |
| State constraints | Min clearance, worst-case violation |

---

## Observer / Estimator Quality

See `robotics-metrics.md` for RMSE, NIS, NEES.

Additional:
- Innovation whiteness test (autocorrelation at lag > 0 should be near zero)
- Filter divergence detection (covariance unbounded)
- Mode probability evolution (IMM-specific)

---

## Reporting Requirements

- Always report which operating condition each metric was measured in.
- Always report whether the controller was in steady-state or transient regime.
- For repeated trials, report mean ± std and N.
- Do not use single-run values to support robustness claims.

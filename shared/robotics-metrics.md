# Robotics Metrics Reference

Standard metrics for robotics research across all sub-domains.

---

## Tracking / Path Following

| Metric | Symbol | Unit | Notes |
|---|---|---|---|
| Position RMSE | RMSE_p | m | √(mean(‖p_ref − p‖²)) |
| Position MAE | MAE_p | m | |
| Position max error | e_max | m | |
| Terminal position error | e_T | m | Error at mission end |
| Lateral tracking error | e_lat | m | For path-following |
| Heading error | e_ψ | deg | |
| Velocity tracking RMSE | RMSE_v | m/s | |
| Relative position error | ‖Δp‖ | m | For pursuit/interception |
| Relative velocity error | ‖Δv‖ | m/s | For pursuit/interception |

---

## Control Effort / Input

| Metric | Symbol | Unit | Notes |
|---|---|---|---|
| Total control effort | J_u | — | Σ‖u(t)‖² Δt |
| Input smoothness (jerk proxy) | J_Δu | — | Σ‖Δu(t)‖² Δt |
| Actuator saturation fraction | f_sat | — | Fraction of time at limits |
| Constraint violation count | N_viol | count | Hard constraint breaches |

---

## Transient Response

| Metric | Symbol | Unit |
|---|---|---|
| Rise time | t_r | s |
| Settling time (2%) | t_s | s |
| Overshoot | OS | % |
| Steady-state error | e_ss | (unit of variable) |
| Undershoot | US | % |

---

## Estimation Performance

| Metric | Symbol | Unit | Notes |
|---|---|---|---|
| Position RMSE (estimated vs truth) | RMSE_p̂ | m | |
| Velocity RMSE (estimated vs truth) | RMSE_v̂ | m/s | |
| Orientation error | e_q | deg | Quaternion angle difference |
| Normalized Innovation Squared | NIS | — | χ² consistency; should follow χ² distribution |
| Normalized Estimation Error Squared | NEES | — | χ² consistency |

---

## Planning / Navigation

| Metric | Symbol | Unit |
|---|---|---|
| Path length | L_path | m |
| Planning time | t_plan | ms |
| Minimum obstacle clearance | d_min | m |
| Replanning rate | f_replan | Hz |
| Coverage fraction | η_cov | — |

---

## Mission-Level

| Metric | Symbol | Unit | Notes |
|---|---|---|---|
| Success rate | P_suc | — | Fraction of trials meeting criterion |
| Collision rate | P_col | — | Fraction with collision |
| Mission completion time | T_mission | s | Mean over successful trials |
| Mission timeout rate | P_timeout | — | |
| Energy consumption | E | J | Estimated from motor currents |

---

## Real-Time / Timing

| Metric | Symbol | Unit |
|---|---|---|
| Mean computation time | t̄_comp | ms |
| Median computation time | t̃_comp | ms |
| 95th percentile computation time | t_p95 | ms |
| 99th percentile computation time | t_p99 | ms |
| Maximum computation time | t_max | ms |
| Deadline miss rate | f_miss | — |
| Solver iterations (mean) | Ī_sol | count |
| Real-time factor | RTF | — |

---

## Robustness / Sensitivity

| Metric | Definition |
|---|---|
| Noise sensitivity | Metric degradation as a function of noise variance σ² |
| Delay sensitivity | Metric degradation vs. communication delay τ |
| Dropout sensitivity | Metric degradation vs. packet loss rate |
| Model mismatch sensitivity | Metric degradation vs. plant model error |
| Wind sensitivity (UAV) | Metric degradation vs. wind speed |
| Initial condition sensitivity | Metric variance across sampled initial conditions |

For robustness metrics, always report:
- The tested range of the perturbation parameter
- The metric value at each level
- Whether the method remains feasible (constraint violations)

---

## Reporting Requirements

- Always state N (number of trials) for any aggregate statistic.
- For N ≥ 5, report mean ± std or confidence interval.
- For N ≥ 10, consider Wilcoxon or t-test if comparing two methods.
- Always state the random seed policy used.
- Do not claim statistical significance without a justified test.

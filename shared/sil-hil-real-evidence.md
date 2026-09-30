# SIL / HIL / Real Evidence Boundary

Defines which claims are permitted at each evidence level.

---

## Evidence Level Summary

| Level | Environment | Platform | Permitted claim scope |
|---|---|---|---|
| L0 | Mathematical | — | Theoretical properties only (stability, convergence, bounds) |
| L1 | ODE/numerical | Simulated model | Numerical feasibility, algorithmic correctness |
| L2 | Physics engine | Simulated robot, physics | Simulation performance under evaluated conditions |
| L3 | SITL | Real code, simulated plant | Code integration correctness; SIL performance |
| L4 | HIL | Real hardware + simulated plant | Hardware timing, integration on target MCU |
| L5 | Physical lab | Real robot, controlled environment | Controlled physical performance |
| L6 | Field | Real robot, operational | Operational performance |

---

## Mapping claim phrases to required levels

| Claim phrase | Minimum required level |
|---|---|
| "In simulation, the method indicates..." | L2 |
| "Real-time constraint satisfied" | L3 (SIL) or L4 (HIL) on target hardware |
| "Hardware validated" | L4 or L5 |
| "Physically demonstrated" | L5 |
| "Robust to real-world disturbances" | L5 or L6 |
| "Operationally deployed" | L6 |
| "Generalizes across environments" | L5 or L6 across diverse environments |

---

## Prohibited claim escalations

| What was done | What is forbidden |
|---|---|
| Gazebo simulation only | "hardware tested", "physically validated" |
| PX4 SITL | "flight tested", "real UAV demonstrated" |
| One lab flight | "field operational", "industry ready" |
| Controlled indoor flight | "outdoor robustness" |
| Single disturbance level | "fully robust to disturbances" |

---

## Boundary statement convention

Every paper using simulation evidence must include a boundary statement:

> "Experiments were conducted in Gazebo simulation (L2 / L3 SITL). Conclusions
> are therefore bounded to the evaluated simulation conditions. Physical
> validation (L5) is reserved for future work."

---

## Claim revision examples

| Original (inflated) | Revised (calibrated) |
|---|---|
| "The method is real-world robust" | "Simulation results indicate robustness to modelled wind disturbances up to 2 m/s" |
| "The system was validated on a real UAV" | "The system was tested in PX4 SITL (L3)" |
| "The controller generalizes to diverse scenarios" | "The controller was evaluated on two scenario types in simulation" |

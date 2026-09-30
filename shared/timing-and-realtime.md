# Timing and Real-Time — Global Rule

## Real-time claims require real-time evidence

To claim a controller "meets real-time requirements":
- The computation time must have been measured during a real execution run
- The p99 computation time must be below the control period
- The measurement must have been taken on representative hardware

Claiming real-time from theory alone is not sufficient for a computational claim.

## Required timing metrics

For any controller with a real-time requirement:
- Report: mean, median, p95, p99, max computation time
- Report: control period (target)
- Report: deadline miss rate
- Report: hardware platform where timing was measured

## SIL vs HIL vs real hardware

| Platform | Timing interpretation |
|---|---|
| SIL (SITL) | Indicates code efficiency; not binding for real hardware |
| HIL | More representative; still not identical to production hardware |
| Real embedded MCU | Valid for real-time constraint claim |

Do not assert "meets real-time constraint" from SIL results alone unless the
paper explicitly scopes the claim to SIL context.

## Scheduling model

Document the scheduling model:
- Fixed-rate timer?
- Event-triggered?
- OS priority (POSIX RT, etc.)?

Results from non-real-time OS (standard Linux) should note this limitation.

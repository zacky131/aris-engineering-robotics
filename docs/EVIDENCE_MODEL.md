# Evidence Model

## Overview

ARIS Engineering Robotics enforces a strict evidence model to ensure
that all claims in research papers are accurately calibrated to the
evidence actually produced.

## Evidence Levels (L0–L6)

| Level | Type | Description |
|---|---|---|
| L0 | Theoretical | Mathematical proof, stability analysis |
| L1 | Numerical simulation | ODE solver, no physics engine |
| L2 | Physics simulation | Gazebo, Isaac, PyBullet |
| L3 | Software-in-the-loop | Real code, simulated plant (SITL) |
| L4 | Hardware-in-the-loop | Real hardware components |
| L5 | Controlled physical experiment | Real robot, controlled environment |
| L6 | Field / operational | Real robot, operational environment |

## Claim calibration

Claims must not exceed the evidence level produced.

See `shared/sil-hil-real-evidence.md` for claim phrase ↔ level mapping.
See `shared/claim-strength.md` for permitted verb ladder.

## Evidence Ledger

`EVIDENCE_LEDGER.yaml` links every evidence record to:
- A result file on disk
- An experiment ID
- A set of metrics with actual values
- A `verified: true/false` flag

Only run `validate_evidence_ledger.py` to set `verified: true`.

## Claim Map

`CLAIM_MAP.yaml` links every manuscript claim to:
- One or more evidence records
- The evidence level
- Permitted language
- Prohibited extensions
- Missing evidence needed

# Claim Strength — Global Rule

## Permitted claim ladder (ascending strength)

Use the weakest verb that is accurate for the evidence available.

```
is consistent with
  └─ requires only: result does not contradict mechanism
suggests
  └─ requires: pattern present in ≥ 1 trial or condition
indicates
  └─ requires: consistent pattern across trials or conditions
supports
  └─ requires: consistent across multiple conditions or baselines
shows
  └─ requires: clear quantitative difference with statistics
demonstrates
  └─ requires: repeated, controlled experiment with full reporting
confirms
  └─ requires: independent replication or cross-validation
```

## Evidence level modifiers

| Evidence level | Maximum claim strength |
|---|---|
| L1 (numerical simulation) | suggests, indicates |
| L2 (physics simulation) | indicates, supports |
| L3 (SIL) | supports, demonstrates (in SIL context) |
| L4 (HIL) | demonstrates (HIL), supports hardware feasibility |
| L5 (controlled physical) | shows, demonstrates |
| L6 (field) | confirms, demonstrates operationally |

## Prohibited terms (without specific justification)

- `proves` — only valid for L0 mathematical/analytical results
- `guarantees` — only valid for formal verification
- `fully robust` — requires exhaustive testing across the claimed domain
- `generalizes` — requires out-of-distribution evaluation
- `state of the art` — requires comprehensive benchmark survey
- `real-world ready` — requires L5 or L6 evidence
- `industry ready` — requires L5/L6 plus reliability/safety validation
- `optimal` — requires proof of global optimality or exhaustive search

---

Source: adapted from `engineering-paper-skills/skills/_shared/claim-strength.md`
Extended with L0–L6 evidence level modifiers.

# Evidence Boundary — Global Invariant

This rule applies to all skills in ARIS Engineering Robotics.

## Hard prohibition

Never invent or fabricate:

- experiments
- trials
- result values
- metric numbers
- statistical significance or p-values
- mechanisms or causal explanations
- robustness claims
- sensors or platforms
- baselines
- deployment or field claims
- citations or references
- completed manuscript edits
- experimental conditions
- timing measurements
- constraint violations

## What "fabricate" means

A metric is fabricated if it is:
- not present in an actual result file on disk
- an estimate or projection not labelled as such
- a value carried over from a different experiment without explicit attribution

## Permitted language for uncertain or projected values

If a value is estimated or expected (not measured), say so:
- "we expect X based on Y"
- "preliminary results suggest X"
- "the design specification requires X"

Never report these as measured results.

## Source traceability requirement

Every numerical value used as evidence must trace to:
1. A file on disk
2. A specific column or field in that file
3. A specific experiment ID

If this trace cannot be established, the value may not be reported as evidence.

---

Source: adapted from `engineering-paper-skills/skills/_shared/evidence-boundary.md`

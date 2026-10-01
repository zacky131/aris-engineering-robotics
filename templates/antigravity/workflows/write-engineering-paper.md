# Workflow: Write Engineering Paper

**Purpose**: Guide the manuscript writing process from evidence-calibrated
claims through polished paper ready for submission. All writing must stay
within the claims allowed by `CLAIM_MAP.yaml`.

**Invoke with**:
```
Use the write-engineering-paper workflow to draft the Results section.
```

---

## Pre-conditions

Before writing, verify:
- `CLAIM_MAP.yaml` exists with at least one `status: supported` claim
- `EVIDENCE_LEDGER.yaml` exists with `verified: true` records
- `RESULT_SUMMARY.yaml` exists

If claims are all `status: unsupported`, stop and run the `analyze-robotics`
workflow first.

---

## Stage 1 — Check claim status

Read `CLAIM_MAP.yaml`.

Identify:
- Supported claims (available for manuscript)
- Partial claims (use with scope qualifiers)
- Unsupported claims (must not be used)

**Paper writing may only use supported or partial claims.**
Partial claims must use language within `permitted_language` and must include
appropriate scope qualifiers.

## Stage 2 — Audit paper story alignment

**Skill**: `engineering-paper-auditor`

Check:
- Story spine is complete: problem → gap → insight → method → evidence → boundary → implication
- Abstract/Introduction claims do not exceed supported claims
- Results section accurately reflects `RESULT_SUMMARY.yaml`
- Conclusion does not generalize beyond the evidence boundary
- No prohibited claim language present (`proves`, `guarantees`, `fully robust`, etc.)

Report audit findings before writing begins.

## Stage 3 — Write or revise manuscript sections

**Skill**: `engineering-writing`

Draft or revise:
- Introduction (problem, gap, contribution)
- Related Work (cite only found literature)
- Method/System (based on actual implementation)
- Results (based only on `RESULT_SUMMARY.yaml`)
- Discussion (within claim boundaries)
- Conclusion (within evidence level)
- Abstract

**Constraints**:
- Do not invent results, metrics, or trial counts
- Do not use claim language stronger than `CLAIM_MAP.yaml` permits
- Always include scope qualifiers on simulation results
- Boundary section must state what was NOT shown

## Stage 4 — Audit figures and tables

**Skill**: `engineering-figure-table`

For each figure or table:
- Verify source data file exists
- Verify plotted values match source
- Verify caption accurately describes the figure
- Verify caption claim matches `CLAIM_MAP.yaml`
- Flag any mismatch in: source → plotted → caption → Results text → Abstract

## Stage 5 — Polish language

**Skill**: `engineering-polishing`

Check:
- Terminology consistency (`terminology-ledger.md`)
- Sentence clarity and flow
- Passive/active voice balance
- Redundancy removal
- Claim language calibration

## Stage 6 — Validate for submission

**Skill**: `engineering-validation`

Check against venue requirements (if known):
- Page limit
- Figure count
- Reference style
- Section naming conventions
- Required sections (e.g., ethical statements, data availability)
- AI-assisted writing disclosure (if required)

---

## Final Check

Before declaring the manuscript ready:

1. Re-read Abstract and Conclusion
2. Verify every numerical value traces to a source file
3. Verify no claim exceeds the evidence level in `CLAIM_MAP.yaml`
4. Verify boundary statement is present and accurate
5. Verify all cited papers were found (not invented)

**A manuscript is not ready if any claim has `status: unsupported` and
that claim appears in the manuscript.**

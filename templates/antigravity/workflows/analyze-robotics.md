# Workflow: Analyze Robotics

**Purpose**: Analyse completed experiment results and update the evidence
and claim artifacts. Use after raw result files exist but have not yet been
processed into claims.

**Invoke with**:
```
Use the analyze-robotics workflow to process EXP001 results.
```

---

## Pre-conditions

Locate result files from any of:
- `results/` directory
- `logs/` directory
- CSV files referenced in `EXPERIMENT.yaml`
- JSON result files
- Rosbag-derived output files (pre-processed CSVs or JSON)
- `EXPERIMENT.yaml` — for context
- `EVIDENCE_LEDGER.yaml` — for linking evidence
- `CLAIM_MAP.yaml` — for updating claim status

## Stage 1 — Load experiment context

Read `EXPERIMENT.yaml` to identify:
- `experiment.id`
- `logging.output_dir` — where result files are
- `metrics` — which metrics to compute
- `platform.type` — for evidence level assignment

If `EXPERIMENT.yaml` is missing, ask the user to provide the result file paths.

## Stage 2 — Analyse results

**Skill**: `robotics-result-analysis`

Load result files and compute:
- Tracking metrics (RMSE, MAE, terminal error)
- Control effort metrics
- Mission success rate
- Real-time timing (if logged)
- Robustness metrics (if sweep data available)

Always state N (number of trials).
Do not fabricate values.
Produce `RESULT_SUMMARY.yaml`.

## Stage 3 — Validate simulation conditions

**Skill**: `simulation-validation`

If the experiment was simulation-based (L2/L3):
- Verify physics configuration is documented
- Verify baseline fairness
- Verify RTF was adequate
- Flag any condition asymmetries

## Stage 4 — Audit experiment integrity

**Skill**: `robotics-experiment-audit`

- Verify result files exist and are not empty
- Verify metrics in summary match source files
- Check baseline fairness was maintained
- Check scope (number of trials, scenarios)
- Detect claim-scope mismatches

Stop if `FAIL` is found. List required corrective actions.

## Stage 5 — Assign evidence level

**Skill**: `sil-hil-validation`

Assign L0–L6 based on `platform.type`.
Flag any manuscript claims that exceed the assigned evidence level.

Update `EVIDENCE_LEDGER.yaml`:
- Set `evidence_level`
- Set `verified: false` initially
- Fill metric values from `RESULT_SUMMARY.yaml`

Run `python tools/validate_evidence_ledger.py` if available.
Only set `verified: true` after validation passes.

## Stage 6 — Map results to claims

**Skill**: `robotics-result-to-claim`

For each claim in `CLAIM_MAP.yaml`:
- Assess whether current evidence supports it
- Assign `status: supported / partial / unsupported`
- Set permitted language based on evidence level
- List prohibited extensions
- List missing evidence for partial claims
- Suggest next experiments if needed

---

## Output

- `RESULT_SUMMARY.yaml` — filled and ready
- `EVIDENCE_LEDGER.yaml` — updated with evidence level and metrics
- `CLAIM_MAP.yaml` — updated status for each claim
- Corrective action list (if any audits failed)
- Next experiment recommendations (if any claims are partial)

Only update claim/evidence artifacts when source evidence can be verified.
Do not upgrade evidence level without actual evidence.

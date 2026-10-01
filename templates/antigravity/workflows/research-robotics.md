# Workflow: Research Robotics

**Purpose**: Guide a complete robotics/control research planning phase from
anchor paper intake and research question to experiment plan.

**Invoke with**: A research topic or question, e.g.
```
/research-robotics "Robust UAV interception using adaptive IMM-MPC"
```
or natural language:
```
Use the research-robotics workflow for my NMPC UAV landing research.
```

---

## Stage 1 — Detect Anchor Papers and Existing Context

Before starting, check:
- `anchor_papers/` — are PDF files present?
- `research/ANCHOR_MANIFEST.yaml` — are anchor papers already processed and unchanged?
- `RESEARCH_CONTRACT.md` — existing research question and claims
- `CLAIM_MAP.yaml` — existing claims
- `EXPERIMENT.yaml` or experiment tracker — existing experiments

Do not restart completed stages.

## Stage 2 — Anchor Paper Intake (if present)

**Skill**: `anchor-paper-intake`

- If `anchor_papers/` contains PDFs that are new or changed:
  Run `anchor-paper-intake` to extract structured paper records, build cross-paper synthesis, identify baseline methods and metrics, and formulate gap hypotheses.
- Outputs generated:
  - `research/ANCHOR_MANIFEST.yaml`
  - `research/anchor_records/AP*.yaml`
  - `research/ANCHOR_PAPER_INDEX.md`
  - `research/ANCHOR_PAPER_SYNTHESIS.md`
  - `research/ANCHOR_GAP_HYPOTHESES.md` (all marked `UNVERIFIED`)
  - `research/LITERATURE_SEARCH_PLAN.md`
  - `research/RESEARCH_GAP_MAP.md` (initial gap status)
- **Scientific invariant**: Anchor papers are starting points, not unquestionable authorities. Gap hypotheses remain `UNVERIFIED` until confirmed against recent literature.
- If no anchor papers are present, skip to Stage 3.

## Stage 3 — Profile Detection

**Skill**: `robotics-research-router`

Classify the research context into one or more profiles:
`classical_control`, `ros2_robotics`, `px4_uav`, `multi_robot`,
`learning_robotics`, `hybrid_ai_control`.
Also report anchor paper status and confirm whether anchor intake was satisfied.

## Stage 4 — Anchor-Guided Literature Search

**Skill**: `research-lit`

If `research/LITERATURE_SEARCH_PLAN.md` exists, execute its targeted search queries:
- Backward and forward citations from anchor seed papers
- Closest competing methods and recent updates
- Benchmark datasets and community-standard scenarios
- Relevant venues (ICRA, IROS, RA-L, T-RO, CDC, ACC, etc.)

Do not invent papers. Only report found literature.

## Stage 5 — Novelty and Gap Verification

**Skill**: `novelty-check`

- Evaluate each hypothesis in `research/ANCHOR_GAP_HYPOTHESES.md` against discovered literature.
- Verify whether the proposed method is distinct from both anchor papers and recent work.
- Avoid absolute claims like "no previous work has..." without extensive proof.

## Stage 6 — Update Research Gap Map

Update `research/RESEARCH_GAP_MAP.md` with verified gap lifecycle states:
- `SUPPORTED_AS_CURRENT_GAP`
- `PARTIALLY_RESOLVED`
- `RESOLVED_BY_PRIOR_WORK`
- `INSUFFICIENT_EVIDENCE`

Never promote an unverified gap to `SUPPORTED_AS_CURRENT_GAP` without independent literature evidence.

## Stage 7 — Research Refinement (if needed)

**Skill**: `research-refine` (or `idea-discovery`)

Sharpen the research question, core contribution, and boundary scope based on the verified gap map.

## Stage 8 — Define Initial Claim Hypotheses

**Skill**: `claims-drafting`

Draft placeholder claims to guide experiment design.
These are initial hypotheses, not evidenced claims.
Write them to `CLAIM_MAP.yaml` with `status: unsupported`.

## Stage 9 — Robotics Experiment Plan

**Skill**: `robotics-experiment-plan`

Load `research/ANCHOR_PAPER_SYNTHESIS.md` and `research/RESEARCH_GAP_MAP.md`.
Design the Q1–Q6 experiment matrix:
- Q1 PERFORMANCE — primary task metric
- Q2 MECHANISM — condition analysis
- Q3 COMPONENT — contribution isolation
- Q4 ROBUSTNESS — disturbance/uncertainty
- Q5 COMPUTATION — real-time feasibility
- Q6 FAILURE ENVELOPE — boundary conditions

Explicitly document baseline provenance (anchor vs literature), community-standard metrics, and specific experiments distinguishing the method from closest prior work.
Classify each experiment: `MUST_RUN` / `SHOULD_RUN` / `NICE_TO_HAVE`.
Map each to one or more claims in `CLAIM_MAP.yaml`.

---

## Output

At the end of this workflow, produce:
1. Anchor paper processing status and manifest (if anchor papers were provided)
2. `research/ANCHOR_PAPER_SYNTHESIS.md` and `research/RESEARCH_GAP_MAP.md`
3. Detected profiles
4. Literature summary (not invented)
5. Novelty assessment
6. Initial claim drafts in `CLAIM_MAP.yaml`
7. Experiment plan / run matrix
8. MUST_RUN experiments as draft `EXPERIMENT.yaml` files

Stop if required source material is missing.
Ask the user before adding NICE_TO_HAVE experiments beyond the declared time budget.

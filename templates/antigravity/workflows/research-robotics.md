# Workflow: Research Robotics

**Purpose**: Guide a complete robotics/control research planning phase from
research question to experiment plan.

**Invoke with**: A research topic or question, e.g.
```
/research-robotics "Robust UAV interception using adaptive IMM-MPC"
```
or natural language:
```
Use the research-robotics workflow for my NMPC UAV landing research.
```

---

## Stage 1 — Inspect existing research context

Before starting, read any existing files:
- `RESEARCH_CONTRACT.md` — existing research question and claims
- `CLAIM_MAP.yaml` — existing claims
- `EXPERIMENT.yaml` or experiment tracker — existing experiments
- Any paper draft

Do not restart completed stages.

## Stage 2 — Profile detection

**Skill**: `robotics-research-router`

Classify the research context into one or more profiles:
`classical_control`, `ros2_robotics`, `px4_uav`, `multi_robot`,
`learning_robotics`, `hybrid_ai_control`

## Stage 3 — Literature search

**Skill**: `research-lit`

Search for:
- Prior work in the detected domain
- Baseline methods to compare against
- Benchmark scenarios
- Relevant venues (ICRA, IROS, RA-L, T-RO, etc.)

Do not invent papers. Only report found literature.

## Stage 4 — Idea discovery (if needed)

**Skill**: `idea-discovery` or `idea-discovery-robot`

Only invoke if the research question needs sharpening or gaps need exploring.
Skip if the research question is already well-defined.

## Stage 5 — Novelty assessment

**Skill**: `novelty-check`

Verify the proposed method is distinct from prior work.
Report confidence and gaps.

## Stage 6 — Research refinement (if available)

**Skill**: `research-refine`

Sharpen the research question, contribution, and scope.

## Stage 7 — Define initial claims

**Skill**: `claims-drafting`

Draft placeholder claims to guide experiment design.
These are initial hypotheses, not evidenced claims.
Write them to `CLAIM_MAP.yaml` with `status: unsupported`.

## Stage 8 — Experiment plan

**Skill**: `robotics-experiment-plan`

Design the Q1–Q6 experiment matrix:
- Q1 PERFORMANCE — primary task metric
- Q2 MECHANISM — condition analysis
- Q3 COMPONENT — contribution isolation
- Q4 ROBUSTNESS — disturbance/uncertainty
- Q5 COMPUTATION — real-time feasibility
- Q6 FAILURE ENVELOPE — boundary conditions

Classify each experiment: `MUST_RUN` / `SHOULD_RUN` / `NICE_TO_HAVE`
Map each to one or more claims.

---

## Output

At the end of this workflow, produce:
1. Detected profiles
2. Literature summary (not invented)
3. Novelty assessment
4. Initial claim drafts in `CLAIM_MAP.yaml`
5. Experiment plan / run matrix
6. MUST_RUN experiments as draft `EXPERIMENT.yaml` files

Stop if required source material is missing.
Ask the user before adding NICE_TO_HAVE experiments beyond the declared time budget.

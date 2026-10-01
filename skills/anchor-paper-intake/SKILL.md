---
name: anchor-paper-intake
description: >
  Read user-provided anchor research papers before broad literature search.
  Extract methods, evidence, baselines, assumptions, limitations, references,
  and gap hypotheses, then build a structured starting point for robotics,
  control, automation, and engineering research.
  Part of Stage 0 in the research pipeline.
platforms:
  - codex
  - claude
  - antigravity
---

# Skill: anchor-paper-intake

## Purpose

Process user-provided PDF papers in `anchor_papers/` before any broad literature
search, idea generation, novelty analysis, or experiment planning begins.

Anchor papers are **starting points**, not unquestionable authorities.
Every gap found in them is an **unverified hypothesis** until independently
confirmed by current literature.

---

## Scientific Invariant (MANDATORY)

```
ANCHOR PAPERS
    ↓
understand terminology, methods, evidence, limitations, references
    ↓
generate gap HYPOTHESES (UNVERIFIED)
    ↓
independent literature expansion
    ↓
verify novelty / current research gap
    ↓
research design
```

**NEVER implement:**
```
ANCHOR PAPER SAYS GAP EXISTS → ASSUME GAP IS NOVEL
```

Always distinguish:
- `AUTHOR-CLAIMED GAP` — what the paper's authors state as future work or limitation
- `CURRENTLY VERIFIED GAP` — confirmed by independent literature search to still be open

---

## Directory Layout Discovery

### Discover all PDFs

Scan `anchor_papers/` recursively for `.pdf` files.

Recognize both layouts:

**Simple:**
```
anchor_papers/
├── paper1.pdf         → category: uncategorized
└── paper2.pdf         → category: uncategorized
```

**Categorized:**
```
anchor_papers/
├── foundational/       → theory, history
├── closest_work/       → strongest novelty comparators
├── methodology/        → design, algorithms, metrics
├── benchmark/          → baselines, datasets, protocols
└── uncategorized/      → no assigned role
```

Do not treat category as proof of relevance.

---

## PDF Reading Behavior

**If the runtime can read PDFs directly:**
- Read the full PDF content
- Inspect figures, tables, equations where materially relevant
- Maintain page-level traceability where possible

**If the runtime cannot parse PDFs:**
- Fail clearly and explain the capability gap
- Do NOT fabricate extraction from filenames or titles
- Do NOT infer paper content from context clues

---

## Manifest Management (`research/ANCHOR_MANIFEST.yaml`)

Before processing any paper:

1. Read `research/ANCHOR_MANIFEST.yaml` if it exists
2. For each PDF discovered:
   - Compute SHA-256 fingerprint
   - If `sha256` matches manifest and `processed: true` → SKIP (no reprocessing)
   - If missing from manifest or SHA changed → process (new or updated)
3. If a previously-manifested PDF is no longer found:
   - Mark it `removed: true` in the manifest
   - Warn: "AP00X was previously processed but the PDF is now missing. Synthesis should be regenerated."
4. After processing, write the updated manifest

---

## Extraction Protocol (per paper)

For each paper, produce an `ANCHOR_PAPER_RECORD.yaml` (template in `templates/`).

Extract:

### 1. Bibliographic metadata
- Title, authors, year, venue, DOI, URL
- If not clearly stated: `null`
- DO NOT invent or infer DOI / URLs

### 2. Research problem
- What problem is this paper solving?
- What is the motivation?

### 3. Method
- Name and class (e.g., MPC, EKF, PPO)
- Architecture overview
- Key components and design choices

### 4. System
- Domain, robot type, controller, estimator, planner
- Middleware (ROS 2, MATLAB, Python)
- Simulator (Gazebo, PyBullet, etc.)
- Autopilot (PX4, ArduPilot)
- Hardware (if physical)

### 5. Experimental design
- Scenarios tested
- Baselines compared against
- Metrics reported
- Number of trials / repetitions
- Simulation or real (assign L0–L6)

### 6. Evidence
- Main findings (quantitative and qualitative)
- Use authors' reported values — do NOT compute new statistics

### 7. Assumptions (explicit + inferred)
- Record separately: `explicit_assumptions` vs `inferred_assumptions`

### 8. Limitations
- `explicit_author_limitations`: stated by the authors
- `inferred_limitations`: reasoned by the agent (must record basis and confidence)
- **Do NOT write inferred limitations as though authors stated them**

### 9. Future work (explicit)
- Verbatim or closely paraphrased from the paper

### 10. References to follow
- Backward candidates: key cited works to retrieve
- Method candidates: references that define the baseline/algorithm
- Benchmark candidates: datasets, evaluation protocols, scenario definitions

### 11. Relevance to current project

---

## Gap Hypothesis Generation

After extracting all papers, generate gap hypotheses in `research/ANCHOR_GAP_HYPOTHESES.md`.

**Every hypothesis starts as `UNVERIFIED`.**

For each gap:
- State the hypothesis precisely
- Record which anchor papers support it (with specific claim/page)
- Record what evidence type (author-claimed, inferred)
- State a falsification condition: what would prove this gap no longer exists?
- Generate search queries for the literature search stage

**Do NOT:**
- promote a gap to `SUPPORTED_AS_CURRENT_GAP` without independent literature evidence
- assume an older paper's claimed gap is still open today
- invent contradictory findings

---

## Conflict Detection

If anchor papers report contradictory findings, create a `## Conflicting Findings` block.

Example:
```
AP001: MPC improves stability under 50ms delay
AP003: MPC degrades under 45ms delay in similar scenario

Possible explanatory differences (hypotheses, NOT conclusions):
- different estimator
- different control rate
- different vehicle dynamics
- different disturbance model
```

Do not choose one paper's finding as correct.

---

## Outputs Generated

After processing, produce or update:

| File | Location | Content |
|---|---|---|
| `ANCHOR_MANIFEST.yaml` | `research/` | PDF fingerprints, IDs, process status |
| Per-paper records | `research/anchor_records/AP001.yaml` | Structured extraction |
| `ANCHOR_PAPER_INDEX.md` | `research/` | Factual index table + per-paper sections |
| `ANCHOR_PAPER_SYNTHESIS.md` | `research/` | Cross-paper comparison matrix and synthesis |
| `ANCHOR_GAP_HYPOTHESES.md` | `research/` | Hypothesis list, all UNVERIFIED |
| `LITERATURE_SEARCH_PLAN.md` | `research/` | Anchor-derived search directions |

---

## `ANCHOR_PAPER_INDEX.md` Format

Table header:
```
| ID | Category | Title | Year | Venue | Method | Platform | Evidence Level | File |
```

Then for each paper:
```
## AP001
### Bibliographic metadata
### Research problem
### Method
### Experimental protocol
### Baselines
### Metrics
### Main findings
### Assumptions
### Explicit author limitations
### Inferred limitations [with basis and confidence]
### Explicit future work
### Important references to follow
### Relevance to this project
```

Mark all agent interpretations with: `[AGENT INTERPRETATION — not author-stated]`

---

## `ANCHOR_PAPER_SYNTHESIS.md` Format

Cross-paper comparison matrix (columns may vary by domain):

```
| Paper | Problem | Method | Platform | Baselines | Metrics | Evidence | Main Limitation | Relevance |
```

Robotics/control synthesis axes:
- controller type, estimator type, motion model
- sensor model, noise model, delay, disturbances, constraints
- solver, real-time computation, simulation fidelity
- SIL/HIL/real evidence level, scenario diversity
- failure analysis

Then: common assumptions, dominant methods, baseline conventions, contradictory findings, unresolved limitations, reusable evaluation patterns.

---

## `LITERATURE_SEARCH_PLAN.md` Format

Sections:
```
A. Backward citation search   (important cited works)
B. Forward citation search    (newer work citing these papers)
C. Closest-method search      (similar methods and architectures)
D. Limitation-driven search   (papers addressing stated limitations)
E. Recent-update search       (last 1–2 years: has gap been solved?)
F. Competing-method search    (alternative approaches)
G. Benchmark search           (evaluation protocols, datasets, scenarios)

## Citation seeds
(prioritized list from anchor references)
```

If citation metadata cannot be reliably reconstructed: write `metadata verification required`.

---

## `RESEARCH_GAP_MAP.md` Format (initialized here, updated by novelty-check)

Table:
```
| Gap ID | Anchor Basis | Current Literature Evidence | Status | Closest Work | Remaining Difference |
```

Initialize all statuses as `UNVERIFIED` when created here.

Gap lifecycle states:
- `UNVERIFIED` — from anchor, not yet literature-searched
- `SEARCHING` — actively being searched
- `SUPPORTED_AS_CURRENT_GAP` — confirmed open by literature
- `PARTIALLY_RESOLVED` — partially addressed by prior work
- `RESOLVED_BY_PRIOR_WORK` — gap no longer exists
- `INSUFFICIENT_EVIDENCE` — cannot determine gap status

**Never promote UNVERIFIED → SUPPORTED_AS_CURRENT_GAP without literature evidence.**

---

## Handoff

After completing intake, report:

```
ANCHOR PAPER INTAKE — COMPLETE
Papers processed: N
New: N  Updated: N  Skipped (unchanged): N

Outputs:
  research/ANCHOR_MANIFEST.yaml
  research/anchor_records/ (N records)
  research/ANCHOR_PAPER_INDEX.md
  research/ANCHOR_PAPER_SYNTHESIS.md
  research/ANCHOR_GAP_HYPOTHESES.md (M hypotheses, all UNVERIFIED)
  research/LITERATURE_SEARCH_PLAN.md
  research/RESEARCH_GAP_MAP.md (M gaps, all UNVERIFIED)

MANDATORY NEXT STEP: research-lit (using LITERATURE_SEARCH_PLAN.md)
Gap hypotheses must NOT be used for research design until literature verification.
```

---

## What This Skill Must Not Do

- Upload PDFs anywhere
- Modify or delete source PDFs
- Commit PDFs (they are git-ignored)
- Invent paper metadata, DOIs, or author lists
- Infer experimental results not stated in the paper
- Promote author-claimed gaps to verified current gaps
- Declare novelty or claim a contribution is new
- Fabricate baseline comparisons or missing experimental details

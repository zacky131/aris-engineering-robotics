# Anchor Papers Guide

## What Are Anchor Papers?

**Anchor papers** are user-provided research papers that serve as the foundational starting point for your research workflow. Instead of having an AI agent start with unfocused broad web searches, anchor papers ground the agent in the exact terminology, mathematical formulations, baseline algorithms, datasets, hardware platforms, and evaluation conventions relevant to your specific research goal.

Anchor papers are **starting points, not unquestionable authorities**. The core scientific invariant implemented by ARIS Engineering Robotics is:

```
ANCHOR PAPERS
    ↓
extract terminology, methods, evidence, limitations, references
    ↓
generate gap hypotheses (marked UNVERIFIED)
    ↓
independent literature expansion (targeted search)
    ↓
verify novelty & current research gap status
    ↓
research design & experiment planning
```

> [!IMPORTANT]
> Never assume an anchor paper's stated limitations remain open research gaps today. Older anchor papers may have had their limitations solved by subsequent literature. The system strictly distinguishes between an **Author-Claimed Gap** and a **Currently Verified Gap**.

---

## Directory Layouts

Place your anchor PDFs in the `anchor_papers/` directory of your project. Both simple and categorized layouts are supported.

### Simple Layout

Ideal for quick starts with a handful of papers:

```text
my-research-project/
└── anchor_papers/
    ├── README.md
    ├── paper1.pdf
    ├── paper2.pdf
    └── paper3.pdf
```

All papers default to `category: uncategorized`.

### Categorized Layout (Recommended)

Allows the agent to understand each paper's primary role in your investigation:

```text
my-research-project/
└── anchor_papers/
    ├── README.md
    ├── foundational/      # Theoretical foundations, classic papers
    │   └── survey_or_classic.pdf
    ├── closest_work/      # Direct competitors, closest prior state-of-the-art
    │   └── recent_competitor.pdf
    ├── methodology/       # Papers providing algorithms, estimators, or architectures
    │   └── kalman_filter_variant.pdf
    ├── benchmark/         # Baseline protocols, public datasets, evaluation metrics
    │   └── benchmark_suite.pdf
    └── uncategorized/     # General reference papers
        └── background.pdf
```

| Category | Description & Purpose |
|---|---|
| `foundational` | Core theories, seminal formulations, and mathematical frameworks |
| `closest_work` | Closest competing approaches; primary focus of novelty analysis |
| `methodology` | Specific algorithms, controllers, estimators, or implementation designs |
| `benchmark` | Evaluation protocols, baseline comparison setups, and datasets |
| `uncategorized` | Papers without an assigned role |

---

## Generated Artifacts

When you invoke `anchor-paper-intake` (or run `robotics-research-router` when anchor papers are present), the agent produces structured files under `research/`:

```text
my-research-project/
└── research/
    ├── ANCHOR_MANIFEST.yaml       # SHA-256 fingerprints & stable AP001 IDs
    ├── anchor_records/            # Detailed YAML extractions per paper
    │   ├── AP001.yaml
    │   ├── AP002.yaml
    │   └── ...
    ├── ANCHOR_PAPER_INDEX.md      # Factual index table + per-paper analysis
    ├── ANCHOR_PAPER_SYNTHESIS.md  # Cross-paper comparison matrix & synthesis
    ├── ANCHOR_GAP_HYPOTHESES.md   # Initial gap hypotheses (all UNVERIFIED)
    ├── LITERATURE_SEARCH_PLAN.md  # Targeted forward/backward search queries
    └── RESEARCH_GAP_MAP.md        # Gap lifecycle tracker
```

### 1. `ANCHOR_MANIFEST.yaml`
Assigns deterministic IDs (`AP001`, `AP002`, ...) and tracks SHA-256 hashes. If a PDF is unchanged, it is not reprocessed. If a PDF is removed, stale claims are flagged.

### 2. `ANCHOR_PAPER_INDEX.md`
A factual catalog containing bibliographic data, problem summary, method architecture, simulation/experimental protocol, metrics, findings, assumptions, explicit author limitations, inferred limitations, and key citations.

### 3. `ANCHOR_PAPER_SYNTHESIS.md`
A comparative matrix contrasting all anchor papers across control architectures, estimators, simulation fidelity, noise models, disturbances, and unresolved limitations. Also highlights conflicting findings between papers.

### 4. `ANCHOR_GAP_HYPOTHESES.md`
Extracts candidate gaps derived from anchor limitations. Every gap is explicitly marked `Status: UNVERIFIED` with concrete falsification criteria.

### 5. `LITERATURE_SEARCH_PLAN.md`
Creates structured queries for broader literature exploration:
- Backward citation seeds
- Forward citation seeds
- Closest-method search queries
- Limitation-driven search queries
- Competing-method search queries

### 6. `RESEARCH_GAP_MAP.md`
Tracks gaps throughout the research lifecycle:
- `UNVERIFIED` — initial hypothesis from anchor paper
- `SEARCHING` — literature search underway
- `SUPPORTED_AS_CURRENT_GAP` — confirmed unresolved by recent papers
- `PARTIALLY_RESOLVED` — partially addressed by recent literature
- `RESOLVED_BY_PRIOR_WORK` — already solved (reject as core novelty)
- `INSUFFICIENT_EVIDENCE` — search inconclusive

---

## Stage 0 in the Research Pipeline

In `research-pipeline-robotics`, Anchor Paper Intake is **Stage 0**:

```text
Stage 0 — Anchor Paper Intake (anchor-paper-intake)
Stage 1 — Understand Research Question
Stage 2 — Select Robotics / Control Profile (robotics-research-router)
Stage 3 — Anchor-Guided Literature Expansion (research-lit)
Stage 4 — Gap and Novelty Verification (novelty-check → RESEARCH_GAP_MAP.md)
Stage 5 — Research Refinement (research-refine)
Stage 6 — Claim Hypotheses (claims-drafting)
Stage 7 — Experiment Planning (robotics-experiment-plan)
...
```

If `anchor_papers/` contains PDFs:
- Stage 0 executes first.
- Literature search (Stage 3) and novelty verification (Stage 4) consume the anchor search plan and gap hypotheses.
- Experiment planning (Stage 7) verifies baseline choices and metrics against anchor synthesis.

If no anchor papers are provided:
- The pipeline records `"no anchor papers supplied"` and executes the standard research workflow.

---

## Privacy, Copyright, and `.gitignore`

Research PDFs may be copyrighted, subject to institutional licenses, or unpublished confidential manuscripts.
To protect research integrity and privacy:
- The framework `.gitignore` excludes `anchor_papers/**/*.pdf`.
- Only metadata, synthesis files, and templates are tracked in git.
- **Never upload confidential PDFs to external unapproved endpoints.**

---

## Initializing a Project

To set up the anchor paper structure in any new or existing project:

```bash
bash tools/init_research_project.sh /path/to/my_robotics_project
```

This creates:
- `anchor_papers/{foundational,closest_work,methodology,benchmark,uncategorized}/`
- `anchor_papers/README.md`
- `research/`
- Starter templates (`EXPERIMENT.yaml`, `EVIDENCE_LEDGER.yaml`, `CLAIM_MAP.yaml`, `RESEARCH_CONTRACT.md`) without overwriting existing files.

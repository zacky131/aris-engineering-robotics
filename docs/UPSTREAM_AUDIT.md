# Upstream Audit

Generated: 2026-09-30

---

## Repository A — ARIS (`Auto-claude-code-research-in-sleep`)

### Reusable without modification

| Skill | Notes |
|---|---|
| `research-lit` | Domain-agnostic literature search |
| `idea-discovery` | Generic gap/idea discovery |
| `idea-discovery-robot` | Already robotics-targeted variant |
| `novelty-check` | Novelty assessment against literature |
| `research-implement-feature` | Implementation planning skill |
| `analyze-results` | General result interpretation |
| `ablation-planner` | Component-wise ablation design |
| `paper-writing` / `paper-write` | General manuscript drafting |
| `paper-claim-audit` | Claim-evidence alignment |
| `research-review` | Paper review workflow |
| `rebuttal` | Reviewer response |
| `paper-compile` | Compilation/packaging |
| `claims-drafting` | Initial claim formulation |
| `formula-derivation` | Mathematical derivation |
| `citation-audit` | Citation checking |
| `mermaid-diagram` | Diagram generation |
| `research-wiki` | Research notes wiki |
| `figure-spec` / `paper-figure` | Figure specification |

### Reusable with wrapper/adaptation

| Skill | Adaptation needed |
|---|---|
| `experiment-plan` | ML-centric defaults must be overridden by robotics profile |
| `run-experiment` | Backend detection must be extended for ROS2/Gazebo/PX4 |
| `monitor-experiment` / `training-check` | Rewired to robotics watchdog checks (not GPU/loss curves) |
| `result-to-claim` | Needs evidence-level (L0–L6) and scope fields |
| `experiment-audit` | Needs robotics-specific baseline fairness checks |
| `research-pipeline` | Must be wrapped as `research-pipeline-robotics` with stopping criteria |
| `dse-loop` | Reused as basis for `controller-tuning` DSE backend |
| `research-refine` | Applicable as-is for robotics papers |
| `research-refine-pipeline` | Applicable with minor adaptation |

### ML-specific and not suitable as default robotics behavior

| Skill | Reason |
|---|---|
| `vast-gpu` | GPU cloud provisioning; not relevant for SIL/HIL |
| `serverless-modal` | Modal cloud training runner |
| `training-check` | GPU/loss-curve specific |
| `feishu-notify` | China IM-specific notifier |
| `xhs_post.md` | Social media posting |
| `auto-review-loop-minimax` | Minimax-specific LLM |
| `pixel-art` | Illustration generation; unrelated |
| `interview-cheatsheet` | Job interview prep |
| `grant-proposal` | Grant writing (out of scope) |
| `patent-*` | Patent workflow (out of scope) |
| `slides-*` / `paper-slides` | Presentation generation (secondary) |
| `poster-*` | Poster generation (secondary) |

### Useful orchestration patterns

- `research-pipeline` sequential stage pattern (→ basis for robotics pipeline)
- `dse-loop` parameter sweep pattern (→ basis for `controller-tuning`)
- `experiment-bridge` (→ adapted for robotics backend dispatch)
- `experiment-queue` (→ adapted for robotics run queue)
- `shared-references` reference management convention

---

## Repository B — Engineering Paper Skills (`engineering-paper-skills`)

### Reusable without modification

| Skill/File | Notes |
|---|---|
| `engineering-writing` | Full manuscript writing skill |
| `engineering-polishing` | Polish and language check |
| `engineering-paper-auditor` | Complete audit workflow |
| `engineering-figure-table` | Figure/table evidence tracing |
| `engineering-response` | Reviewer response generation |
| `engineering-validation` | Pre-submission validation |
| `engineering-paper-router` | Skill routing for paper tasks |
| `engineering-paper-coach` | Writing coaching |
| `_shared/evidence-boundary.md` | Core scientific integrity rule |
| `_shared/claim-strength.md` | Claim language calibration |
| `_shared/story-spine.md` | Story structure |
| `_shared/sentence-role-and-story-flow.md` | Sentence-level writing logic |
| `_shared/terminology-ledger.md` | Term consistency |
| `_shared/citation-boundary.md` | Citation integrity |
| `_shared/citation-verification-workflow.md` | Citation verification |
| `_shared/ai-assisted-writing-policy.md` | AI disclosure policy |
| `_shared/list-to-argument.md` | Converting lists to prose arguments |

### Reusable with adaptation

| File | Adaptation needed |
|---|---|
| Venue profiles (if any) | Extend with robotics venues: ICRA, IROS, RAL, T-RO, T-ASE, CDC, IfAC |

### Paper-quality governance rules worth making global

- `evidence-boundary.md` — promoted to integration-level global invariant
- `claim-strength.md` — promoted globally, extended with SIL/HIL levels
- `story-spine.md` — promoted globally with robotics result chain
- `terminology-ledger.md` — promoted globally

---

## Overlap / Conflicts

| ARIS capability | Engineering Paper Skills capability | Owner in integrated system | Reason |
|---|---|---|---|
| `result-to-claim` | `engineering-paper-auditor` evidence check | `robotics-result-to-claim` (new) + EPS auditor | New skill adds L0–L6 and scope; EPS auditor validates manuscript |
| `experiment-audit` | EPS evidence traceability in `engineering-paper-auditor` | `robotics-experiment-audit` + EPS auditor | Experiment-level vs manuscript-level auditing |
| `paper-writing` | `engineering-writing` | EPS `engineering-writing` primary | EPS is more mature for engineering paper writing |
| `paper-claim-audit` | `engineering-paper-auditor` | EPS `engineering-paper-auditor` primary | EPS has more rigorous audit rules |
| `rebuttal` | `engineering-response` | EPS `engineering-response` primary | EPS version is engineering-venue aware |
| `paper-compile` | `engineering-validation` | EPS `engineering-validation` primary | EPS handles venue-specific validation |
| `claims-drafting` | Implicit in EPS auditor | `robotics-result-to-claim` (claim generation) + EPS auditor (validation) | Generation vs validation split |

---

## Integration Decisions

1. **ARIS research-front skills are installed as-is**: `research-lit`, `idea-discovery`, `novelty-check`, `research-implement-feature` are general enough to use unchanged.

2. **EPS paper-writing skills are installed as-is**: The engineering paper skills are more mature than ARIS paper writing for engineering venues. ARIS paper-writing serves as backup.

3. **New robotics integration layer**: 11 new skills are created specifically for robotics/control research that ARIS and EPS do not cover.

4. **ML-specific ARIS skills are NOT installed by default**: GPU, cloud, and ML-training-specific skills are excluded from default install. Users can add them manually.

5. **Global integrity rules** are promoted from EPS `_shared/` and extended with robotics-specific additions in `shared/`.

6. **Evidence level L0–L6** is a new concept in this integration, synthesizing SIL/HIL practice with EPS evidence-boundary rules.

7. **Claim map** is a new integration artifact linking experiment evidence to manuscript claims across both upstream systems.

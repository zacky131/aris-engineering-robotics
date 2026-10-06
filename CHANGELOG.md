# Changelog

All notable changes to ARIS Engineering Robotics are documented here.

Format: [Semantic Versioning](https://semver.org/)

## [0.4.0] — 2026-10-06

### Added — Vision-Language-Action (VLA), Learning-Based Control, AI Control & SOTA Safety Filters

**Vision-Language-Action (VLA) in Robotics**
- `profiles/vla_robotics.yaml` — profile covering OpenVLA, Octo, RT-1/2, π0, SmolVLA, ACT, and Diffusion Policy.
- `skills/vla-robotics/SKILL.md` — end-to-end VLA workflow managing visual/proprioceptive inputs, high-level (5–10 Hz) vs low-level (100–500 Hz) frequency decoupling, action chunking, temporal ensembling, and workspace bounding-box safety cages.
- `shared/vla-standards.md` & `skills/_shared/vla-standards.md` — benchmark evaluation rules (SIMPLER Env, LIBERO, CALVIN, ManiSkill), camera frame validation, action frame normalization, and latency budgets.
- `schemas/vla-evaluation.schema.json` & `templates/VLA_EVALUATION.yaml` — formal validation schema and configuration template for VLA evaluations.
- `templates/antigravity/workflows/vla-robotics.md` — dedicated Antigravity workflow for end-to-end VLA benchmarking and deployment.

**Learning-Based Control & Sim-to-Real**
- `profiles/learning_control.yaml` — profile for model-free/model-based/offline DRL (PPO, SAC, TD3, CQL, IQL) and sim-to-real transfer.
- `skills/learning-control-eval/SKILL.md` — multi-seed statistical evaluation implementing Agarwal et al. (2021) / `rliable` standards: Interquartile Mean (IQM), 95% bootstrap confidence intervals (2,000 resamples), performance profiles, and domain randomization auditing.
- `shared/learning-control-standards.md` & `skills/_shared/learning-control-standards.md` — statistical reporting protocols and RMA teacher-student distillation verification.
- `schemas/learning-control.schema.json` & `templates/LEARNING_EXPERIMENT.yaml` — schema and template for reinforcement learning experiments.
- `templates/antigravity/workflows/learning-control.md` — dedicated Antigravity workflow for learning-based control experiments.

**AI-Based & Physics-Informed Control**
- `profiles/ai_control.yaml` — profile for Neural ODEs, Physics-Informed Neural Networks (PINNs), Neural MPC, GP-MPC, and Residual RL.
- `shared/ai-control-realtime.md` & `skills/_shared/ai-control-realtime.md` — real-time latency budgets ($P99 < T_s$), GPU jitter isolation, and deterministic fallback controllers.

**SOTA Safety Filters & Control Barrier Functions (CBF)**
- `profiles/safe_sota_control.yaml` — profile for formal safety shields, CBF, CLF-CBF, and QP filtering.
- `skills/safety-filter-cbf/SKILL.md` — synthesizes Control Barrier Function QP shields between high-level policies (VLA/DRL) and low-level actuators, enforcing forward invariance and slack relaxation.
- `shared/safety-cbf-standards.md` & `skills/_shared/safety-cbf-standards.md` — mathematical invariants, QP solver configuration (OSQP, qpOASES, Clarabel), and infeasibility fallback protocols.

**Core Pipeline & Watchdog Upgrades**
- `skills/robotics-research-router/SKILL.md` — added keyword detection and routing for `vla_robotics`, `learning_control`, `ai_control`, and `safe_sota_control`.
- `skills/robotics-watchdog/SKILL.md` — added VLA inference latency monitoring, camera feed freeze watchdog, action chunk delta spike detection, and CBF QP solver feasibility tracking.
- `skills/robotics-result-analysis/SKILL.md` — added VLA and Learning metrics (IQM, bootstrap CI, subtask progression, action jerk, inference latency).
- `skills/robotics-experiment-audit/SKILL.md` — added OOD split audits, prompt disjointness audits, and multi-seed fairness audits.
- `skills/research-pipeline-robotics/SKILL.md` — expanded execution and evaluation stages for VLA and learning pipelines.
- `docs/VLA_AND_AI_CONTROL.md` — dedicated comprehensive technical guide.

---

## [0.3.0] — 2026-10-01

### Added — Anchor-Paper-First Research Intake, End-to-End Workflow & Self-Contained Bundling

**Self-Contained All-in-One Skill Bundling**
- Bundled all 30 ARIS research/literature skills and 8 EPS engineering paper skills directly into `skills/` and `shared/`
- Zero external dependencies required at install time: 50 skills + shared references ready immediately upon `git clone`
- Preserved `tools/sync_upstreams.sh` for optional synchronization with upstream author repositories

**New Skill & Intake System**
- `skills/anchor-paper-intake/SKILL.md` — parses user anchor PDFs before broad literature search, extracts structured records, builds cross-paper synthesis, and generates gap hypotheses
- `anchor_papers/` directory structure with support for simple (flat) and categorized layouts (`foundational/`, `closest_work/`, `methodology/`, `benchmark/`, `uncategorized/`)
- `tools/init_research_project.sh` — non-destructive research project initializer creating directory layouts and starter templates

**Scientific Invariant & Gap Lifecycle**
- Enforces invariant: Anchor limitations are unverified hypotheses, not confirmed facts or current gaps
- Gap lifecycle tracking with 6 explicit states: `UNVERIFIED`, `SEARCHING`, `SUPPORTED_AS_CURRENT_GAP`, `PARTIALLY_RESOLVED`, `RESOLVED_BY_PRIOR_WORK`, `INSUFFICIENT_EVIDENCE`
- Distinction between Author-Claimed Gaps and Currently Verified Gaps

**Schemas & Templates**
- `schemas/anchor-paper-record.schema.json` — validation schema for structured paper extraction
- `schemas/anchor-manifest.schema.json` — validation schema for PDF fingerprint tracking
- `templates/ANCHOR_PAPER_RECORD.yaml` & `templates/ANCHOR_MANIFEST.yaml`
- Research output templates:
  * `templates/research/ANCHOR_PAPER_INDEX.md`
  * `templates/research/ANCHOR_PAPER_SYNTHESIS.md`
  * `templates/research/ANCHOR_GAP_HYPOTHESES.md`
  * `templates/research/LITERATURE_SEARCH_PLAN.md`
  * `templates/research/RESEARCH_GAP_MAP.md`
- Updated `templates/RESEARCH_CONTRACT.md` with literature anchor and search policies

**Pipeline & Skill Integration**
- `skills/research-pipeline-robotics/SKILL.md` — updated to 22 stages (Stages 0–21) with Anchor Paper Intake as Stage 0
- `skills/robotics-research-router/SKILL.md` — automatically detects `anchor_papers/` PDFs and routes to `anchor-paper-intake`
- `skills/robotics-experiment-plan/SKILL.md` — verifies baseline provenance, community-standard metrics, and gap alignment against anchor synthesis

**Platform & Workflow Integration**
- `templates/antigravity/AGENTS.md` — added persistent Anchor Papers rule
- `templates/antigravity/workflows/research-robotics.md` — updated to 9-stage anchor-guided workflow
- `tools/install_skills.sh` & `tools/validate_installation.py` — registered `anchor-paper-intake` across Codex, Claude, and Antigravity

**Documentation & End-to-End Workflow**
- `docs/ANCHOR_PAPERS.md` — comprehensive guide on anchor-paper research intake, layouts, gap lifecycles, and copyright rules
- `README.md` — added "Start Research from Anchor Papers" and complete "End-to-End Sample Prompt Workflow from ARIS to Engineering Paper" spanning Phase 0 through Phase 4

---

## [0.2.0] — 2026-10-01

### Added — Google Antigravity support

**Installer**
- `--platform antigravity` support in `tools/install_skills.sh`
- Project-local install to `.agents/skills/` (Antigravity native path)
- User-wide install to `~/.gemini/config/skills/`
- AGENTS.md safe managed-block patching (non-destructive)
- Workflow files install to `.agents/workflows/`
- `--list-platforms` / `--list-skills` options
- `--bootstrap` flag (auto-calls `bootstrap_upstreams.sh`)
- Shared dependency installation (`_shared`, `shared-references`)
- Structured YAML manifest (`installed-manifest.yaml`)

**Upstream bootstrap**
- `tools/bootstrap_upstreams.sh` — fetches upstreams into `vendor/upstreams/`
- 5-level resolution: env var → config → sibling → vendor → error

**Antigravity templates**
- `templates/antigravity/AGENTS.md` — persistent project rules with managed markers
- `templates/antigravity/workflows/research-robotics.md`
- `templates/antigravity/workflows/experiment-robotics.md`
- `templates/antigravity/workflows/analyze-robotics.md`
- `templates/antigravity/workflows/write-engineering-paper.md`

**Skill metadata**
- Added `antigravity` to `platforms:` in all 11 native skills

**Validation**
- `validate_installation.py` supports `--platform antigravity`
- SKILL.md frontmatter validation, shared dependency checks

**Documentation**
- `docs/ANTIGRAVITY.md` — full Antigravity guide
- `docs/PLATFORM_COMPATIBILITY.md` — three-platform capability matrix
- `README.md` — Antigravity quickstart section

**Tests**
- `tests/test_antigravity.py` — 7 Antigravity tests (A–G)

---

## [0.1.0] — 2026-09-30


### Added

**Repository structure**
- Initial integration repository combining ARIS and engineering-paper-skills
- `.aris-engineering-robotics/config.yaml` — upstream path configuration
- `vendor/README.md` — vendoring policy

**Documentation**
- `docs/UPSTREAM_AUDIT.md` — full audit of both upstream repositories
- `docs/ARCHITECTURE.md` — system architecture with Mermaid diagrams
- `docs/INSTALL.md` — full installation instructions
- `docs/QUICKSTART.md` — three worked examples (MPC UAV, PX4 landing, MARL)
- `docs/SKILL_OWNERSHIP.md` — explicit skill routing ownership table
- `docs/EVIDENCE_MODEL.md` — L0–L6 evidence classification system
- `docs/ROBOTICS_EXPERIMENT_MODEL.md` — experiment contract documentation
- `docs/RESEARCH_WORKFLOW.md` — end-to-end research workflow
- `docs/CUSTOMIZATION.md` — customisation and extension guide
- `docs/MIGRATION_AND_UPDATE.md` — update instructions

**New Skills**
- `skills/robotics-research-router` — profile detection and skill routing
- `skills/robotics-experiment-plan` — Q1–Q6 experiment design framework
- `skills/run-robotics-experiment` — multi-backend experiment runner
- `skills/robotics-watchdog` — experiment health monitoring
- `skills/robotics-result-analysis` — domain-aware metrics and statistics
- `skills/controller-tuning` — DSE-based controller parameter optimisation
- `skills/robotics-experiment-audit` — integrity and fairness audit
- `skills/simulation-validation` — simulation scientific validity check
- `skills/sil-hil-validation` — evidence level classification
- `skills/robotics-result-to-claim` — evidence-calibrated claim generation
- `skills/research-pipeline-robotics` — full orchestration pipeline

**Shared integrity rules**
- `shared/evidence-boundary.md`
- `shared/claim-strength.md`
- `shared/story-spine.md`
- `shared/robotics-metrics.md`
- `shared/control-metrics.md`
- `shared/experiment-integrity.md`
- `shared/simulation-integrity.md`
- `shared/timing-and-realtime.md`
- `shared/statistical-reporting.md`
- `shared/sil-hil-real-evidence.md`
- `shared/claim-language.md`
- `shared/terminology-ledger.md`

**Profiles**
- `profiles/classical_control.yaml`
- `profiles/ros2_robotics.yaml`
- `profiles/px4_uav.yaml`
- `profiles/multi_robot.yaml`
- `profiles/learning_robotics.yaml`
- `profiles/hybrid_ai_control.yaml`

**Schemas**
- `schemas/experiment.schema.json`
- `schemas/evidence-ledger.schema.json`
- `schemas/claim-map.schema.json`
- `schemas/result-record.schema.json`

**Templates**
- `templates/EXPERIMENT.yaml`
- `templates/EXPERIMENT_TRACKER.md`
- `templates/EVIDENCE_LEDGER.yaml`
- `templates/CLAIM_MAP.yaml`
- `templates/RESULT_SUMMARY.yaml`
- `templates/RESEARCH_CONTRACT.md`

**Tools**
- `tools/install_skills.sh`
- `tools/uninstall_skills.sh`
- `tools/validate_installation.py`
- `tools/validate_evidence_ledger.py`
- `tools/validate_result_record.py`
- `tools/sync_upstreams.sh`

**Tests**
- `tests/test_integration.py`
- `tests/test_evidence.py`
- `tests/test_claim_map.py`
- `tests/test_experiment_schema.py`
- `tests/test_routing.py`
- `tests/fixtures/` — fixture data
- `tests/expected/` — expected outputs

# Changelog

All notable changes to ARIS Engineering Robotics are documented here.

Format: [Semantic Versioning](https://semver.org/)

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

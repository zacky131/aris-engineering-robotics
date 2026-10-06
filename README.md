# ARIS Engineering Robotics

> **Research orchestration × robotics/control engineering × engineering paper skills — unified.**
> Supports **Codex CLI**, **Claude Code**, and **Google Antigravity**.

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

---

## What is this?

**ARIS Engineering Robotics** is an integration repository that combines the strongest capabilities of two sibling repositories:

| Source | Focus |
|---|---|
| [`Auto-claude-code-research-in-sleep`](../Auto-claude-code-research-in-sleep) (ARIS) | Research orchestration, literature, idea discovery, experiment planning, result-to-claim |
| [`engineering-paper-skills`](../engineering-paper-skills) (EPS) | Engineering-paper writing, auditing, evidence governance, reviewer response, submission validation |

It adds a new **Robotics / Control Research Layer** between them that neither upstream repository provides:

- ROS 2 / Gazebo / PX4 experiment lifecycle management
- Controller tuning and design-space exploration
- SIL / HIL evidence classification (L0–L6)
- Robotics-domain result analysis and metric catalogues
- Simulation integrity auditing
- Evidence ledger and claim-map governance artifacts

---

## Architecture

```
ARIS Research Layer
  research-lit · idea-discovery · novelty-check · experiment-plan
  research-implement-feature · paper-claim-audit · research-review · rebuttal
        │
        ▼
Robotics / Advanced Control Layer  (NEW — this repository)
  anchor-paper-intake · robotics-research-router · robotics-experiment-plan
  run-robotics-experiment · robotics-watchdog · controller-tuning
  vla-robotics · learning-control-eval · safety-filter-cbf
  robotics-result-analysis · robotics-experiment-audit · simulation-validation
  sil-hil-validation · robotics-result-to-claim · research-pipeline-robotics
        │
        ▼
Engineering Paper Layer
  engineering-writing · engineering-polishing · engineering-paper-auditor
  engineering-figure-table · engineering-response · engineering-validation
```

See [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md) and [`docs/VLA_AND_AI_CONTROL.md`](docs/VLA_AND_AI_CONTROL.md) for detailed architecture and paradigm standards.

---

## Supported Research Domains & Control Paradigms

- **Vision-Language-Action (VLA) & Embodied AI**: OpenVLA, Octo, RT-1, RT-2, π0, SmolVLA, ACT, Diffusion Policy, action chunking, temporal ensembling, SIMPLER Env, LIBERO, CALVIN, ManiSkill, workspace safety cages
- **Learning-Based Control**: Deep RL (PPO, SAC, TD3), offline RL (CQL, IQL), imitation learning, Sim-to-Real transfer, domain randomization, Rapid Motor Adaptation (RMA), multi-seed evaluation (IQM, 95% bootstrap CIs via rliable)
- **AI-Based & Physics-Informed Control**: Physics-informed neural networks (PINN), Neural ODEs, Neural MPC, Gaussian Process MPC (GP-MPC), Deep Koopman operators, residual RL
- **SOTA Safety Control & Formal Guarantees**: Control Barrier Functions (CBF), CLF-CBF, Quadratic Program (QP) safety shields, forward invariance verification, solver fallback gates
- **Classical Control**: PID, LQR, MPC, NMPC, SMC (sliding mode), adaptive control, H-infinity robust control
- **State Estimation**: Kalman filter (KF), EKF, UKF, IMM, particle filter, Moving Horizon Estimation (MHE)
- **Robotics Middleware & Autopilots**: ROS 2 (Nav2, SLAM, TF), PX4 UAV (SITL, offboard, MAVLink, uXRCE-DDS)
- **Multi-Robot Systems**: MARL (MAPPO, IPPO), swarm coordination, multi-UAV trajectory deconfliction

---

## Installation

ARIS Engineering Robotics supports three AI coding agent platforms:
- **Codex CLI** (OpenAI)
- **Claude Code** (Anthropic)
- **Google Antigravity** (Google DeepMind)

See [`docs/PLATFORM_COMPATIBILITY.md`](docs/PLATFORM_COMPATIBILITY.md) for a full capability matrix.

### Prerequisites

- Bash ≥ 4
- Python ≥ 3.9 (for validation scripts)
- One of: Codex CLI, Claude Code, Google Antigravity
- **100% Self-Contained**: All 53 research, robotics, and paper-writing skills are pre-bundled directly in `skills/` and `shared/` with zero external dependencies required!

### Optional — Sync with upstream repositories

```bash
bash tools/sync_upstreams.sh
```

All 53 skills are already bundled and ready to install immediately out-of-the-box. If you ever wish to fetch or synchronize future upstream updates from `Auto-claude-code-research-in-sleep` or `engineering-paper-skills`, `tools/sync_upstreams.sh` and `tools/bootstrap_upstreams.sh` can pull them.


### Project-Local Installation (Recommended)

To install all skills, shared references, agent rules, and workflows directly into your target research project:

#### Linux / macOS / WSL / Git Bash
```bash
# For Google Antigravity
bash tools/install_skills.sh --platform antigravity --project /path/to/my_robotics_project

# For OpenAI Codex CLI
bash tools/install_skills.sh --platform codex --project /path/to/my_robotics_project

# For Claude Code
bash tools/install_skills.sh --platform claude --project /path/to/my_robotics_project
```

#### Windows (PowerShell)
```powershell
# For Google Antigravity
powershell -ExecutionPolicy Bypass -File tools\install_skills.ps1 -Platform antigravity -Project C:\path\to\my_robotics_project

# For OpenAI Codex CLI
powershell -ExecutionPolicy Bypass -File tools\install_skills.ps1 -Platform codex -Project C:\path\to\my_robotics_project

# For Claude Code
powershell -ExecutionPolicy Bypass -File tools\install_skills.ps1 -Platform claude -Project C:\path\to\my_robotics_project
```

#### Windows / Cross-Platform (Python — CMD, PowerShell, Terminal)
```cmd
# For Google Antigravity
python tools\install_skills.py --platform antigravity --project C:\path\to\my_robotics_project

# For OpenAI Codex CLI
python tools\install_skills.py --platform codex --project C:\path\to\my_robotics_project

# For Claude Code
python tools\install_skills.py --platform claude --project C:\path\to\my_robotics_project
```

### User-Wide Installation (Global)

**Linux / macOS:**
```bash
bash tools/install_skills.sh --platform antigravity  # Antigravity (~/.gemini/config/skills)
bash tools/install_skills.sh --platform codex        # OpenAI Codex (~/.codex/skills)
bash tools/install_skills.sh --platform claude       # Claude Code (~/.claude/skills)
```

**Windows (PowerShell / Python):**
```powershell
# Using PowerShell
powershell -ExecutionPolicy Bypass -File tools\install_skills.ps1 -Platform antigravity
powershell -ExecutionPolicy Bypass -File tools\install_skills.ps1 -Platform codex
powershell -ExecutionPolicy Bypass -File tools\install_skills.ps1 -Platform claude

# Or using Python
python tools\install_skills.py --platform antigravity
python tools\install_skills.py --platform codex
python tools\install_skills.py --platform claude
```

> [!NOTE]
> For Google Antigravity, the installer configures `.agents/skills/`, creates/merges `.agents/AGENTS.md` safely, and registers Antigravity workflows in `.agents/workflows/`. See [`docs/ANTIGRAVITY.md`](docs/ANTIGRAVITY.md) for details.

### Validate installation

```bash
# Codex
python3 tools/validate_installation.py --platform codex

# Antigravity
python3 tools/validate_installation.py \
    --platform antigravity \
    --dest /path/to/project/.agents/skills \
    --project /path/to/project
```

### Dry run (no changes made)

```bash
bash tools/install_skills.sh --platform codex --dry-run
bash tools/install_skills.sh --platform antigravity --project /path --dry-run
```

### List available platforms and skills

```bash
bash tools/install_skills.sh --list-platforms
bash tools/install_skills.sh --list-skills
```

---

## Start Research from Anchor Papers

ARIS Engineering Robotics supports **Anchor-Paper-First Research**. Instead of beginning with broad, unstructured web search, you can ground the AI agent with specific baseline papers, competitor approaches, and benchmark datasets.

```bash
# 1. Initialize research project structure
bash tools/init_research_project.sh ~/my_uav_project

# 2. Place your anchor PDFs in category subfolders:
#    ~/my_uav_project/anchor_papers/foundational/
#    ~/my_uav_project/anchor_papers/closest_work/
#    ~/my_uav_project/anchor_papers/methodology/
#    ~/my_uav_project/anchor_papers/benchmark/
```

When anchor papers are present, the agent automatically executes **Stage 0 (`anchor-paper-intake`)** to generate:
- `research/ANCHOR_PAPER_INDEX.md` (structured paper extractions)
- `research/ANCHOR_PAPER_SYNTHESIS.md` (cross-paper comparison matrix)
- `research/ANCHOR_GAP_HYPOTHESES.md` (gap hypotheses marked `UNVERIFIED`)
- `research/LITERATURE_SEARCH_PLAN.md` (targeted citation queries)
- `research/RESEARCH_GAP_MAP.md` (gap lifecycle tracker)

> [!NOTE]
> Anchor-paper limitations are treated strictly as **hypotheses**, never as confirmed facts. Broad literature search and novelty verification independently confirm whether gaps remain unresolved in the state of the art.
> See [`docs/ANCHOR_PAPERS.md`](docs/ANCHOR_PAPERS.md) for full details.

---

## End-to-End Sample Prompt Workflow: ARIS to Engineering Paper

Below is an end-to-end prompt sequence demonstrating a complete research cycle — from user anchor papers and ARIS literature search to robotics experiment execution and a publication-ready IEEE/AIAA manuscript.

### Phase 0: Anchor Paper Intake & Grounding

**User Prompt:**
```text
I have initialized this project and placed 4 PDFs into anchor_papers/closest_work/ and anchor_papers/benchmark/.
Please inspect the anchor papers, extract their methods, baselines, and reported limitations, and build a literature search plan.
```

**Agent Action & Response:**
```text
1. Discovers PDFs: anchor_papers/closest_work/chen2024_nmpc_uav.pdf, etc.
2. Invokes: anchor-paper-intake
3. Generates:
   - research/ANCHOR_MANIFEST.yaml (hashes & IDs: AP001..AP004)
   - research/ANCHOR_PAPER_INDEX.md (method parameters, disturbance models, metrics)
   - research/ANCHOR_PAPER_SYNTHESIS.md (cross-paper comparison matrix)
   - research/ANCHOR_GAP_HYPOTHESES.md (G001: Adaptive IMM-MPC under rapid maneuvers; Status: UNVERIFIED)
   - research/LITERATURE_SEARCH_PLAN.md (seed citation queries)
```

---

### Phase 1: ARIS Literature Search & Novelty Verification

**User Prompt:**
```text
Now execute the literature search using research/LITERATURE_SEARCH_PLAN.md.
Verify whether gap hypothesis G001 has already been solved by recent 2024-2026 publications, and check novelty for our proposed adaptive-horizon IMM-MPC method.
```

**Agent Action & Response:**
```text
1. Invokes: research-lit (targeted backward/forward search from AP001 seeds)
2. Discovers recent competitor works (e.g. Wang et al., 2025)
3. Invokes: novelty-check
4. Updates: research/RESEARCH_GAP_MAP.md
   - G001 promoted: UNVERIFIED → SUPPORTED_AS_CURRENT_GAP
5. Invokes: research-refine (sharpens problem scope and non-claims)
6. Invokes: claims-drafting
   - Populates CLAIM_MAP.yaml with initial hypotheses:
     C001: "Reduces miss distance by >= 25% under target acceleration steps" (unsupported)
     C002: "Guarantees solver execution <= 15 ms at 50 Hz" (unsupported)
```

---

### Phase 2: Robotics Experiment Design & Execution

**User Prompt:**
```text
Use robotics-research-router to confirm our active profiles, then use robotics-experiment-plan to design our run matrix addressing Q1 (Performance), Q4 (Robustness), and Q5 (Computation).
```

**Agent Action & Response:**
```text
1. Invokes: robotics-research-router
   - Detected profiles: classical_control + px4_uav (HIGH confidence)
2. Invokes: robotics-experiment-plan (incorporates ANCHOR_PAPER_SYNTHESIS.md baselines)
   - Matrix generated:
     * EXP001: Proposed IMM-MPC vs Baseline NMPC (AP001) under step maneuvers (MUST_RUN -> C001)
     * EXP002: Wind gust robustness sweep 0-3 m/s (MUST_RUN -> C001)
     * EXP003: Real-time execution profile on companion computer SITL (MUST_RUN -> C002)
   - Drafts EXPERIMENT.yaml for EXP001..EXP003
```

**User Prompt:**
```text
Run experiment EXP001 in PX4 Gazebo SITL and monitor execution with the watchdog.
```

**Agent Action & Response:**
```text
1. Invokes: run-robotics-experiment (checks HARDWARE_GATE: SITL approved)
2. Invokes: robotics-watchdog (monitors ROS 2 topic rates, divergence, real-time factor >= 0.95)
3. Experiment completes: logs captured to results/exp001_raw.csv
```

---

### Phase 3: Result Analysis, Evidence Audit & Claim Governance

**User Prompt:**
```text
Analyze the simulation results, run the robotics experiment audit, and update our evidence ledger and claim map.
```

**Agent Action & Response:**
```text
1. Invokes: robotics-result-analysis
   - Calculates miss distance (mean, 95th percentile) and solve time
   - Outputs RESULT_SUMMARY.yaml
2. Invokes: robotics-experiment-audit
   - Confirms baseline fairness, seed counts, and simulation validity (L3 SIL)
3. Invokes: robotics-result-to-claim
   - Appends verified record to EVIDENCE_LEDGER.yaml
   - Updates CLAIM_MAP.yaml:
     C001: status promoted to "supported" (Evidence Level: L3)
     C002: status promoted to "supported" (Evidence Level: L3)
```

---

### Phase 4: Engineering Paper Writing & Verification

**User Prompt:**
```text
We have verified evidence for C001 and C002. Use engineering-paper-auditor to check our paper story spine, then use engineering-writing and engineering-figure-table to draft Section IV (Results).
```

**Agent Action & Response:**
```text
1. Invokes: engineering-paper-auditor
   - Validates story spine: problem -> gap -> method -> evidence -> boundary
   - Ensures no claim exceeds L3 (simulation) to real-world overclaiming
2. Invokes: engineering-writing
   - Drafts Section IV with calibrated claims linked to EXP001-EXP003
3. Invokes: engineering-figure-table
   - Generates trajectory plots and comparison tables tracing directly to results/
4. Invokes: engineering-polishing
   - Refines control terminology, transitions, and mathematical notation
5. Invokes: engineering-validation
   - Verifies target venue requirements (IEEE Transactions / ICRA format)
```

---

## Quick Start

See [`docs/QUICKSTART.md`](docs/QUICKSTART.md) for additional walkthroughs.

### Quick Workflow Overview (Command Summary)

```
1. Initialize: bash tools/init_research_project.sh ./my_project
2. Add PDFs:   cp *.pdf ./my_project/anchor_papers/closest_work/
3. Open Codex / Claude / Antigravity in your project directory
4. Stage 0:    Call anchor-paper-intake
5. Stage 1-4:  Call research-lit & novelty-check
6. Stage 5-6:  Call research-refine & claims-drafting
7. Stage 7:    Call robotics-research-router & robotics-experiment-plan
8. Stage 8-10: Call run-robotics-experiment & robotics-watchdog
9. Stage 11-13:Call robotics-result-analysis, robotics-experiment-audit, robotics-result-to-claim
10. Stage 14+: Call engineering-paper-auditor, engineering-writing, engineering-validation
```

## Usage Instructions

### How to Use This System

This integration exposes its capabilities as **skills** — plain-Markdown instruction files
loaded by your AI coding agent (Codex CLI or Claude Code).

#### Step 1 — Install skills

Run the installer once:

```bash
bash tools/install_skills.sh --platform codex
```

This places skill files into `~/.codex/skills/` (user-wide) or `.codex/skills/` (project-local).

#### Step 2 — Open your AI agent in your research project

Navigate to your robotics research project in VS Code / terminal, then open Codex or Claude.

#### Step 3 — Call skills by name

In the agent chat, reference a skill by its directory name:

```
Use the robotics-research-router skill to classify my research context.
```

```
Use the robotics-experiment-plan skill to design an MPC robustness experiment.
```

```
Use the vla-robotics skill to evaluate OpenVLA on the LIBERO benchmark with action chunking and a safety bounding box.
```

```
Use the learning-control-eval skill to analyze PPO quadruped sim-to-real transfer across 10 random seeds using IQM and 95% bootstrap CIs.
```

```
Use the safety-filter-cbf skill to formulate a CBF-QP safety shield guaranteeing forward invariance.
```

```
Use the robotics-result-to-claim skill to convert my simulation results to claims.
```

```
Use the engineering-writing skill to draft the Results section.
```

#### Step 4 — Use the evidence artifacts

Your research project should maintain:

- `EXPERIMENT.yaml` — per-experiment configuration
- `EVIDENCE_LEDGER.yaml` — all verified result records
- `CLAIM_MAP.yaml` — link claims to evidence
- `RESULT_SUMMARY.yaml` — summary of each experiment run

Copy templates from [`templates/`](templates/) to get started.

#### Step 5 — Validate before writing

Always run the experiment audit and result-to-claim skills before drafting manuscript sections.
This prevents inflated claims.

---

## Evidence and Claim Governance

The integration enforces a strict evidence model.

Evidence levels:

| Level | Type |
|---|---|
| L0 | Theoretical / analytical |
| L1 | Numerical simulation |
| L2 | Physics simulation (Gazebo, etc.) |
| L3 | Software-in-the-loop (SIL) |
| L4 | Hardware-in-the-loop (HIL) |
| L5 | Controlled physical experiment |
| L6 | Operational / field environment |

Claims may not exceed the level of evidence produced.

See [`docs/EVIDENCE_MODEL.md`](docs/EVIDENCE_MODEL.md) for details.

---

## Limitations

- Physical robot actuation always requires explicit human approval. The framework prepares commands but does not autonomously arm or move real robots.
- GPU-accelerated training is not the default experiment backend. Use ARIS `vast-gpu` or `serverless-modal` directly if needed.
- The installer assumes upstream repos are peer siblings unless the config file is edited.
- SIL/HIL automation requires a working local ROS 2 / Gazebo / PX4 installation.
- Real-time factor tracking requires the experiment runner to capture timing data.

---

## Attribution

- **ARIS / Auto-claude-code-research-in-sleep** — © 2026 wanshuiyin. MIT License.
- **engineering-paper-skills** — © 2026 Engineering Paper Skills contributors. MIT License. Includes adapted material from phd-writing (© 2026 Yuqi Cheng, MIT).

See [`NOTICE.md`](NOTICE.md) for full third-party notices.

---

## License

MIT — see [`LICENSE`](LICENSE).

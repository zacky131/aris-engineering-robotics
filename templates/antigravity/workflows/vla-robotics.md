# Workflow: Vision-Language-Action (VLA) Robotics

**Purpose**: Guide a rigorous Vision-Language-Action and Embodied AI research workflow from model selection to simulated benchmark evaluation and safety-gated hardware deployment.

**Invoke with**: A VLA research topic or instruction, e.g.:
```
/vla-robotics "Evaluate OpenVLA on LIBERO-Spatial with CBF safety filter"
```
or natural language:
```
Run the vla-robotics workflow for our language-conditioned manipulation policy.
```

---

## Stage 1 — Model & Environment Inspection

**Skill**: `vla-robotics`
- Confirm model weights / checkpoint (OpenVLA, Octo, RT-1/2, π0, SmolVLA, ACT, Diffusion Policy).
- Confirm observation space: RGB camera views (wrist + over-the-shoulder), proprioception, language prompt encoding.
- Select target benchmark environment: SIMPLER Env (WidowX / Google Robot), LIBERO, CALVIN, ManiSkill, or RoboSuite.

## Stage 2 — Routing & Profile Activation

**Skill**: `robotics-research-router`
- Classify into `vla_robotics` and determine if safety shield is needed (`safe_sota_control`).
- Load active shared rules: `shared/vla-standards.md`, `shared/safety-cbf-standards.md`.

## Stage 3 — Experiment Design across Generalization Axes

**Skill**: `robotics-experiment-plan`
- Design evaluation matrix covering:
  1. In-Distribution (ID) task performance.
  2. Out-of-Distribution Visual (OOD-V): novel textures, lighting, distractors.
  3. Out-of-Distribution Spatial (OOD-S): novel 3D object positions/rotations.
  4. Out-of-Distribution Language (OOD-L): paraphrased synonyms, novel goals.
- Generate `VLA_EVALUATION.yaml`.

## Stage 4 — Action Chunking & Execution Setup

**Skill**: `vla-robotics`
- Configure prediction horizon $H$ (e.g. 16 steps) and temporal ensembling.
- Decouple frequencies: 5–10 Hz high-level VLA policy with 100–500 Hz low-level Cartesian/joint impedance controller.

## Stage 5 — Configure Safety Shield (CBF / Virtual Cage)

**Skill**: `safety-filter-cbf`
- Set workspace Cartesian bounding box: $p_{\text{EEF}} \in [x_{\min}, x_{\max}] \times [y_{\min}, y_{\max}] \times [z_{\min}, z_{\max}]$.
- Set velocity clamping limits: $\|\Delta p\| \le v_{\max} \Delta t$.
- If `safe_sota_control` active, configure real-time QP barrier filter to enforce obstacle clearance.

## Stage 6 — Rollout Execution & Watchdog Monitoring

**Skill**: `robotics-watchdog`
- Monitor policy inference latency per step (flag if $t_{\text{inf}} > \Delta t_{\text{budget}}$).
- Monitor camera streams (flag frozen frames, black frames, or ROS lag).
- Monitor safety shield QP feasibility and cage boundary clamps.

## Stage 7 — Result & Failure Analysis

**Skill**: `robotics-result-analysis`
- Compute task success rate, subtask progression rate, trajectory jerk, and mean inference latency.
- Break down failure modes: perceptual grounding miss vs grasp miss vs boundary violation vs timeout.

## Stage 8 — Experiment Audit & Claim Map

**Skills**: `robotics-experiment-audit` → `robotics-result-to-claim`
- Verify evaluation prompts are disjoint from training demonstrations.
- Audit that visual OOD degradation is explicitly documented.
- Record verified evidence in `EVIDENCE_LEDGER.yaml` and calibrate claims in `CLAIM_MAP.yaml`.

---

## Output

Produce:
1. `VLA_EVALUATION.yaml` configuration.
2. Rollout telemetry logs and failure mode breakdown.
3. Updated `EVIDENCE_LEDGER.yaml` and `CLAIM_MAP.yaml`.

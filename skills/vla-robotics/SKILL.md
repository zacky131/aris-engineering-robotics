---
name: vla-robotics
description: >
  Orchestrate, evaluate, and benchmark Vision-Language-Action (VLA) foundation models
  and embodied AI policies (OpenVLA, Octo, RT-1/2, pi0, SmolVLA, ACT, Diffusion Policy).
  Handles multimodal observation formatting, action chunking execution, latency budgeting,
  frequency decoupling, and physical workspace safety gating.
platforms:
  - codex
  - claude
  - antigravity
---

# Skill: vla-robotics

## Purpose

Guide the systematic research, evaluation, and physical deployment of **Vision-Language-Action (VLA)** models and multimodal robotic policies.

VLA models map continuous sensory observations (RGB cameras, proprioception) and natural language goals directly into low-level robotic action sequences:
$$\pi_{\text{VLA}}: (\mathbf{I}_{\text{RGB}}, \mathbf{q}_{\text{proprio}}, \mathcal{T}_{\text{lang}}) \mapsto \mathbf{A}_{t:t+H}$$

---

## Instructions

### Step 1 — Verify Model & Input-Output Specifications

Identify and document:
1. **Model Architecture**:
   - VLA Foundation: OpenVLA (Prismatic VLM 7B), Octo, RT-1, RT-2, π0, SmolVLA
   - Action Chunking Policy: ACT (Action Chunking with Transformers), Diffusion Policy, Flow Matching
2. **Observation Space**:
   - Primary Camera: Resolution (e.g. 224×224, 256×256), frame rate, placement (static third-person or over-the-shoulder).
   - Wrist Camera: Gripper-centric view for fine alignment.
   - Proprioception: Joint angles $q \in \mathbb{R}^N$ or Cartesian EEF pose $p \in \mathrm{SE}(3)$.
   - Language Goal: Free-form text string, tokenized via tokenizer (e.g., Llama/T5/Gemma).
3. **Action Space & Chunk Horizon**:
   - Prediction horizon $H$ (typically 8 to 64 steps).
   - Action type: EEF $\Delta$ position $[dx, dy, dz]$, rotation $[d\phi, d\theta, d\psi]$, and binary/continuous gripper state.

### Step 2 — Environment & Benchmark Selection

Select and configure the evaluation benchmark:
- **SIMPLER Env**: Evaluates generalizable VLA policies on real-to-sim digital twins of Google Robot and WidowX manipulators.
- **LIBERO**: 130 standardized tasks across 4 suites (`LIBERO-Spatial`, `LIBERO-Object`, `LIBERO-Goal`, `LIBERO-100`).
- **CALVIN**: Long-horizon multi-task language-conditioned manipulation (34 tasks, 1000+ chain sequences).
- **ManiSkill / RoboSuite**: Precise contact-rich physics manipulation in SAPIEN or MuJoCo.
- **Isaac Lab**: Massively parallel GPU-accelerated visual rollouts.

### Step 3 — Curate Evaluation Matrix (Generalization Axes)

Do not test only on in-distribution configurations. Define evaluation sets across 4 axes:
1. **In-Distribution (ID)**: Exact training object assets, textures, and prompt phrases.
2. **Visual Novelty (OOD-V)**: Unseen tablecloth colors, novel distractor objects, ambient lighting shifts.
3. **Spatial Shift (OOD-S)**: Objects placed at previously unseen workspace coordinates or rotations.
4. **Semantic Paraphrasing (OOD-L)**: Synonymous rephrasings (e.g., "pick up the red mug" vs "grasp the crimson cup").

### Step 4 — Configure Execution & Frequency Decoupling

1. **Temporal Ensembling**:
   Compute executed action $a_t$ at step $t$ using exponential decay weighting across active overlapping chunks:
   $$a_t = \frac{\sum_{i=1}^{\min(t, H)} w_i A_{t-i+1, i}}{\sum_{i=1}^{\min(t, H)} w_i}, \quad w_i = \exp(-m \cdot i)$$
2. **Frequency Decoupling**:
   - Run VLA inference at $5 \text{--} 10 \text{ Hz}$.
   - Interpolate chunk trajectories via minimum-jerk splines to feed the low-level controller at $100 \text{--} 500 \text{ Hz}$.

### Step 5 — Enforce Workspace Safety Gates

Before rollouts commence:
1. **Virtual Cage (Bounding Box)**:
   $$\mathbf{p}_{\text{EEF}} \in [x_{\min}, x_{\max}] \times [y_{\min}, y_{\max}] \times [z_{\min}, z_{\max}]$$
   Clamp any commanded step exceeding these bounds.
2. **Action Delta Clipping**:
   $$\|\Delta \mathbf{p}\|_\infty \le v_{\max} \cdot \Delta t$$
3. **Out-of-Distribution Anomaly Watchdog**:
   If visual feature reconstruction loss or model uncertainty exceeds the threshold, trigger slow-down or pause.

### Step 6 — Result & Failure Analysis Reporting

Produce structured evaluation summary:

```yaml
vla_evaluation_report:
  model_id: "openvla-7b-finetuned-libero"
  benchmark: "LIBERO-Spatial"
  total_trials: 100
  overall_success_rate: 0.82
  breakdown_by_axis:
    in_distribution: 0.94
    visual_ood: 0.80
    spatial_ood: 0.76
    language_ood: 0.78
  failure_modes:
    perceptual_grounding_failure: 6
    grasp_execution_miss: 8
    boundary_clamp_intervention: 4
    timeout: 0
  latency:
    mean_inference_time_ms: 112.4
    p95_inference_time_ms: 128.0
    control_loop_jitter_ms: 1.2
```

---

## Constraints

- Never evaluate on training demonstrations or training seed layouts.
- Report both full success and intermediate subtask milestones.
- Real hardware deployment must have human supervisory emergency stop enabled.

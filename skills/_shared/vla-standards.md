# Shared Rule: Vision-Language-Action (VLA) Standards

## 1. Scope & Purpose

This document governs research involving **Vision-Language-Action (VLA)** models, multimodal embodied AI policies, and end-to-end sensorimotor manipulation and navigation (e.g., OpenVLA, Octo, RT-1, RT-2, π0, SmolVLA, ACT, Diffusion Policy).

---

## 2. Model & Action Architecture Standards

### 2.1 Action Representation & Chunking
- **Action Chunking**: VLA models predict horizons of actions $A_{t:t+H} \in \mathbb{R}^{H \times D}$ where $H \in [8, 64]$ to avoid high-frequency compounding errors.
- **Action Frame**: Explicitly specify the action frame:
  - `tool_frame_cartesian_delta` ($\Delta x, \Delta y, \Delta z, \Delta \text{roll}, \Delta \text{pitch}, \Delta \text{yaw}, \text{gripper}$)
  - `base_frame_cartesian_delta`
  - `joint_position_delta` ($\Delta q \in \mathbb{R}^N$)
- **Temporal Ensembling**: When deploying overlapping chunks at timestep $t$, use exponential or linear weighting across predictions from past timesteps to smooth trajectories.

### 2.2 Frequency Decoupling
- VLA models run at lower inference frequencies ($f_{\text{VLA}} \approx 5 \text{--} 10 \text{ Hz}$).
- Robot execution must run at higher control frequencies ($f_{\text{ctrl}} \approx 100 \text{--} 500 \text{ Hz}$) via:
  - Cubic spline or minimum-jerk action chunk interpolation.
  - Low-level joint position/velocity impedance controllers.

---

## 3. Evaluation & Generalization Protocols

Every VLA paper or experiment must report results across systematically isolated generalization axes:

| Evaluation Axis | Definition | Requirement |
|---|---|---|
| **In-Distribution (ID)** | Seen training scenes, objects, lighting, and language prompts | Report baseline task success rate |
| **Visual Unseen (OOD-V)** | Novel object textures, background distractors, varying lighting | Test robustness to perceptual shifts |
| **Spatial Generalization (OOD-S)** | Novel object positions, rotated orientations, unseen table heights | Test 3D spatial grounding |
| **Language Generalization (OOD-L)** | Paraphrased synonyms, novel instruction combinations, unseen goals | Test semantic grounding |

### Prohibited Evaluation Practices:
1. **Never test on training episode demonstrations or exact seed initializations.**
2. **Never cherry-pick camera angles**: Fix camera intrinsic and extrinsic calibrations and document mounting offsets.
3. **Do not report only binary completion**: Log subtask progression (e.g. 1/3 grasp, 2/3 lift, 3/3 place) to pinpoint failure modes.

---

## 4. Hardware Safety Gates for Physical VLA Deployment

When deploying VLA models onto physical robot arms or mobile manipulators:

1. **Workspace Virtual Cage (Bounding Box)**:
   - Define hard Cartesian limits: $x \in [x_{\min}, x_{\max}]$, $y \in [y_{\min}, y_{\max}]$, $z \in [z_{\min}, z_{\max}]$.
   - Clamping rule: If VLA policy commands an EEF pose outside this cage, the action is projected onto the boundary and flagged.
2. **Maximum Delta Velocity Limit**:
   - Clamp $\|\Delta p\|_{\infty} \le v_{\max} \cdot \Delta t$ to prevent sudden erratic jerks caused by visual attention hallucinations.
3. **E-Stop & Human Supervisor**:
   - Software and physical emergency stops must be active throughout all rollouts.
4. **Collision & Force Torque Guard**:
   - If end-effector torque or external force exceeds threshold ($F_{\text{ext}} > F_{\text{limit}}$), trigger immediate impedance release or safety stop.

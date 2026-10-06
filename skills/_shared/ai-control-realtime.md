# Shared Rule: AI-Based Control & Real-Time Guarantees

## 1. Scope & Purpose

This document governs research utilizing **AI-driven dynamic models** (Neural ODEs, Physics-Informed Neural Networks / PINNs, Gaussian Processes) and **Hybrid AI-Control** (Neural MPC, Residual Control).

---

## 2. Physics-Informed Constraints (PINNs & Neural ODEs)

1. **Physical Conservation Compliance**:
   - Neural models parameterizing physical dynamics $\dot{x} = f_\theta(x, u)$ must report conservation error metrics:
     - Energy conservation: $\left|\frac{d}{dt} E(x) - P_{\text{input}}\right|$
     - Skew-symmetry / passivity constraints: $x^T (M(q)\ddot{q} + C(q,\dot{q})\dot{q}) \le 0$
2. **Multi-Step Rollout Stability**:
   - Do not report single-step prediction loss ($L_1/L_2$ on $\hat{x}_{t+1}$) alone.
   - Must evaluate open-loop and closed-loop prediction divergence over a horizon of at least $H \ge 20 \text{--} 50$ steps to detect error accumulation and state drift.

---

## 3. Real-Time Worst-Case Execution Time (WCET)

In continuous robotics control (e.g. 50 Hz – 1 kHz), neural network evaluation must not block the control loop:

1. **Inference Latency Budget**:
   - Control Loop Frequency $f_{\text{ctrl}} = 100\text{ Hz} \implies \text{Loop Deadline} = 10.0\text{ ms}$.
   - Neural Network Inference Budget $\le 5.0\text{ ms}$ (leaving 5 ms for state estimation, communication, and actuator write).
2. **Deployment Acceleration**:
   - Standard PyTorch runtime is prohibited for hard real-time execution.
   - Use compiled backends: **TensorRT**, **ONNX Runtime (with CUDA/TensorRT execution provider)**, or **TorchScript C++ libtorch**.
3. **Deterministic Classical Fallback**:
   - If neural inference exceeds the allocated deadline (or crashes due to GPU timeout), the control loop must deterministically trigger a safety fallback to a nominal baseline (e.g., LQR, PD, or standard linear MPC) without causing actuator dropout.

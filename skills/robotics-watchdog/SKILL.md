---
name: robotics-watchdog
description: >
  Monitor the health of a running robotics experiment. Detects process failures,
  ROS topic issues, Gazebo/PX4 connectivity, timing problems, estimator faults,
  and logging failures. Only manages PIDs started by run-robotics-experiment.
platforms:
  - codex
  - claude
  - antigravity
---

# Skill: robotics-watchdog

## Purpose

Monitor a running robotics experiment for health issues and detect failure categories
before they silently corrupt results. Adapted from ARIS `monitor-experiment` for
robotics-specific checks.

## Failure Categories

| Category | Trigger examples |
|---|---|
| `PROCESS_FAILURE` | Required process not in process list |
| `SENSOR_FAILURE` | Topic not publishing, stale timestamp |
| `ESTIMATOR_FAILURE` | NaN / Inf in state estimate, diverged covariance |
| `CONTROL_FAILURE` | Controller not publishing, actuator fully saturated |
| `TIMING_FAILURE` | Deadline misses, RTF below threshold, sim clock stalled |
| `SCENARIO_FAILURE` | Collision, geofence breach, mission timeout |
| `LOGGING_FAILURE` | Rosbag not recording, log file not growing |

## Instructions

### Step 1 — Load experiment context

Read:
- `EXPERIMENT.yaml` for expected processes, topics, timing requirements
- Active profile from `robotics-research-router`
- `platform.middleware` and `platform.simulator`

### Step 2 — Build check list

Select applicable checks from the master check list:

#### Process checks
```
□ Required simulation process alive (Gazebo, SITL)
□ Required ROS 2 nodes alive (ros2 node list)
□ Experiment script / controller process alive
□ Rosbag record process alive (if logging.rosbag == true)
```

#### Topic / communication checks
```
□ Key topics publishing (ros2 topic hz)
□ Topic frequency within expected range ± 20%
□ TF available (ros2 run tf2_ros tf2_echo)
□ PX4 heartbeat / offboard setpoint receiving
```

#### State / estimation checks
```
□ State estimate not NaN / Inf
□ Covariance bounded
□ Innovation within expected range
```

#### Control checks
```
□ Control output not fully saturated (all repetitions)
□ MPC solver returning feasible solution
□ Solver time below control period (p99)
```

#### Timing checks
```
□ Simulation clock progressing (not stalled)
□ Real-time factor ≥ threshold (default: RTF ≥ 0.9 for SIL)
□ Controller deadline misses ≤ threshold
```

#### Scenario checks
```
□ No collision (if collision detection enabled)
□ Mission not timed out
□ Scenario goal conditions progressing
```

#### Logging checks
```
□ Rosbag file size growing
□ CSV log file size growing
□ No write errors in stdout/stderr
```

### Step 3 — Classify detected issues

For each detected issue:
```yaml
issue:
  category: TIMING_FAILURE
  description: "Real-time factor dropped to 0.61 (threshold 0.90)"
  severity: WARNING  # WARNING | ERROR | CRITICAL
  recommended_action: "Reduce simulation complexity or increase control period"
  auto_fixable: false
```

### Step 4 — Take action based on severity

| Severity | Action |
|---|---|
| `WARNING` | Log and continue monitoring |
| `ERROR` | Log, alert user, continue unless safety-critical |
| `CRITICAL` | Log, alert user, recommend stopping experiment |

**Never automatically kill processes not started by `run-robotics-experiment`.**

### Step 5 — Report

```yaml
watchdog_report:
  experiment_id: EXP001
  check_time: "2026-09-30T17:00:00+09:00"
  overall_status: HEALTHY  # HEALTHY | DEGRADED | FAILED
  issues: []
  metrics_snapshot:
    rtf: 0.98
    controller_deadline_misses: 0
    topic_hz_cmd_vel: 50.1
    estimator_nan: false
```

## Constraints

- Only manage PIDs tracked by `run-robotics-experiment`.
- Never kill unrelated user processes.
- Do not modify simulator configuration during a run.
- If CRITICAL failure detected and platform.type == real: immediately alert user and stop checks.

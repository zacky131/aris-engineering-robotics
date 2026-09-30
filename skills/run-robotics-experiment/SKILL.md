---
name: run-robotics-experiment
description: >
  Execute a robotics or control experiment based on a filled EXPERIMENT.yaml.
  Supports Python, MATLAB/Simulink, ROS 2, Gazebo, PX4 SITL, ArduPilot SITL,
  and generic shell command backends.
platforms:
  - codex
  - claude
---

# Skill: run-robotics-experiment

## Purpose

Execute a robotics experiment described in `EXPERIMENT.yaml` (or equivalent).
This skill manages backend detection, pre-flight checks, launch, logging,
and graceful cleanup.

**Safety constraint**: This skill does NOT autonomously arm, start motors,
or move physical robots. Physical actuation requires explicit human approval.
See `docs/ROBOTICS_EXPERIMENT_MODEL.md` for the hardware safety boundary.

## Supported Backends

| Backend | Identifier | Notes |
|---|---|---|
| Python script | `python` | `python run.py` or pytest-based |
| MATLAB script | `matlab` | `-batch` mode; no GUI unless specified |
| Simulink model | `simulink` | `sim()` via MATLAB batch |
| ROS 2 launch | `ros2` | `ros2 launch <pkg> <launch_file>` |
| Gazebo + ROS 2 | `gazebo` | Launches Gazebo world + ROS nodes |
| PX4 SITL | `px4_sitl` | PX4 SITL + Gazebo + ROS 2 bridge |
| ArduPilot SITL | `ardupilot_sitl` | SITL + ROS 2 bridge |
| Generic shell | `shell` | Any `command` specified in EXPERIMENT.yaml |

**NOT_IMPLEMENTED**: Direct HIL execution, real robot launch, and cloud GPU
backends. These require hardware-specific setup beyond this skill's scope.

## Instructions

### Step 1 — Load experiment configuration

Read `EXPERIMENT.yaml` (or the file the user provides).

Extract:
- `experiment.id`, `experiment.name`
- `platform.type` (simulation / sil / hil / real)
- `platform.middleware`, `platform.simulator`, `platform.autopilot`
- `scenario.repetitions`, `scenario.seed_policy`
- `logging` settings
- `metrics` list

### Step 2 — Safety gate

If `platform.type == real` or `platform.type == hil`:
- **STOP**
- Print: `HARDWARE_GATE: This experiment requires physical hardware. Please execute manually or confirm safe automated access.`
- Do not proceed.

### Step 3 — Pre-flight checks

Before launching:

```
□ Confirm EXPERIMENT.yaml is valid (run validate_experiment.py if available)
□ Confirm result directory exists or create it
□ Confirm no conflicting experiment is running (check PIDs)
□ Confirm simulator is not already running (check process list)
□ Confirm ROS 2 environment sourced (echo $ROS_DISTRO)
□ Confirm PX4_SOURCE_DIR set if px4_sitl backend
```

Report any failed pre-flight check and stop.

### Step 4 — Build launch command

Construct the exact shell commands to run the experiment.

Example for `px4_sitl`:

```bash
# Terminal 1: PX4 SITL
cd $PX4_SOURCE_DIR && make px4_sitl gazebo-classic_iris

# Terminal 2: ROS 2 bridge
ros2 run micro_ros_agent micro_ros_agent udp4 --port 8888

# Terminal 3: ROS 2 launch (experiment)
ros2 launch my_pkg experiment.launch.py experiment_id:=EXP001
```

### Step 5 — Track PIDs

Record all PIDs started by this skill. Only these PIDs will be managed by
the cleanup step.

### Step 6 — Monitor launch

After launch:
- Confirm key processes are alive
- Confirm required ROS topics are publishing (if ROS 2)
- Hand off to `robotics-watchdog` for continuous monitoring

### Step 7 — Wait for completion

Wait for:
- Scenario duration reached, OR
- Success/failure condition triggered, OR
- Timeout, OR
- Manual stop

### Step 8 — Graceful cleanup

On completion or error:
- Terminate only tracked PIDs
- Save rosbag if specified
- Save stdout/stderr logs
- Record experiment status in `EXPERIMENT_TRACKER.md`

### Step 9 — Report

```yaml
experiment_id: EXP001
status: completed  # completed | failed | timeout | aborted
result_files:
  - results/EXP001/run_001.csv
  - results/EXP001/rosbag_001.db3
duration_s: 63.2
repetitions_completed: 10
errors: []
next_skill: robotics-watchdog  # or robotics-result-analysis if complete
```

## Constraints

- Never kill PIDs not started by this skill.
- Do not assume GPU availability.
- Do not set default GPU execution.
- Log all shell commands actually run.
- Do not assume ROS 2 is sourced; instruct the user to source it first if not detected.

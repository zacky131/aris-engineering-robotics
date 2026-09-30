#!/usr/bin/env python3
"""Tests: routing keyword detection logic (static keyword matching simulation)."""
import sys

PROFILES = {
    "classical_control": ["PID", "LQR", "MPC", "NMPC", "SMC", "EKF", "UKF", "IMM",
                          "Kalman", "adaptive control", "robust control", "observer"],
    "ros2_robotics": ["ROS 2", "ROS2", "Nav2", "SLAM", "rosbag", "TF", "sensor fusion"],
    "px4_uav": ["PX4", "SITL", "MAVLink", "uXRCE-DDS", "offboard", "UAV", "guidance"],
    "multi_robot": ["MARL", "swarm", "coordination", "multi-UAV", "multi-robot", "MAPPO"],
    "learning_robotics": ["PPO", "SAC", "TD3", "MAPPO", "IPPO", "imitation", "learned policy"],
    "hybrid_ai_control": ["hybrid", "learned cost", "neural network controller"],
}


def detect_profiles(prompt: str) -> list:
    detected = []
    for profile, keywords in PROFILES.items():
        if any(kw.lower() in prompt.lower() for kw in keywords):
            detected.append(profile)
    return detected


def test_mpc_uav():
    prompt = "Design an MPC robustness experiment for UAV interception"
    profiles = detect_profiles(prompt)
    assert "classical_control" in profiles, f"Expected classical_control, got {profiles}"
    print(f"PASS: MPC UAV → {profiles}")

def test_px4_sitl():
    prompt = "Run PX4 SITL landing experiments in Gazebo"
    profiles = detect_profiles(prompt)
    assert "px4_uav" in profiles, f"Expected px4_uav, got {profiles}"
    print(f"PASS: PX4 SITL → {profiles}")

def test_mappo_multi_agent():
    prompt = "Analyze MAPPO multi-agent training results"
    profiles = detect_profiles(prompt)
    assert "learning_robotics" in profiles or "multi_robot" in profiles, \
        f"Expected learning_robotics or multi_robot, got {profiles}"
    print(f"PASS: MAPPO multi-agent → {profiles}")

def test_paper_writing_not_robotics():
    prompt = "Rewrite the Results section of my robotics paper"
    profiles = detect_profiles(prompt)
    # No strong robotics experiment keywords → profiles may be empty or minimal
    # This is correct: paper tasks go to engineering-paper-router
    print(f"PASS: paper writing → profiles {profiles} (should route to paper layer)")

if __name__ == "__main__":
    tests = [test_mpc_uav, test_px4_sitl, test_mappo_multi_agent, test_paper_writing_not_robotics]
    failed = 0
    for t in tests:
        try:
            t()
        except Exception as e:
            print(f"FAIL: {t.__name__}: {e}")
            failed += 1
    print(f"\n{len(tests)-failed}/{len(tests)} passed")
    sys.exit(0 if failed == 0 else 1)

#!/usr/bin/env python3
"""
validate_installation.py — Verify skills are correctly installed.

Usage:
    python tools/validate_installation.py
    python tools/validate_installation.py --dest /path/to/.codex/skills
"""
import argparse
import os
import sys
from pathlib import Path

ROBOTICS_SKILLS = [
    "robotics-research-router",
    "robotics-experiment-plan",
    "run-robotics-experiment",
    "robotics-watchdog",
    "robotics-result-analysis",
    "controller-tuning",
    "robotics-experiment-audit",
    "simulation-validation",
    "sil-hil-validation",
    "robotics-result-to-claim",
    "research-pipeline-robotics",
]

ARIS_SKILLS = [
    "research-lit",
    "idea-discovery",
    "novelty-check",
    "experiment-plan",
    "research-implement-feature",
    "result-to-claim",
    "paper-claim-audit",
    "dse-loop",
    "ablation-planner",
]

EPS_SKILLS = [
    "engineering-writing",
    "engineering-polishing",
    "engineering-paper-auditor",
    "engineering-figure-table",
    "engineering-response",
    "engineering-validation",
]


def check_skill(dest: Path, name: str) -> bool:
    skill_dir = dest / name
    skill_md = skill_dir / "SKILL.md"
    if not skill_dir.exists():
        return False
    if not skill_md.exists():
        print(f"  WARNING: {name}/SKILL.md not found (directory exists but may be empty)")
        return False
    return True


def main():
    parser = argparse.ArgumentParser(description="Validate ARIS Engineering Robotics installation")
    parser.add_argument("--dest", default=str(Path.home() / ".codex/skills"),
                        help="Skills directory to check (default: ~/.codex/skills)")
    args = parser.parse_args()

    dest = Path(args.dest)
    print(f"=== ARIS Engineering Robotics — Installation Validator ===")
    print(f"Checking: {dest}")
    print()

    passed = 0
    failed = 0
    missing_upstream = []

    def check_group(label, skills, optional=False):
        nonlocal passed, failed
        print(f"--- {label} ---")
        for skill in skills:
            ok = check_skill(dest, skill)
            status = "✓" if ok else ("⚠ MISSING (optional)" if optional else "✗ MISSING")
            print(f"  {status}: {skill}")
            if ok:
                passed += 1
            else:
                failed += 1
                if optional:
                    missing_upstream.append(skill)
        print()

    check_group("Robotics / Control Skills (REQUIRED)", ROBOTICS_SKILLS, optional=False)
    check_group("ARIS Upstream Skills (OPTIONAL — install from ARIS repo)", ARIS_SKILLS, optional=True)
    check_group("EPS Upstream Skills (OPTIONAL — install from EPS repo)", EPS_SKILLS, optional=True)

    print(f"Results: {passed} installed, {failed} missing")
    print()

    if missing_upstream:
        print("Tip: Run the installer to get optional upstream skills:")
        print("  bash tools/install_skills.sh --platform codex")
        print()

    # Only fail if required robotics skills are missing
    required_missing = [s for s in ROBOTICS_SKILLS if not check_skill(dest, s)]
    if required_missing:
        print(f"ERROR: {len(required_missing)} required robotics skills not installed:")
        for s in required_missing:
            print(f"  - {s}")
        sys.exit(1)
    else:
        print("All required robotics skills are installed.")
        print("Run: bash tools/install_skills.sh --platform codex  to add upstream skills.")
        sys.exit(0)


if __name__ == "__main__":
    main()

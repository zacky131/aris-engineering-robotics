#!/usr/bin/env python3
"""
validate_installation.py — Verify that skills are correctly installed.

Usage:
    python3 tools/validate_installation.py
    python3 tools/validate_installation.py --platform codex --dest ~/.codex/skills
    python3 tools/validate_installation.py --platform antigravity --dest /project/.agents/skills
    python3 tools/validate_installation.py --platform claude --dest ~/.claude/skills
"""
import argparse
import json
import sys
from pathlib import Path

ROBOTICS_SKILLS = [
    "anchor-paper-intake",
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
    "vla-robotics",
    "learning-control-eval",
    "safety-filter-cbf",
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

SHARED_DEPS = {
    # For Antigravity: these shared directories must be co-located with skills
    "aris": "shared-references",
    "eps":  "_shared",
}


def check_skill(dest: Path, name: str) -> tuple[bool, list[str]]:
    """Returns (ok, warnings)."""
    skill_dir = dest / name
    skill_md = skill_dir / "SKILL.md"
    warnings = []

    if not skill_dir.exists():
        return False, []

    if not skill_md.exists():
        warnings.append(f"{name}/SKILL.md missing")
        return False, warnings

    # Parse YAML frontmatter (simple extraction — no library required)
    content = skill_md.read_text(errors="replace")
    if content.startswith("---"):
        end = content.find("---", 3)
        if end > 0:
            frontmatter = content[3:end]
            has_name = "name:" in frontmatter
            has_desc = "description:" in frontmatter
            if not has_name:
                warnings.append(f"{name}: SKILL.md missing 'name' in frontmatter")
            if not has_desc:
                warnings.append(f"{name}: SKILL.md missing 'description' in frontmatter")

    return True, warnings


def check_shared_dep(dest: Path, dep_name: str) -> bool:
    return (dest / dep_name).is_dir()


def check_agents_md(project_dir: Path) -> str:
    agents_md = project_dir / ".agents" / "AGENTS.md"
    if not agents_md.exists():
        return "MISSING"
    content = agents_md.read_text(errors="replace")
    if "BEGIN ARIS-ENGINEERING-ROBOTICS" in content:
        return "INSTALLED_WITH_MANAGED_BLOCK"
    return "PRESENT_NO_MANAGED_BLOCK"


def check_workflows(project_dir: Path) -> list[str]:
    wf_dir = project_dir / ".agents" / "workflows"
    if not wf_dir.exists():
        return []
    return [f.name for f in wf_dir.iterdir() if f.suffix == ".md"]


def main():
    parser = argparse.ArgumentParser(
        description="Validate ARIS Engineering Robotics installation"
    )
    parser.add_argument(
        "--platform",
        default="codex",
        choices=["codex", "claude", "antigravity"],
        help="Platform to validate (default: codex)",
    )
    parser.add_argument(
        "--dest",
        default=None,
        help="Skills directory to check. Defaults based on platform.",
    )
    parser.add_argument(
        "--project",
        default=None,
        help="Project root (for Antigravity AGENTS.md / workflow checks)",
    )
    args = parser.parse_args()

    # Resolve default dest
    if args.dest is None:
        if args.platform == "codex":
            args.dest = str(Path.home() / ".codex/skills")
        elif args.platform == "claude":
            args.dest = str(Path.home() / ".claude/skills")
        elif args.platform == "antigravity":
            args.dest = str(Path.home() / ".gemini/config/skills")

    dest = Path(args.dest)
    project = Path(args.project) if args.project else None

    print(f"=== ARIS Engineering Robotics — Installation Validator ===")
    print(f"Platform : {args.platform}")
    print(f"Skills   : {dest}")
    if project:
        print(f"Project  : {project}")
    print()

    passed = 0
    failed = 0
    total_warnings = []

    def check_group(label, skills, optional=False):
        nonlocal passed, failed
        print(f"--- {label} ---")
        for skill in skills:
            ok, warns = check_skill(dest, skill)
            total_warnings.extend(warns)
            if ok:
                warn_str = f" (⚠ {'; '.join(warns)})" if warns else ""
                print(f"  ✓: {skill}{warn_str}")
                passed += 1
            else:
                mark = "⚠ MISSING (optional)" if optional else "✗ MISSING"
                print(f"  {mark}: {skill}")
                failed += 1
        print()

    check_group("Robotics / Control Skills (REQUIRED)", ROBOTICS_SKILLS, optional=False)
    check_group("ARIS Upstream Skills (OPTIONAL)", ARIS_SKILLS, optional=True)
    check_group("EPS Upstream Skills (OPTIONAL)", EPS_SKILLS, optional=True)

    # Shared dependency checks
    print("--- Shared Dependencies ---")
    for dep_label, dep_name in SHARED_DEPS.items():
        ok = check_shared_dep(dest, dep_name)
        status = "✓" if ok else "⚠ MISSING (optional)"
        print(f"  {status}: {dep_name} ({dep_label} shared dependency)")
    print()

    # Antigravity-specific checks
    if args.platform == "antigravity" and project:
        print("--- Antigravity-Specific Checks ---")
        agents_status = check_agents_md(project)
        print(f"  AGENTS.md: {agents_status}")

        workflows = check_workflows(project)
        expected_workflows = [
            "research-robotics.md",
            "experiment-robotics.md",
            "analyze-robotics.md",
            "write-engineering-paper.md",
        ]
        for wf in expected_workflows:
            status = "✓" if wf in workflows else "⚠ MISSING"
            print(f"  workflow {status}: {wf}")
        print()

    print(f"Results: {passed} installed, {failed} missing/failed")
    if total_warnings:
        print(f"Warnings: {len(total_warnings)}")
        for w in total_warnings:
            print(f"  ⚠ {w}")
    print()

    # Only fail for required missing robotics skills
    required_missing = [s for s in ROBOTICS_SKILLS if not check_skill(dest, s)[0]]
    if required_missing:
        print(f"ERROR: {len(required_missing)} required robotics skills not installed:")
        for s in required_missing:
            print(f"  - {s}")
        print()
        print(f"Fix: bash tools/install_skills.sh --platform {args.platform} --project {project or '<path>'}")
        sys.exit(1)
    else:
        print("✓ All required robotics skills are installed.")
        if args.platform == "antigravity":
            print("  Tip: install optional upstream skills with --bootstrap flag.")
        sys.exit(0)


if __name__ == "__main__":
    main()

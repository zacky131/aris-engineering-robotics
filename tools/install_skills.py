#!/usr/bin/env python3
"""
install_skills.py — Cross-platform installer for ARIS Engineering Robotics skills.
Works on Windows (PowerShell, Command Prompt), macOS, and Linux.

Usage:
  python tools/install_skills.py --platform antigravity --project C:\\path\\to\\project
  python tools/install_skills.py --platform codex --project C:\\path\\to\\project
  python tools/install_skills.py --platform claude --project C:\\path\\to\\project
  python tools/install_skills.py --platform codex
  python tools/install_skills.py --platform codex --dry-run
  python tools/install_skills.py --list-platforms
  python tools/install_skills.py --list-skills
"""
import argparse
import datetime
import os
import shutil
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent

MANAGED_BEGIN = "<!-- BEGIN ARIS-ENGINEERING-ROBOTICS -->"
MANAGED_END = "<!-- END ARIS-ENGINEERING-ROBOTICS -->"


def list_platforms():
    print("codex")
    print("claude")
    print("antigravity")


def list_skills():
    print("")
    print("=== ARIS Research Skills ===")
    print("  research-lit, idea-discovery, idea-discovery-robot, novelty-check")
    print("  experiment-plan, research-implement-feature, run-experiment")
    print("  monitor-experiment, analyze-results, ablation-planner")
    print("  paper-claim-audit, research-review, rebuttal, paper-compile")
    print("  research-pipeline, dse-loop, claims-drafting, result-to-claim")
    print("  citation-audit, formula-derivation, paper-write")
    print("")
    print("=== Robotics / Control Skills ===")
    print("  anchor-paper-intake, robotics-research-router, robotics-experiment-plan")
    print("  run-robotics-experiment, robotics-watchdog")
    print("  robotics-result-analysis, controller-tuning")
    print("  robotics-experiment-audit, simulation-validation")
    print("  sil-hil-validation, robotics-result-to-claim")
    print("  vla-robotics, learning-control-eval, safety-filter-cbf")
    print("  research-pipeline-robotics")
    print("")
    print("=== Engineering Paper Skills ===")
    print("  engineering-writing, engineering-polishing, engineering-paper-auditor")
    print("  engineering-figure-table, engineering-response, engineering-validation")
    print("  engineering-paper-router, engineering-paper-coach")


def resolve_destination(platform: str, project_dir: Path | None) -> Path:
    home = Path.home()
    if platform == "codex":
        return project_dir / ".codex" / "skills" if project_dir else home / ".codex" / "skills"
    elif platform == "claude":
        return project_dir / ".claude" / "skills" if project_dir else home / ".claude" / "skills"
    elif platform == "antigravity":
        return project_dir / ".agents" / "skills" if project_dir else home / ".gemini" / "config" / "skills"
    else:
        raise ValueError(f"Unknown platform: {platform}")


def patch_agents_md(agents_md: Path, template_file: Path):
    template_content = template_file.read_text(encoding="utf-8")
    start = template_content.find(MANAGED_BEGIN)
    stop = template_content.find(MANAGED_END) + len(MANAGED_END)
    if start == -1 or stop <= len(MANAGED_END):
        return

    managed_block = template_content[start:stop]

    if not agents_md.exists():
        agents_md.parent.mkdir(parents=True, exist_ok=True)
        agents_md.write_text(template_content, encoding="utf-8")
        print("  INSTALLED: .agents/AGENTS.md")
        return

    existing = agents_md.read_text(encoding="utf-8")
    if MANAGED_BEGIN in existing:
        idx_s = existing.find(MANAGED_BEGIN)
        idx_e = existing.find(MANAGED_END) + len(MANAGED_END)
        updated = existing[:idx_s] + managed_block + existing[idx_e:]
        agents_md.write_text(updated, encoding="utf-8")
        print("  UPDATED: .agents/AGENTS.md (managed block replaced)")
    else:
        new_block = "\n\n---\n\n" + managed_block
        agents_md.write_text(existing + new_block, encoding="utf-8")
        print("  APPENDED: .agents/AGENTS.md (managed block added)")


def main():
    parser = argparse.ArgumentParser(description="Cross-platform skill installer for ARIS Engineering Robotics")
    parser.add_argument("--platform", choices=["codex", "claude", "antigravity"], help="Target AI coding platform")
    parser.add_argument("--project", help="Target project directory (for project-local installation)")
    parser.add_argument("--dry-run", action="store_true", help="Preview installation without copying files")
    parser.add_argument("--list-platforms", action="store_true", help="List supported platforms")
    parser.add_argument("--list-skills", action="store_true", help="List all bundled skills")

    args = parser.parse_args()

    if args.list_platforms:
        list_platforms()
        return 0

    if args.list_skills:
        list_skills()
        return 0

    if not args.platform:
        print("ERROR: --platform is required (codex, claude, antigravity).", file=sys.stderr)
        print("Run with --list-platforms to see all options.", file=sys.stderr)
        return 1

    project_dir = Path(args.project).resolve() if args.project else None
    dest_dir = resolve_destination(args.platform, project_dir)

    print("=== ARIS Engineering Robotics — Skill Installer (Cross-Platform) ===")
    print(f"Platform   : {args.platform}")
    print(f"Dry run    : {args.dry_run}")
    print(f"Destination: {dest_dir}")
    print("")

    installed_skills = []
    installed_shared = []
    installed_workflows = []
    installed_agents_md = False

    # 1. Install skills from skills/
    print("--- Installing all skills (robotics, research, engineering paper) ---")
    skills_root = REPO_ROOT / "skills"
    if skills_root.is_dir():
        for item in sorted(skills_root.iterdir()):
            if item.is_dir() and item.name not in ["_shared", "shared-references"]:
                dst = dest_dir / item.name
                if args.dry_run:
                    print(f"  DRY-RUN: would install {item.name} → {dst}")
                else:
                    dest_dir.mkdir(parents=True, exist_ok=True)
                    if dst.exists():
                        shutil.rmtree(dst)
                    shutil.copytree(item, dst)
                    print(f"  INSTALLED: {item.name}")
                    installed_skills.append(item.name)

    # 2. Install shared dependencies
    print("")
    print("--- Installing shared dependencies ---")
    for shared_name in ["shared-references", "_shared"]:
        src = REPO_ROOT / "shared" / shared_name
        if not src.is_dir():
            src = REPO_ROOT / "skills" / shared_name
        if src.is_dir():
            dst = dest_dir / shared_name
            if args.dry_run:
                print(f"  DRY-RUN: would install shared/{shared_name} → {dst}")
            else:
                dest_dir.mkdir(parents=True, exist_ok=True)
                if dst.exists():
                    shutil.rmtree(dst)
                shutil.copytree(src, dst)
                print(f"  INSTALLED shared: {shared_name}")
                installed_shared.append(shared_name)

    # 3. Antigravity project-local extras
    if args.platform == "antigravity" and project_dir:
        if args.dry_run:
            print("")
            print("DRY-RUN: would install .agents/AGENTS.md (safe patch)")
            print("DRY-RUN: would install .agents/workflows/ (workflow files)")
        else:
            agents_dir = project_dir / ".agents"
            agents_dir.mkdir(parents=True, exist_ok=True)
            agents_template = REPO_ROOT / "templates" / "antigravity" / "AGENTS.md"
            agents_md = agents_dir / "AGENTS.md"

            if agents_template.exists():
                patch_agents_md(agents_md, agents_template)
                installed_agents_md = True

            workflows_src = REPO_ROOT / "templates" / "antigravity" / "workflows"
            if workflows_src.is_dir():
                wf_dest = agents_dir / "workflows"
                wf_dest.mkdir(parents=True, exist_ok=True)
                print("")
                print("--- Installing Antigravity workflows ---")
                for wf in sorted(workflows_src.glob("*.md")):
                    dst = wf_dest / wf.name
                    shutil.copy2(wf, dst)
                    print(f"  INSTALLED workflow: {wf.name}")
                    installed_workflows.append(wf.name)

    # 4. Manifest recording
    if not args.dry_run:
        manifest_dir = REPO_ROOT / ".aris-engineering-robotics"
        manifest_dir.mkdir(parents=True, exist_ok=True)
        manifest_yaml = manifest_dir / "installed-manifest.yaml"
        manifest_legacy = manifest_dir / "installed-skills.txt"

        now = datetime.datetime.now().isoformat()
        with open(manifest_yaml, "w", encoding="utf-8") as f:
            f.write("# ARIS Engineering Robotics — install manifest\n")
            f.write(f"# Generated: {now}\n")
            f.write(f"platform: {args.platform}\n")
            f.write(f"destination: {dest_dir}\n")
            if project_dir:
                f.write(f"project: {project_dir}\n")
            f.write("\nmanaged:\n")
            f.write("  skills:\n")
            for s in installed_skills:
                f.write(f"    - {s}\n")
            f.write("  shared:\n")
            for s in installed_shared:
                f.write(f"    - {s}\n")
            f.write(f"  agents_md: {installed_agents_md}\n")
            f.write("  workflows:\n")
            for w in installed_workflows:
                f.write(f"    - {w}\n")

        with open(manifest_legacy, "w", encoding="utf-8") as f:
            for s in installed_skills:
                f.write(f"{dest_dir / s}\n")
            for s in installed_shared:
                f.write(f"{dest_dir / s}\n")

        print("")
        print(f"Manifest written to: {manifest_yaml}")

    print("")
    print(f"=== Install complete (platform={args.platform} dry_run={args.dry_run}) ===")
    print("")
    print("Validate with:")
    print(f"  python tools/validate_installation.py --platform {args.platform} --dest {dest_dir}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

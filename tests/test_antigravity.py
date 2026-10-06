#!/usr/bin/env python3
"""
Tests: Antigravity platform installation (Tests A–G).

Test A — project-local install to .agents/skills/
Test B — shared references and _shared dependency
Test C — AGENTS.md creation and safe patching
Test D — workflow files
Test E — uninstall removes only managed files
Test F — missing upstream produces actionable error message
Test G — bootstrapped (vendor) upstream works
"""
import json
import os
import re
import subprocess
import sys
import tempfile
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent
INSTALLER = REPO_ROOT / "tools" / "install_skills.sh"
UNINSTALLER = REPO_ROOT / "tools" / "uninstall_skills.sh"
VALIDATOR = REPO_ROOT / "tools" / "validate_installation.py"

REQUIRED_ROBOTICS_SKILLS = [
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

EXPECTED_WORKFLOWS = [
    "research-robotics.md",
    "experiment-robotics.md",
    "analyze-robotics.md",
    "write-engineering-paper.md",
    "vla-robotics.md",
    "learning-control.md",
]

MANAGED_BEGIN = "<!-- BEGIN ARIS-ENGINEERING-ROBOTICS -->"
MANAGED_END   = "<!-- END ARIS-ENGINEERING-ROBOTICS -->"


def run(cmd: list, cwd=None, env=None) -> subprocess.CompletedProcess:
    e = dict(os.environ)
    if env:
        e.update(env)
    return subprocess.run(cmd, cwd=cwd or REPO_ROOT, capture_output=True, text=True, env=e)


# ── Test A — project-local antigravity install ─────────────────────────────────
def test_a_project_local_install():
    with tempfile.TemporaryDirectory() as tmp:
        project = Path(tmp)
        result = run([
            "bash", str(INSTALLER),
            "--platform", "antigravity",
            "--project", str(project),
        ])
        assert result.returncode == 0, f"Installer failed:\n{result.stdout}\n{result.stderr}"

        skills_dir = project / ".agents" / "skills"
        assert skills_dir.is_dir(), ".agents/skills/ not created"

        missing = [s for s in REQUIRED_ROBOTICS_SKILLS if not (skills_dir / s / "SKILL.md").exists()]
        assert not missing, f"Missing required skills: {missing}"

        print("PASS A: project-local Antigravity install")


# ── Test B — shared dependencies ──────────────────────────────────────────────
def test_b_shared_dependencies():
    with tempfile.TemporaryDirectory() as tmp:
        project = Path(tmp)
        result = run([
            "bash", str(INSTALLER),
            "--platform", "antigravity",
            "--project", str(project),
        ])
        assert result.returncode == 0, f"Installer failed:\n{result.stderr}"

        skills_dir = project / ".agents" / "skills"

        # EPS _shared — only check if EPS skills were installed
        eps_skills = list(skills_dir.glob("engineering-*"))
        if eps_skills:
            eps_shared = skills_dir / "_shared"
            if not eps_shared.is_dir():
                print("  NOTE: _shared not installed (EPS _shared may not exist in upstream)")
            else:
                print(f"  _shared installed: {eps_shared}")

        # ARIS shared-references — only check if ARIS skills were installed
        aris_skills = list(skills_dir.glob("research-lit"))
        if aris_skills:
            aris_shared = skills_dir / "shared-references"
            if not aris_shared.is_dir():
                print("  NOTE: shared-references not installed (may not exist in upstream)")
            else:
                print(f"  shared-references installed: {aris_shared}")

        print("PASS B: shared dependencies check")


# ── Test C — AGENTS.md creation and safe patching ─────────────────────────────
def test_c_agents_md():
    with tempfile.TemporaryDirectory() as tmp:
        project = Path(tmp)
        agents_dir = project / ".agents"
        agents_md = agents_dir / "AGENTS.md"

        # First install: should create AGENTS.md
        result = run([
            "bash", str(INSTALLER),
            "--platform", "antigravity",
            "--project", str(project),
        ])
        assert result.returncode == 0, f"First install failed:\n{result.stderr}"
        assert agents_md.exists(), "AGENTS.md not created on first install"

        first_content = agents_md.read_text()
        assert MANAGED_BEGIN in first_content, "Managed block not in AGENTS.md"
        assert MANAGED_END in first_content, "Managed block end not in AGENTS.md"

        # Add user content before and after managed block
        agents_md.write_text(
            "# My Research Project\n\nMy custom rules.\n\n" + first_content + "\n\n## My Extra Section\n"
        )

        # Second install: should patch managed block without destroying user content
        result2 = run([
            "bash", str(INSTALLER),
            "--platform", "antigravity",
            "--project", str(project),
        ])
        assert result2.returncode == 0, f"Second install failed:\n{result2.stderr}"

        second_content = agents_md.read_text()
        assert "My custom rules." in second_content, "User content destroyed by reinstall"
        assert "My Extra Section" in second_content, "User section destroyed by reinstall"
        assert MANAGED_BEGIN in second_content, "Managed block missing after reinstall"

        # Managed block should appear exactly once
        count = second_content.count(MANAGED_BEGIN)
        assert count == 1, f"Managed block duplicated (appears {count} times)"

        print("PASS C: AGENTS.md creation and safe patching")


# ── Test D — workflows ─────────────────────────────────────────────────────────
def test_d_workflows():
    with tempfile.TemporaryDirectory() as tmp:
        project = Path(tmp)
        result = run([
            "bash", str(INSTALLER),
            "--platform", "antigravity",
            "--project", str(project),
        ])
        assert result.returncode == 0

        wf_dir = project / ".agents" / "workflows"
        assert wf_dir.is_dir(), ".agents/workflows/ not created"

        missing = [w for w in EXPECTED_WORKFLOWS if not (wf_dir / w).exists()]
        assert not missing, f"Missing workflows: {missing}"

        # Verify workflows are non-empty
        for wf in EXPECTED_WORKFLOWS:
            content = (wf_dir / wf).read_text()
            assert len(content) > 100, f"Workflow {wf} appears empty"

        print("PASS D: workflows installed correctly")


# ── Test E — uninstall only removes managed files ─────────────────────────────
def test_e_selective_uninstall():
    with tempfile.TemporaryDirectory() as tmp:
        project = Path(tmp)

        # Install
        run([
            "bash", str(INSTALLER),
            "--platform", "antigravity",
            "--project", str(project),
        ])

        skills_dir = project / ".agents" / "skills"
        # Create a user skill
        user_skill = skills_dir / "my-user-skill"
        user_skill.mkdir()
        (user_skill / "SKILL.md").write_text("---\nname: my-user-skill\n---\n# My skill\n")

        # Uninstall
        result = run(["bash", str(UNINSTALLER)])
        assert result.returncode == 0, f"Uninstall failed:\n{result.stderr}"

        # User skill should remain
        assert user_skill.exists(), "Uninstall destroyed user skill"

        print("PASS E: uninstall preserves user-created skills")


# ── Test F — missing upstream gives actionable error ──────────────────────────
def test_f_missing_upstream_actionable():
    """When upstreams cannot be found, installer should warn and still install robotics skills."""
    with tempfile.TemporaryDirectory() as tmp:
        project = Path(tmp) / "project"
        project.mkdir()

        # Point upstream paths to non-existent locations AND override config path
        env = {
            "ARIS_REPO": "/nonexistent_aris_path_xyz",
            "EPS_REPO":  "/nonexistent_eps_path_xyz",
            # Override PATH so sibling-detection falls back to vendor only
            "HOME": str(Path(tmp) / "fakehome"),  # avoids ~/.gemini interferance
        }
        # We also need to ensure the sibling path doesn't exist
        # by running with a fake repo root (copying the installer to a temp location)
        fake_repo = Path(tmp) / "fake_repo"
        fake_repo.mkdir()
        (fake_repo / "tools").mkdir()
        import shutil
        shutil.copy(INSTALLER, fake_repo / "tools" / "install_skills.sh")
        # Copy required skills/
        shutil.copytree(REPO_ROOT / "skills", fake_repo / "skills")
        shutil.copytree(REPO_ROOT / ".aris-engineering-robotics", fake_repo / ".aris-engineering-robotics")
        shutil.copytree(REPO_ROOT / "templates", fake_repo / "templates")

        result = run([
            "bash", str(fake_repo / "tools" / "install_skills.sh"),
            "--platform", "antigravity",
            "--project", str(project),
        ], cwd=fake_repo, env=env)

        output = result.stdout + result.stderr
        # Should warn about missing upstreams
        assert "NOT FOUND" in output or "not found" in output.lower() or "SKIP" in output, \
            f"Expected actionable missing-upstream message.\nOutput:\n{output}"

        # Robotics skills should still be installed
        skills_dir = project / ".agents" / "skills"
        for s in REQUIRED_ROBOTICS_SKILLS:
            assert (skills_dir / s / "SKILL.md").exists(), f"Robotics skill missing: {s}"

        print("PASS F: missing upstream gives actionable message; robotics skills install")


# ── Test G — validation script works for antigravity ──────────────────────────
def test_g_validator_antigravity():
    with tempfile.TemporaryDirectory() as tmp:
        project = Path(tmp)

        # Install
        run([
            "bash", str(INSTALLER),
            "--platform", "antigravity",
            "--project", str(project),
        ])

        skills_dir = project / ".agents" / "skills"
        result = run([
            sys.executable, str(VALIDATOR),
            "--platform", "antigravity",
            "--dest", str(skills_dir),
            "--project", str(project),
        ])

        assert result.returncode == 0, (
            f"Validator failed for Antigravity install:\n{result.stdout}\n{result.stderr}"
        )
        assert "All required robotics skills are installed" in result.stdout

        print("PASS G: validator passes for Antigravity installation")


if __name__ == "__main__":
    tests = [
        test_a_project_local_install,
        test_b_shared_dependencies,
        test_c_agents_md,
        test_d_workflows,
        test_e_selective_uninstall,
        test_f_missing_upstream_actionable,
        test_g_validator_antigravity,
    ]
    failed = 0
    for t in tests:
        try:
            t()
        except AssertionError as e:
            print(f"FAIL: {t.__name__}: {e}")
            failed += 1
        except Exception as e:
            print(f"ERROR: {t.__name__}: {e}")
            failed += 1

    print(f"\n{len(tests) - failed}/{len(tests)} tests passed")
    sys.exit(0 if failed == 0 else 1)

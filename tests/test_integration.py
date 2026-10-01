#!/usr/bin/env python3
"""Tests: repository integration — upstream path detection, installer dry-run."""
import os
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent

def test_repo_structure_exists():
    """New repository has required directories."""
    required = ["skills", "shared", "profiles", "schemas", "templates", "tools", "docs"]
    for d in required:
        assert (REPO_ROOT / d).is_dir(), f"Missing directory: {d}"
    print("PASS: repo structure exists")

def test_all_skills_have_skill_md():
    """Every skill directory has a SKILL.md (excluding shared reference dirs)."""
    skills_dir = REPO_ROOT / "skills"
    skill_count = 0
    for skill_dir in skills_dir.iterdir():
        if skill_dir.is_dir() and skill_dir.name not in ["_shared", "shared-references"]:
            assert (skill_dir / "SKILL.md").exists(), f"SKILL.md missing in {skill_dir.name}"
            skill_count += 1
    assert skill_count >= 50, f"Expected at least 50 skills, found {skill_count}"
    print(f"PASS: all {skill_count} skills have SKILL.md")

def test_upstream_aris_detection():
    """ARIS upstream repo is detectable."""
    aris = REPO_ROOT.parent / "Auto-claude-code-research-in-sleep"
    assert aris.is_dir(), f"ARIS repo not found at {aris}"
    assert (aris / "skills").is_dir(), "ARIS skills directory missing"
    print("PASS: ARIS repo detected")

def test_upstream_eps_detection():
    """EPS upstream repo is detectable."""
    eps = REPO_ROOT.parent / "engineering-paper-skills"
    assert eps.is_dir(), f"EPS repo not found at {eps}"
    assert (eps / "skills").is_dir(), "EPS skills directory missing"
    print("PASS: EPS repo detected")

def test_installer_dry_run():
    """Dry-run installer completes without error."""
    result = subprocess.run(
        ["bash", "tools/install_skills.sh", "--platform", "codex", "--dry-run"],
        cwd=REPO_ROOT, capture_output=True, text=True
    )
    assert result.returncode == 0, f"Installer failed:\n{result.stdout}\n{result.stderr}"
    assert "DRY-RUN" in result.stdout, "Dry-run output missing expected marker"
    print("PASS: installer dry-run succeeded")

def test_config_file_exists():
    """Integration config file exists."""
    cfg = REPO_ROOT / ".aris-engineering-robotics" / "config.yaml"
    assert cfg.exists(), f"Config not found: {cfg}"
    print("PASS: config.yaml exists")

if __name__ == "__main__":
    tests = [
        test_repo_structure_exists,
        test_all_skills_have_skill_md,
        test_upstream_aris_detection,
        test_upstream_eps_detection,
        test_installer_dry_run,
        test_config_file_exists,
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

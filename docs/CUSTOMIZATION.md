# Customization Guide

## Adding a new profile

1. Create `profiles/my_profile.yaml` following the existing profile format.
2. Add the profile name to the `detect_profiles()` logic in `robotics-research-router/SKILL.md`.
3. Add profile-specific metrics to `shared/robotics-metrics.md` if needed.

## Adding a new skill

1. Create `skills/my-skill/SKILL.md` with YAML frontmatter (name, description, platforms).
2. Add the skill to `install_skills.sh` in the robotics skills section.
3. Update `docs/SKILL_OWNERSHIP.md` to assign task ownership.
4. Add a test in `tests/test_integration.py`.

## Overriding upstream skill paths

Edit `.aris-engineering-robotics/config.yaml` or set environment variables:

```bash
export ARIS_REPO=/path/to/your/aris
export EPS_REPO=/path/to/your/eps
```

## Installing on multiple machines

Run the installer on each machine:

```bash
bash tools/install_skills.sh --platform codex
```

The installer reads from the upstream repos at their configured paths.

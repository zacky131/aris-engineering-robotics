#!/usr/bin/env python3
"""Tests: Vision-Language-Action (VLA), Learning-Based Control, AI Control, and SOTA Safety filters."""
import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent

try:
    import yaml
    HAS_YAML = True
except ImportError:
    HAS_YAML = False

try:
    import jsonschema
    HAS_JSONSCHEMA = True
except ImportError:
    HAS_JSONSCHEMA = False


def test_vla_and_learning_profiles():
    if not HAS_YAML:
        print("SKIP: PyYAML not installed")
        return

    expected_profiles = {
        "vla_robotics.yaml": "vla_robotics",
        "learning_control.yaml": "learning_control",
        "ai_control.yaml": "ai_control",
        "safe_sota_control.yaml": "safe_sota_control",
    }

    for filename, profile_name in expected_profiles.items():
        profile_path = REPO_ROOT / "profiles" / filename
        assert profile_path.exists(), f"Missing profile file: {profile_path}"
        with open(profile_path) as f:
            data = yaml.safe_load(f)
        assert data.get("profile") == profile_name, f"Expected profile '{profile_name}', got {data.get('profile')}"
        assert "description" in data, f"Missing description in {filename}"

    print("PASS: all 4 advanced control & VLA profiles parsed and verified")


def test_vla_evaluation_schema_and_template():
    schema_path = REPO_ROOT / "schemas" / "vla-evaluation.schema.json"
    template_path = REPO_ROOT / "templates" / "VLA_EVALUATION.yaml"

    assert schema_path.exists(), "Missing vla-evaluation.schema.json"
    assert template_path.exists(), "Missing VLA_EVALUATION.yaml"

    with open(schema_path) as f:
        schema = json.load(f)
    assert schema.get("$schema"), "Missing $schema in vla-evaluation.schema.json"
    for req in ["vla_model", "benchmark", "evaluation_matrix", "action_chunking", "safety"]:
        assert req in schema.get("required", []), f"Missing '{req}' in schema required"

    if HAS_YAML and HAS_JSONSCHEMA:
        with open(template_path) as f:
            template_data = yaml.safe_load(f)
        jsonschema.validate(instance=template_data, schema=schema)
        print("PASS: VLA_EVALUATION.yaml passes jsonschema validation")
    else:
        print("PASS: VLA schema structure checked (jsonschema/pyyaml missing)")


def test_learning_control_schema_and_template():
    schema_path = REPO_ROOT / "schemas" / "learning-control.schema.json"
    template_path = REPO_ROOT / "templates" / "LEARNING_EXPERIMENT.yaml"

    assert schema_path.exists(), "Missing learning-control.schema.json"
    assert template_path.exists(), "Missing LEARNING_EXPERIMENT.yaml"

    with open(schema_path) as f:
        schema = json.load(f)
    assert schema.get("$schema"), "Missing $schema in learning-control.schema.json"
    for req in ["experiment", "algorithm", "environment", "seeds", "metrics"]:
        assert req in schema.get("required", []), f"Missing '{req}' in schema required"

    if HAS_YAML and HAS_JSONSCHEMA:
        with open(template_path) as f:
            template_data = yaml.safe_load(f)
        jsonschema.validate(instance=template_data, schema=schema)
        print("PASS: LEARNING_EXPERIMENT.yaml passes jsonschema validation")
    else:
        print("PASS: Learning control schema structure checked (jsonschema/pyyaml missing)")


def test_shared_standards_and_skills_sync():
    standards = [
        "vla-standards.md",
        "learning-control-standards.md",
        "ai-control-realtime.md",
        "safety-cbf-standards.md",
    ]
    for std in standards:
        shared_file = REPO_ROOT / "shared" / std
        skill_shared_file = REPO_ROOT / "skills" / "_shared" / std
        assert shared_file.exists(), f"Missing shared/{std}"
        assert skill_shared_file.exists(), f"Missing skills/_shared/{std}"
        content_shared = shared_file.read_text()
        content_skill = skill_shared_file.read_text()
        assert content_shared == content_skill, f"Sync mismatch between shared/{std} and skills/_shared/{std}"

    print("PASS: shared standards exist and are in sync with skills/_shared/")


def test_new_skills_frontmatter():
    new_skills = [
        "vla-robotics",
        "learning-control-eval",
        "safety-filter-cbf",
    ]
    for skill in new_skills:
        skill_file = REPO_ROOT / "skills" / skill / "SKILL.md"
        assert skill_file.exists(), f"Missing skill file: {skill_file}"
        content = skill_file.read_text()
        assert content.startswith("---"), f"Missing frontmatter in {skill}"
        assert f"name: {skill}" in content, f"Missing name: {skill} in frontmatter"
        assert "description:" in content, f"Missing description in {skill}"
        assert "platforms:" in content, f"Missing platforms in {skill}"

    print("PASS: all new skills exist with valid frontmatter")


def test_new_antigravity_workflows():
    workflows = [
        "vla-robotics.md",
        "learning-control.md",
    ]
    for wf in workflows:
        wf_file = REPO_ROOT / "templates" / "antigravity" / "workflows" / wf
        assert wf_file.exists(), f"Missing workflow file: {wf_file}"
        content = wf_file.read_text()
        assert len(content) > 200, f"Workflow {wf} seems too short"
        assert "# Workflow:" in content, f"Workflow header missing in {wf}"

    print("PASS: Antigravity VLA and Learning Control workflows verified")


def test_experiment_schema_expanded_enums():
    path = REPO_ROOT / "schemas" / "experiment.schema.json"
    assert path.exists()
    with open(path) as f:
        schema = json.load(f)
    domains = schema["properties"]["experiment"]["properties"]["domain"]["enum"]
    simulators = schema["properties"]["platform"]["properties"]["simulator"]["enum"]

    assert "learning_control" in domains, "Expected 'learning_control' in domain enum"
    assert "ai_control" in domains, "Expected 'ai_control' in domain enum"
    assert "vla_manipulation" in domains, "Expected 'vla_manipulation' in domain enum"
    assert "vla_navigation" in domains, "Expected 'vla_navigation' in domain enum"
    assert "simpler_env" in simulators, "Expected 'simpler_env' in simulator enum"
    assert "libero" in simulators, "Expected 'libero' in simulator enum"
    assert "maniskill" in simulators, "Expected 'maniskill' in simulator enum"

    print("PASS: experiment.schema.json domain and simulator enums successfully expanded")


if __name__ == "__main__":
    tests = [
        test_vla_and_learning_profiles,
        test_vla_evaluation_schema_and_template,
        test_learning_control_schema_and_template,
        test_shared_standards_and_skills_sync,
        test_new_skills_frontmatter,
        test_new_antigravity_workflows,
        test_experiment_schema_expanded_enums,
    ]
    failed = 0
    for t in tests:
        try:
            t()
        except Exception as e:
            print(f"FAIL: {t.__name__}: {e}")
            failed += 1
    print(f"\n{len(tests)-failed}/{len(tests)} passed")
    sys.exit(0 if failed == 0 else 1)

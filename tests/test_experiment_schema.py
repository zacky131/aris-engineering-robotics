#!/usr/bin/env python3
"""Tests: experiment schema and template validation."""
import json, sys
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent

try:
    import yaml
    HAS_YAML = True
except ImportError:
    HAS_YAML = False

def test_experiment_schema_parseable():
    path = REPO_ROOT / "schemas" / "experiment.schema.json"
    assert path.exists()
    with open(path) as f:
        schema = json.load(f)
    for key in ["experiment", "platform", "scenario", "metrics"]:
        assert key in schema.get("required", []), f"'{key}' not in required"
    print("PASS: experiment schema has required fields")

def test_template_parseable():
    if not HAS_YAML:
        print("SKIP: PyYAML not installed")
        return
    path = REPO_ROOT / "templates" / "EXPERIMENT.yaml"
    assert path.exists()
    with open(path) as f:
        data = yaml.safe_load(f)
    assert "experiment" in data
    assert "platform" in data
    assert "metrics" in data
    print("PASS: EXPERIMENT.yaml template parseable")

def test_valid_platform_types():
    if not HAS_YAML:
        print("SKIP: PyYAML not installed")
        return
    path = REPO_ROOT / "schemas" / "experiment.schema.json"
    with open(path) as f:
        schema = json.load(f)
    valid_types = schema["properties"]["platform"]["properties"]["type"]["enum"]
    assert "simulation" in valid_types
    assert "real" in valid_types
    assert "hil" in valid_types
    print("PASS: platform types include simulation/real/hil")

if __name__ == "__main__":
    tests = [test_experiment_schema_parseable, test_template_parseable, test_valid_platform_types]
    failed = 0
    for t in tests:
        try:
            t()
        except Exception as e:
            print(f"FAIL: {t.__name__}: {e}")
            failed += 1
    print(f"\n{len(tests)-failed}/{len(tests)} passed")
    sys.exit(0 if failed == 0 else 1)

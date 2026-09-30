#!/usr/bin/env python3
"""Tests: claim map schema validation."""
import json, sys
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent

try:
    import yaml
    HAS_YAML = True
except ImportError:
    HAS_YAML = False

def test_schema_parseable():
    schema_path = REPO_ROOT / "schemas" / "claim-map.schema.json"
    assert schema_path.exists(), "claim-map.schema.json not found"
    with open(schema_path) as f:
        schema = json.load(f)
    assert "claims" in schema.get("properties", {}), "claims property missing from schema"
    print("PASS: claim-map schema parseable")

def test_template_parseable():
    if not HAS_YAML:
        print("SKIP: PyYAML not installed")
        return
    tpl = REPO_ROOT / "templates" / "CLAIM_MAP.yaml"
    assert tpl.exists()
    with open(tpl) as f:
        data = yaml.safe_load(f)
    assert "claims" in data, "claims key missing from template"
    c001 = data["claims"].get("C001", {})
    assert "status" in c001, "status key missing from C001"
    assert "evidence" in c001, "evidence key missing from C001"
    print("PASS: CLAIM_MAP.yaml template parseable")

def test_claim_id_pattern():
    if not HAS_YAML:
        print("SKIP: PyYAML not installed")
        return
    tpl = REPO_ROOT / "templates" / "CLAIM_MAP.yaml"
    with open(tpl) as f:
        data = yaml.safe_load(f)
    import re
    for cid in data.get("claims", {}):
        assert re.match(r"^C\d+$", cid), f"Invalid claim ID format: {cid}"
    print("PASS: claim ID format correct")

if __name__ == "__main__":
    tests = [test_schema_parseable, test_template_parseable, test_claim_id_pattern]
    failed = 0
    for t in tests:
        try:
            t()
        except Exception as e:
            print(f"FAIL: {t.__name__}: {e}")
            failed += 1
    print(f"\n{len(tests)-failed}/{len(tests)} passed")
    sys.exit(0 if failed == 0 else 1)

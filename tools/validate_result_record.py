#!/usr/bin/env python3
"""
validate_result_record.py — Verify a RESULT_SUMMARY.yaml result record.
Checks that result files exist and metrics are not null.

Usage:
    python tools/validate_result_record.py path/to/RESULT_SUMMARY.yaml
"""
import argparse
import sys
from pathlib import Path

try:
    import yaml
except ImportError:
    print("ERROR: PyYAML not installed. Run: pip install pyyaml")
    sys.exit(1)


def validate(path: Path) -> int:
    errors = 0
    with open(path) as f:
        data = yaml.safe_load(f)

    project_dir = path.parent
    exp_id = data.get("experiment_id", "unknown")
    result_files = data.get("result_files", [])
    metrics = data.get("metrics", {})
    evidence_level = data.get("evidence_level")

    print(f"=== Result Record Validator ===")
    print(f"Experiment: {exp_id}")
    print()

    for rf in result_files:
        abs_path = project_dir / rf
        if abs_path.exists():
            print(f"  ✓ result file exists: {rf}")
        else:
            print(f"  ✗ result file MISSING: {rf}")
            errors += 1

    for k, v in metrics.items():
        val = v.get("mean") or v.get("value") if isinstance(v, dict) else v
        if val is None:
            print(f"  ⚠ metric null: {k}")
        else:
            print(f"  ✓ metric: {k} = {v}")

    if evidence_level:
        print(f"  ✓ evidence_level: {evidence_level}")
    else:
        print(f"  ⚠ evidence_level not set")

    print()
    print(f"Errors: {errors}")
    return errors


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("record", nargs="?", default="RESULT_SUMMARY.yaml")
    args = parser.parse_args()
    path = Path(args.record)
    if not path.exists():
        print(f"ERROR: {path} not found")
        sys.exit(1)
    sys.exit(1 if validate(path) > 0 else 0)


if __name__ == "__main__":
    main()

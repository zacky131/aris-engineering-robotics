#!/usr/bin/env python3
"""
validate_evidence_ledger.py — Verify that all evidence records in EVIDENCE_LEDGER.yaml
have their source files present and metric values filled.

Usage:
    python tools/validate_evidence_ledger.py path/to/EVIDENCE_LEDGER.yaml
"""
import argparse
import sys
from pathlib import Path

try:
    import yaml
except ImportError:
    print("ERROR: PyYAML not installed. Run: pip install pyyaml")
    sys.exit(1)


def validate(ledger_path: Path) -> int:
    errors = 0
    warnings = 0

    with open(ledger_path) as f:
        data = yaml.safe_load(f)

    evidence = data.get("evidence", {})
    project_dir = ledger_path.parent

    print(f"=== Evidence Ledger Validator ===")
    print(f"File   : {ledger_path}")
    print(f"Project: {project_dir}")
    print(f"Records: {len(evidence)}")
    print()

    for eid, record in evidence.items():
        source_file = record.get("source", {}).get("file")
        verified = record.get("verified", False)
        metrics = record.get("metrics", {})
        evidence_level = record.get("evidence_level")

        print(f"--- {eid} ---")

        # Check source file
        if not source_file:
            print(f"  ERROR: no source.file")
            errors += 1
        else:
            abs_path = project_dir / source_file
            if abs_path.exists():
                print(f"  ✓ source file exists: {source_file}")
            else:
                print(f"  ✗ source file MISSING: {source_file}")
                errors += 1

        # Check metrics not null
        null_metrics = [k for k, v in metrics.items() if v is None]
        filled_metrics = [k for k, v in metrics.items() if v is not None]

        if filled_metrics:
            print(f"  ✓ metrics filled: {', '.join(filled_metrics)}")
        if null_metrics:
            print(f"  ⚠ metrics null (unfilled): {', '.join(null_metrics)}")
            warnings += 1

        # Check evidence level
        if not evidence_level:
            print(f"  ⚠ evidence_level not set (should be L0–L6)")
            warnings += 1
        else:
            print(f"  ✓ evidence level: {evidence_level}")

        # Check verified flag
        if verified and errors == 0:
            print(f"  ✓ verified: true")
        elif verified and errors > 0:
            print(f"  ERROR: verified=true but source file is missing — reset to false")
            errors += 1
        else:
            print(f"  ⚠ verified: false (run validator before setting true)")
            warnings += 1

        print()

    print(f"Errors: {errors}, Warnings: {warnings}")
    return errors


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("ledger", nargs="?", default="EVIDENCE_LEDGER.yaml",
                        help="Path to EVIDENCE_LEDGER.yaml")
    args = parser.parse_args()

    path = Path(args.ledger)
    if not path.exists():
        print(f"ERROR: File not found: {path}")
        sys.exit(1)

    errors = validate(path)
    sys.exit(1 if errors > 0 else 0)


if __name__ == "__main__":
    main()

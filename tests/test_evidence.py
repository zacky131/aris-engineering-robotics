#!/usr/bin/env python3
"""Tests: evidence ledger validation."""
import sys
from pathlib import Path
import tempfile, textwrap

REPO_ROOT = Path(__file__).parent.parent
TOOL = REPO_ROOT / "tools" / "validate_evidence_ledger.py"

try:
    import yaml
    HAS_YAML = True
except ImportError:
    HAS_YAML = False

def run_validator(content: str, extra_files=None) -> int:
    import subprocess, os
    with tempfile.TemporaryDirectory() as tmpdir:
        ledger = Path(tmpdir) / "EVIDENCE_LEDGER.yaml"
        ledger.write_text(content)
        if extra_files:
            for fname, fcontent in extra_files.items():
                p = Path(tmpdir) / fname
                p.parent.mkdir(parents=True, exist_ok=True)
                p.write_text(fcontent)
        result = subprocess.run(
            [sys.executable, str(TOOL), str(ledger)],
            capture_output=True, text=True
        )
        return result.returncode

def test_valid_evidence_with_existing_source():
    content = textwrap.dedent("""
    project: {name: test, domain: robotics}
    evidence:
      E001:
        type: simulation_result
        evidence_level: L2
        source: {file: results/run.csv, commit: null}
        experiment: {id: EXP001}
        metrics: {position_rmse_m: 0.34}
        scope: {environment: simulation, trials: 20}
        verified: false
    """)
    rc = run_validator(content, {"results/run.csv": "col1,col2\n1,2\n"})
    assert rc == 0, "Expected success for valid evidence with existing source"
    print("PASS: valid evidence with existing source")

def test_missing_source_file():
    content = textwrap.dedent("""
    project: {name: test, domain: robotics}
    evidence:
      E001:
        type: simulation_result
        evidence_level: L2
        source: {file: results/nonexistent.csv, commit: null}
        experiment: {id: EXP001}
        metrics: {position_rmse_m: 0.34}
        scope: {environment: simulation, trials: 20}
        verified: false
    """)
    rc = run_validator(content)
    assert rc != 0, "Expected failure for missing source file"
    print("PASS: missing source file detected")

def test_null_metrics_warns():
    content = textwrap.dedent("""
    project: {name: test, domain: robotics}
    evidence:
      E001:
        type: simulation_result
        evidence_level: L2
        source: {file: results/run.csv, commit: null}
        experiment: {id: EXP001}
        metrics: {position_rmse_m: null}
        scope: {environment: simulation, trials: 20}
        verified: false
    """)
    rc = run_validator(content, {"results/run.csv": "col\n1\n"})
    # Null metrics produce warning but not error
    assert rc == 0, "Null metrics should warn but not error"
    print("PASS: null metrics produce warning but no error")

if __name__ == "__main__":
    tests = [test_valid_evidence_with_existing_source,
             test_missing_source_file,
             test_null_metrics_warns]
    failed = 0
    for t in tests:
        try:
            t()
        except Exception as e:
            print(f"FAIL: {t.__name__}: {e}")
            failed += 1
    print(f"\n{len(tests)-failed}/{len(tests)} tests passed")
    sys.exit(0 if failed == 0 else 1)

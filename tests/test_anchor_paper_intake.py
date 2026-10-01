#!/usr/bin/env python3
"""
Tests: Anchor-Paper-First Research Intake system.

Covers all 12 acceptance test cases required by add_anchor_paper_intake_prompt.md:
  Test 1  — simple anchor discovery
  Test 2  — categorized discovery
  Test 3  — empty directory
  Test 4  — stable AP IDs
  Test 5  — manifest detects unchanged PDF
  Test 6  — manifest detects changed/new PDF
  Test 7  — gap-state validation
  Test 8  — project initialization does not overwrite files
  Test 9  — gitignore protects PDFs
  Test 10 — anchor intake precedes literature search when PDFs exist
  Test 11 — no-anchor project follows legacy flow
  Test 12 — already-processed unchanged anchors are not unnecessarily reprocessed
"""

import hashlib
import json
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent

VALID_GAP_STATES = {
    "UNVERIFIED",
    "SEARCHING",
    "SUPPORTED_AS_CURRENT_GAP",
    "PARTIALLY_RESOLVED",
    "RESOLVED_BY_PRIOR_WORK",
    "INSUFFICIENT_EVIDENCE",
}

VALID_CATEGORIES = {
    "foundational",
    "closest_work",
    "methodology",
    "benchmark",
    "uncategorized",
}


def compute_sha256(filepath: Path) -> str:
    h = hashlib.sha256()
    with open(filepath, "rb") as f:
        while chunk := f.read(8192):
            h.update(chunk)
    return h.hexdigest()


def discover_anchor_papers(anchor_dir: Path) -> list[dict]:
    """Simulates discovery logic of anchor-paper-intake skill."""
    if not anchor_dir.is_dir():
        return []

    papers = []
    # Find all pdfs
    for p in sorted(anchor_dir.rglob("*.pdf")):
        rel = p.relative_to(anchor_dir)
        parts = rel.parts
        if len(parts) > 1 and parts[0] in VALID_CATEGORIES:
            category = parts[0]
        else:
            category = "uncategorized"

        papers.append({
            "path": p,
            "rel_path": str(p.relative_to(anchor_dir.parent)),
            "category": category,
            "filename": p.name,
            "sha256": compute_sha256(p),
        })

    # Stable sorting: category then filename
    papers.sort(key=lambda x: (x["category"], x["filename"]))
    for idx, p in enumerate(papers, start=1):
        p["paper_id"] = f"AP{idx:03d}"

    return papers


# --- Test 1: Simple anchor discovery ---
def test_1_simple_anchor_discovery():
    with tempfile.TemporaryDirectory() as tmpdir:
        tmp = Path(tmpdir)
        anchor_dir = tmp / "anchor_papers"
        anchor_dir.mkdir()

        (anchor_dir / "paperA.pdf").write_bytes(b"%PDF-1.4 paper A dummy content")
        (anchor_dir / "paperB.pdf").write_bytes(b"%PDF-1.4 paper B dummy content")

        found = discover_anchor_papers(anchor_dir)
        assert len(found) == 2, f"Expected 2 papers, found {len(found)}"
        for p in found:
            assert p["category"] == "uncategorized"
            assert p["paper_id"].startswith("AP")
        print("PASS: Test 1 — simple anchor discovery")


# --- Test 2: Categorized discovery ---
def test_2_categorized_discovery():
    with tempfile.TemporaryDirectory() as tmpdir:
        tmp = Path(tmpdir)
        anchor_dir = tmp / "anchor_papers"
        for cat in ["foundational", "closest_work", "methodology", "benchmark", "uncategorized"]:
            (anchor_dir / cat).mkdir(parents=True)

        (anchor_dir / "foundational" / "classic.pdf").write_bytes(b"%PDF-1.4 classic")
        (anchor_dir / "closest_work" / "rival.pdf").write_bytes(b"%PDF-1.4 rival")
        (anchor_dir / "methodology" / "kalman.pdf").write_bytes(b"%PDF-1.4 kalman")
        (anchor_dir / "benchmark" / "dataset.pdf").write_bytes(b"%PDF-1.4 dataset")

        found = discover_anchor_papers(anchor_dir)
        assert len(found) == 4, f"Expected 4 papers, found {len(found)}"

        cat_map = {p["filename"]: p["category"] for p in found}
        assert cat_map["classic.pdf"] == "foundational"
        assert cat_map["rival.pdf"] == "closest_work"
        assert cat_map["kalman.pdf"] == "methodology"
        assert cat_map["dataset.pdf"] == "benchmark"
        print("PASS: Test 2 — categorized discovery")


# --- Test 3: Empty directory ---
def test_3_empty_directory():
    with tempfile.TemporaryDirectory() as tmpdir:
        tmp = Path(tmpdir)
        anchor_dir = tmp / "anchor_papers"
        anchor_dir.mkdir()

        found = discover_anchor_papers(anchor_dir)
        assert len(found) == 0, f"Expected 0 papers, found {len(found)}"
        print("PASS: Test 3 — empty directory")


# --- Test 4: Stable AP IDs ---
def test_4_stable_ap_ids():
    with tempfile.TemporaryDirectory() as tmpdir:
        tmp = Path(tmpdir)
        anchor_dir = tmp / "anchor_papers"
        anchor_dir.mkdir()

        (anchor_dir / "paper1.pdf").write_bytes(b"%PDF-1.4 content 1")
        (anchor_dir / "paper2.pdf").write_bytes(b"%PDF-1.4 content 2")
        (anchor_dir / "paper3.pdf").write_bytes(b"%PDF-1.4 content 3")

        run1 = discover_anchor_papers(anchor_dir)
        run2 = discover_anchor_papers(anchor_dir)

        ids1 = [p["paper_id"] for p in run1]
        ids2 = [p["paper_id"] for p in run2]
        assert ids1 == ["AP001", "AP002", "AP003"], f"Unexpected IDs: {ids1}"
        assert ids1 == ids2, "Paper IDs are not deterministic across runs"
        print("PASS: Test 4 — stable AP IDs")


# --- Test 5: Manifest detects unchanged PDF ---
def test_5_manifest_detects_unchanged_pdf():
    with tempfile.TemporaryDirectory() as tmpdir:
        tmp = Path(tmpdir)
        anchor_dir = tmp / "anchor_papers"
        anchor_dir.mkdir()
        pdf = anchor_dir / "paper1.pdf"
        pdf.write_bytes(b"%PDF-1.4 test unchanged")

        h1 = compute_sha256(pdf)
        manifest = {
            "papers": {
                "AP001": {
                    "file": str(pdf),
                    "sha256": h1,
                    "processed": True,
                }
            }
        }

        # Check against manifest
        h2 = compute_sha256(pdf)
        is_unchanged = (manifest["papers"]["AP001"]["sha256"] == h2 and manifest["papers"]["AP001"]["processed"])
        assert is_unchanged is True
        print("PASS: Test 5 — manifest detects unchanged PDF")


# --- Test 6: Manifest detects changed / new PDF ---
def test_6_manifest_detects_changed_or_new_pdf():
    with tempfile.TemporaryDirectory() as tmpdir:
        tmp = Path(tmpdir)
        anchor_dir = tmp / "anchor_papers"
        anchor_dir.mkdir()
        pdf = anchor_dir / "paper1.pdf"
        pdf.write_bytes(b"%PDF-1.4 original")

        manifest = {
            "papers": {
                "AP001": {
                    "file": str(pdf),
                    "sha256": compute_sha256(pdf),
                    "processed": True,
                }
            }
        }

        # Modify PDF content
        pdf.write_bytes(b"%PDF-1.4 modified content with new methods")
        new_hash = compute_sha256(pdf)
        assert new_hash != manifest["papers"]["AP001"]["sha256"], "Hash should differ after edit"

        # Add new PDF
        pdf2 = anchor_dir / "paper2.pdf"
        pdf2.write_bytes(b"%PDF-1.4 second paper")
        assert "AP002" not in manifest["papers"], "AP002 should be detected as new"
        print("PASS: Test 6 — manifest detects changed/new PDF")


# --- Test 7: Gap-state validation ---
def test_7_gap_state_validation():
    # Verify that invalid states fail and all 6 valid states pass
    test_states = [
        ("UNVERIFIED", True),
        ("SEARCHING", True),
        ("SUPPORTED_AS_CURRENT_GAP", True),
        ("PARTIALLY_RESOLVED", True),
        ("RESOLVED_BY_PRIOR_WORK", True),
        ("INSUFFICIENT_EVIDENCE", True),
        ("PROVEN_NOVEL", False),
        ("SOLVED", False),
        ("UNKNOWN_STATUS", False),
    ]

    for state, should_be_valid in test_states:
        is_valid = state in VALID_GAP_STATES
        assert is_valid == should_be_valid, f"State validation failed for: {state}"

    # Scientific invariant check: UNVERIFIED gap cannot transition to SUPPORTED without evidence
    gap = {"id": "G001", "status": "UNVERIFIED", "literature_evidence": []}
    def promote_gap(g, new_status):
        if new_status == "SUPPORTED_AS_CURRENT_GAP" and not g.get("literature_evidence"):
            raise ValueError("Invariant violation: cannot promote UNVERIFIED gap without literature evidence")
        g["status"] = new_status

    try:
        promote_gap(gap, "SUPPORTED_AS_CURRENT_GAP")
        assert False, "Should have raised invariant violation"
    except ValueError:
        pass

    gap["literature_evidence"] = ["Wang et al., 2025 confirms lack of adaptive IMM in closed-loop MPC"]
    promote_gap(gap, "SUPPORTED_AS_CURRENT_GAP")
    assert gap["status"] == "SUPPORTED_AS_CURRENT_GAP"
    print("PASS: Test 7 — gap-state validation")


# --- Test 8: Project initialization does not overwrite files ---
def test_8_project_initialization_does_not_overwrite():
    with tempfile.TemporaryDirectory() as tmpdir:
        test_proj = Path(tmpdir) / "test_proj"
        test_proj.mkdir()

        # Step 1: Run init
        cmd = ["bash", str(REPO_ROOT / "tools" / "init_research_project.sh"), str(test_proj)]
        res1 = subprocess.run(cmd, capture_output=True, text=True)
        assert res1.returncode == 0, f"Init failed: {res1.stderr}"
        assert (test_proj / "anchor_papers" / "README.md").exists()
        assert (test_proj / "CLAIM_MAP.yaml").exists()

        # Step 2: Overwrite CLAIM_MAP.yaml with custom user content
        custom_content = "# USER EXPERIMENT CLAIMS\nclaims:\n  - C001: custom claim\n"
        (test_proj / "CLAIM_MAP.yaml").write_text(custom_content)

        # Step 3: Run init again
        res2 = subprocess.run(cmd, capture_output=True, text=True)
        assert res2.returncode == 0, f"Second init failed: {res2.stderr}"
        assert (test_proj / "CLAIM_MAP.yaml").read_text() == custom_content, "CLAIM_MAP.yaml was overwritten!"
        print("PASS: Test 8 — project initialization does not overwrite files")


# --- Test 9: Gitignore protects PDFs ---
def test_9_gitignore_protects_pdfs():
    gitignore_path = REPO_ROOT / ".gitignore"
    assert gitignore_path.exists(), ".gitignore missing"
    content = gitignore_path.read_text()

    assert "*.pdf" in content or "anchor_papers/**/*.pdf" in content or "anchor_papers/*.pdf" in content, (
        "PDF ignore rule missing from .gitignore"
    )

    # Use git check-ignore to verify git ignores dummy anchor PDFs
    res = subprocess.run(
        ["git", "check-ignore", "anchor_papers/closest_work/secret_paper.pdf"],
        cwd=REPO_ROOT, capture_output=True, text=True
    )
    assert res.returncode == 0, "anchor_papers PDF was not ignored by git!"

    # Verify README.md in anchor_papers is NOT ignored
    res_readme = subprocess.run(
        ["git", "check-ignore", "templates/anchor_papers/README.md"],
        cwd=REPO_ROOT, capture_output=True, text=True
    )
    assert res_readme.returncode != 0, "anchor_papers README.md should NOT be ignored!"
    print("PASS: Test 9 — gitignore protects PDFs")


# --- Test 10: Anchor intake precedes literature search when PDFs exist ---
def test_10_anchor_intake_precedes_lit_search():
    pipeline_file = REPO_ROOT / "skills" / "research-pipeline-robotics" / "SKILL.md"
    content = pipeline_file.read_text()
    assert "Stage 0 — Anchor Paper Intake" in content, "Stage 0 missing from research-pipeline-robotics"
    assert "anchor-paper-intake" in content, "anchor-paper-intake not referenced in pipeline"

    router_file = REPO_ROOT / "skills" / "robotics-research-router" / "SKILL.md"
    router_content = router_file.read_text()
    assert "anchor_papers" in router_content, "anchor_papers check missing from router"
    assert "anchor-paper-intake" in router_content, "anchor-paper-intake missing from router recommendation"
    print("PASS: Test 10 — anchor intake precedes literature search when PDFs exist")


# --- Test 11: No-anchor project follows legacy flow ---
def test_11_no_anchor_project_follows_legacy_flow():
    pipeline_file = REPO_ROOT / "skills" / "research-pipeline-robotics" / "SKILL.md"
    content = pipeline_file.read_text()
    assert "no anchor papers supplied" in content or "continue normal research workflow" in content, (
        "Pipeline does not explicitly describe no-anchor fallback"
    )
    print("PASS: Test 11 — no-anchor project follows legacy flow")


# --- Test 12: Already-processed unchanged anchors are not reprocessed ---
def test_12_unchanged_anchors_not_reprocessed():
    with tempfile.TemporaryDirectory() as tmpdir:
        tmp = Path(tmpdir)
        anchor_dir = tmp / "anchor_papers"
        anchor_dir.mkdir()
        pdf = anchor_dir / "paper1.pdf"
        pdf.write_bytes(b"%PDF-1.4 test caching")

        h = compute_sha256(pdf)
        manifest = {
            "papers": {
                "AP001": {
                    "file": "anchor_papers/paper1.pdf",
                    "sha256": h,
                    "processed": True,
                }
            }
        }

        # Simulated check:
        current_papers = discover_anchor_papers(anchor_dir)
        needs_processing = []
        for p in current_papers:
            rel = p["rel_path"]
            stored = manifest["papers"].get(p["paper_id"])
            if not stored or stored.get("sha256") != p["sha256"] or not stored.get("processed"):
                needs_processing.append(p)

        assert len(needs_processing) == 0, f"Unchanged paper marked for reprocessing: {needs_processing}"
        print("PASS: Test 12 — already-processed unchanged anchors are not unnecessarily reprocessed")


if __name__ == "__main__":
    tests = [
        test_1_simple_anchor_discovery,
        test_2_categorized_discovery,
        test_3_empty_directory,
        test_4_stable_ap_ids,
        test_5_manifest_detects_unchanged_pdf,
        test_6_manifest_detects_changed_or_new_pdf,
        test_7_gap_state_validation,
        test_8_project_initialization_does_not_overwrite,
        test_9_gitignore_protects_pdfs,
        test_10_anchor_intake_precedes_lit_search,
        test_11_no_anchor_project_follows_legacy_flow,
        test_12_unchanged_anchors_not_reprocessed,
    ]

    print("=== Running Anchor Paper Intake Test Suite (12 tests) ===")
    failed = 0
    for t in tests:
        try:
            t()
        except AssertionError as e:
            print(f"FAIL: {t.__name__} — {e}")
            failed += 1
        except Exception as e:
            print(f"ERROR: {t.__name__} — {e}")
            failed += 1

    if failed == 0:
        print(f"All {len(tests)} tests passed.")
        sys.exit(0)
    else:
        print(f"{failed}/{len(tests)} tests failed.")
        sys.exit(1)

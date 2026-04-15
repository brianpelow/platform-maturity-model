"""Tests for maturity assessors."""

import tempfile
from pathlib import Path
from maturity.assessors.repo import assess_from_repos
from maturity.assessors.scorer import compute_assessment


def test_assess_empty_dir() -> None:
    with tempfile.TemporaryDirectory() as tmpdir:
        assessments = assess_from_repos([Path(tmpdir)])
        assert len(assessments) == 6
        for da in assessments:
            assert da.assessed_level >= 1


def test_assess_well_structured_repo() -> None:
    with tempfile.TemporaryDirectory() as tmpdir:
        path = Path(tmpdir)
        (path / ".github" / "workflows").mkdir(parents=True)
        (path / ".github" / "workflows" / "ci.yml").write_text("name: CI\n")
        (path / ".github" / "workflows" / "nightly-agent.yml").write_text(
            "name: Nightly\non:\n  schedule:\n    - cron: '0 2 * * *'\njobs:\n  agent:\n    runs-on: ubuntu-latest\n"
        )
        (path / ".github" / "CODEOWNERS").write_text("* @owner\n")
        (path / "CONTRIBUTING.md").write_text("# Contributing")
        (path / "CHANGELOG.md").write_text("# Changelog")
        (path / "docs" / "adr").mkdir(parents=True)
        (path / "tests").mkdir()
        (path / "tests" / "test_main.py").write_text("def test_x(): pass")

        assessments = assess_from_repos([path])
        delivery = next(a for a in assessments if a.domain == "Delivery")
        assert delivery.assessed_level >= 2


def test_compute_assessment() -> None:
    with tempfile.TemporaryDirectory() as tmpdir:
        assessments = assess_from_repos([Path(tmpdir)])
        result = compute_assessment("test-org", assessments)
        assert result.overall_level >= 1
        assert result.overall_level <= 5
        assert result.overall_score > 0
        assert result.org == "test-org"
        assert result.assessed_at != ""


def test_compute_assessment_industry() -> None:
    with tempfile.TemporaryDirectory() as tmpdir:
        assessments = assess_from_repos([Path(tmpdir)])
        result = compute_assessment("test", assessments, industry="manufacturing")
        assert result.industry == "manufacturing"
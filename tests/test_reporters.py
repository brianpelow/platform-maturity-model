"""Tests for reporters."""

from maturity.model.evidence import MaturityAssessment, DomainAssessment
from maturity.reporters.narrator import generate_roadmap
from maturity.reporters.markdown import generate_report


def make_assessment(level: int = 2) -> MaturityAssessment:
    domains = [
        DomainAssessment(domain="Delivery", assessed_level=level,
            gaps=["Add golden path CI/CD"], strengths=["CI workflows present"]),
        DomainAssessment(domain="Reliability", assessed_level=max(1, level-1),
            gaps=["Define SLOs"], strengths=[]),
        DomainAssessment(domain="Security", assessed_level=level,
            gaps=["Add SAST scanning"], strengths=[]),
        DomainAssessment(domain="Developer Experience", assessed_level=level,
            gaps=["Add developer portal"], strengths=["CONTRIBUTING.md present"]),
        DomainAssessment(domain="Observability", assessed_level=max(1, level-1),
            gaps=["Add distributed tracing"], strengths=[]),
        DomainAssessment(domain="Governance", assessed_level=level,
            gaps=["Automate compliance evidence"], strengths=["CODEOWNERS defined"]),
    ]
    return MaturityAssessment(
        org="test-org",
        assessed_at="2026-04-12T00:00:00+00:00",
        industry="fintech",
        overall_level=level,
        overall_score=float(level),
        domains=domains,
        narrative="Test narrative.",
        top_strengths=["CI workflows present"],
        critical_gaps=["Define SLOs"],
        roadmap=[],
    )


def test_generate_roadmap() -> None:
    assessment = make_assessment(level=2)
    roadmap = generate_roadmap(assessment, target_level=3)
    assert len(roadmap) > 0
    assert all(isinstance(r, str) for r in roadmap)


def test_generate_roadmap_at_target() -> None:
    assessment = make_assessment(level=5)
    roadmap = generate_roadmap(assessment, target_level=5)
    assert len(roadmap) > 0


def test_generate_report_contains_sections() -> None:
    assessment = make_assessment()
    report = generate_report(assessment)
    assert "# Platform Engineering Maturity Report" in report
    assert "## Domain scores" in report
    assert "## Critical gaps" in report
    assert "## Recommended roadmap" in report


def test_generate_report_includes_level() -> None:
    assessment = make_assessment(level=3)
    report = generate_report(assessment)
    assert "Level 3" in report or "Defined" in report
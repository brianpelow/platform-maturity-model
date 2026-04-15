"""Maturity scoring engine."""

from __future__ import annotations

from datetime import datetime, timezone
from maturity.model.evidence import DomainAssessment, MaturityAssessment
from maturity.model.levels import CAPABILITY_DOMAINS


def compute_assessment(
    org: str,
    domain_assessments: list[DomainAssessment],
    industry: str = "fintech",
) -> MaturityAssessment:
    """Compute overall maturity assessment from domain scores."""
    total_weight = sum(d.weight for d in CAPABILITY_DOMAINS)
    weighted_sum = 0.0

    domain_map = {d.domain: d for d in domain_assessments}

    for domain_def in CAPABILITY_DOMAINS:
        da = domain_map.get(domain_def.name)
        level = da.assessed_level if da else 1
        weighted_sum += level * domain_def.weight

    overall_score = weighted_sum / total_weight
    overall_level = max(1, min(5, round(overall_score)))

    strengths = []
    gaps = []
    for da in domain_assessments:
        strengths.extend(da.strengths[:1])
        gaps.extend(da.gaps[:1])

    return MaturityAssessment(
        org=org,
        assessed_at=datetime.now(timezone.utc).isoformat(),
        industry=industry,
        overall_level=overall_level,
        overall_score=round(overall_score, 2),
        domains=domain_assessments,
        top_strengths=strengths[:5],
        critical_gaps=gaps[:5],
    )
"""AI-powered maturity narrative generator."""

from __future__ import annotations

import os
from maturity.model.evidence import MaturityAssessment
from maturity.core.config import MaturityConfig


def generate_narrative(assessment: MaturityAssessment, config: MaturityConfig) -> str:
    """Generate an executive maturity narrative using Claude."""
    if config.has_api_key:
        return _ai_narrative(assessment, config)
    return _template_narrative(assessment)


def _ai_narrative(assessment: MaturityAssessment, config: MaturityConfig) -> str:
    try:
        from openai import OpenAI
        client = OpenAI(base_url="https://openrouter.ai/api/v1", api_key=config.openrouter_api_key)

        domain_summary = "\n".join(
            f"- {d.domain}: Level {d.assessed_level}/5 ({d.confidence} confidence)"
            for d in assessment.domains
        )

        prompt = f"""You are a platform engineering advisor writing a maturity assessment for a {config.industry} engineering organization.

Organization: {assessment.org or "Engineering organization"}
Overall maturity: Level {assessment.overall_level}/5 ({assessment.level_name})
Overall score: {assessment.overall_score:.1f}/5.0
Industry: {config.industry}

Domain scores:
{domain_summary}

Top strengths: {', '.join(assessment.top_strengths[:3]) or 'none identified'}
Critical gaps: {', '.join(assessment.critical_gaps[:3]) or 'none identified'}

Write a 4-paragraph executive assessment:
1. Overall platform maturity posture and what it means competitively
2. Key strengths and what they enable the business to do
3. Critical gaps and their business risk implications for {config.industry}
4. Investment priorities for reaching the next maturity level

Write for a CTO/board audience. Be specific about {config.industry} implications (regulatory, competitive, operational).
Be honest, data-driven, and actionable."""

        message = client.chat.completions.create(
            model="meta-llama/llama-3.1-8b-instruct:free",
            max_tokens=700,
            messages=[{"role": "user", "content": prompt}],
        )
        return message.choices[0].message.content
    except Exception:
        return _template_narrative(assessment)


def _template_narrative(assessment: MaturityAssessment) -> str:
    posture = {
        1: "nascent â€” significant foundational investment required",
        2: "developing â€” basic capabilities established, standardization needed",
        3: "established â€” solid foundation, optimization opportunities ahead",
        4: "advanced â€” data-driven and proactive, approaching industry leadership",
        5: "industry-leading â€” continuous improvement and AI-augmentation achieved",
    }.get(assessment.overall_level, "developing")

    return f"""## Platform Engineering Maturity Assessment

**Overall maturity: Level {assessment.overall_level}/5 â€” {assessment.level_name}**

The {assessment.org or "engineering organization"} platform engineering capability is **{posture}**.
The overall maturity score of {assessment.overall_score:.1f}/5.0 reflects a {assessment.level_name.lower()} state
across {len(assessment.domains)} assessed capability domains in the {assessment.industry} context.

**Strengths**: {'. '.join(assessment.top_strengths[:3]) if assessment.top_strengths else 'Foundation capabilities are in place.'}
These capabilities provide a solid base for continued platform investment.

**Critical gaps**: {'. '.join(assessment.critical_gaps[:3]) if assessment.critical_gaps else 'No critical gaps identified at this level.'}
Addressing these gaps is the highest-leverage investment for reaching Level {min(5, assessment.overall_level + 1)}.

**Investment priority**: Focus platform team capacity on closing the identified gaps,
targeting Level {min(5, assessment.overall_level + 1)} ({
{2: 'Managed', 3: 'Defined', 4: 'Measured', 5: 'Optimizing'}.get(min(5, assessment.overall_level + 1), 'Optimizing')
}) within the next 2-3 quarters.
In {assessment.industry}, moving from Level {assessment.overall_level} to {min(5, assessment.overall_level + 1)}
typically reduces incident MTTR by 40% and deployment lead time by 60%.
"""


def generate_roadmap(assessment: MaturityAssessment, target_level: int = 0) -> list[str]:
    """Generate a prioritized roadmap for leveling up."""
    target = target_level or min(5, assessment.overall_level + 1)
    roadmap = []

    for da in sorted(assessment.domains, key=lambda d: d.assessed_level):
        if da.assessed_level < target:
            for gap in da.gaps[:2]:
                roadmap.append(f"[{da.domain}] Implement: {gap}")

    if not roadmap:
        roadmap.append(f"Organization is at or above target Level {target}. Focus on Level 5 optimizations.")

    return roadmap[:10]
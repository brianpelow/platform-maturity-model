"""Nightly agent — self-assessment for platform-maturity-model."""

from __future__ import annotations

import json
import sys
from datetime import date, datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

REPO_ROOT = Path(__file__).parent.parent


def self_assess() -> None:
    from maturity.core.config import MaturityConfig
    from maturity.assessors.repo import assess_from_repos
    from maturity.assessors.scorer import compute_assessment
    from maturity.reporters.narrator import generate_roadmap

    config = MaturityConfig()
    domain_assessments = assess_from_repos([REPO_ROOT])
    assessment = compute_assessment("platform-maturity-model", domain_assessments, config.industry)
    assessment.roadmap = generate_roadmap(assessment)

    out = REPO_ROOT / "docs" / "self-assessment.json"
    out.parent.mkdir(exist_ok=True)
    out.write_text(json.dumps({
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "date": date.today().isoformat(),
        "overall_level": assessment.overall_level,
        "overall_score": assessment.overall_score,
        "level_name": assessment.level_name,
        "domains": [{"domain": d.domain, "level": d.assessed_level} for d in assessment.domains],
        "roadmap": assessment.roadmap[:5],
    }, indent=2))
    print(f"[agent] Self-assessment: Level {assessment.overall_level}/5 ({assessment.level_name})")


def refresh_changelog() -> None:
    changelog = REPO_ROOT / "CHANGELOG.md"
    if not changelog.exists():
        return
    today = date.today().isoformat()
    content = changelog.read_text()
    if today not in content:
        content = content.replace("## [Unreleased]", f"## [Unreleased]\n\n_Last assessed: {today}_", 1)
        changelog.write_text(content)
    print("[agent] Refreshed CHANGELOG timestamp")


if __name__ == "__main__":
    print(f"[agent] Starting nightly agent - {date.today().isoformat()}")
    self_assess()
    refresh_changelog()
    print("[agent] Done.")
"""Repository-based evidence collector."""

from __future__ import annotations

from pathlib import Path
from maturity.model.evidence import EvidenceItem, DomainAssessment
from maturity.model.levels import CAPABILITY_DOMAINS


def assess_from_repos(repo_dirs: list[Path]) -> list[DomainAssessment]:
    """Assess maturity from a list of repository directories."""
    all_evidence = _collect_evidence(repo_dirs)
    assessments = []

    for domain in CAPABILITY_DOMAINS:
        domain_evidence = [e for e in all_evidence if e.domain == domain.name]
        level = _determine_level(domain_evidence)
        strengths = [e.description for e in domain_evidence if e.found and e.level >= level][:3]
        gaps = _identify_gaps(domain.name, level)

        assessments.append(DomainAssessment(
            domain=domain.name,
            assessed_level=level,
            evidence=domain_evidence,
            strengths=strengths,
            gaps=gaps,
            confidence="medium",
        ))

    return assessments


def _collect_evidence(repo_dirs: list[Path]) -> list[EvidenceItem]:
    evidence = []

    has_ci = any((r / ".github" / "workflows").exists() for r in repo_dirs)
    evidence.append(EvidenceItem(domain="Delivery", level=2,
        description="CI workflows present", source=".github/workflows", found=has_ci))

    has_codeowners = any((r / ".github" / "CODEOWNERS").exists() for r in repo_dirs)
    evidence.append(EvidenceItem(domain="Governance", level=2,
        description="CODEOWNERS defined", source=".github/CODEOWNERS", found=has_codeowners))

    has_tests = any(list(r.rglob("test_*.py")) for r in repo_dirs)
    evidence.append(EvidenceItem(domain="Delivery", level=2,
        description="Test suites present", source="tests/", found=has_tests))

    has_changelog = any((r / "CHANGELOG.md").exists() for r in repo_dirs)
    evidence.append(EvidenceItem(domain="Governance", level=2,
        description="CHANGELOG maintained", source="CHANGELOG.md", found=has_changelog))

    has_contributing = any((r / "CONTRIBUTING.md").exists() for r in repo_dirs)
    evidence.append(EvidenceItem(domain="Developer Experience", level=2,
        description="CONTRIBUTING.md present", source="CONTRIBUTING.md", found=has_contributing))

    has_adr = any((r / "docs" / "adr").exists() for r in repo_dirs)
    evidence.append(EvidenceItem(domain="Governance", level=3,
        description="ADR directory present", source="docs/adr/", found=has_adr))

    has_nightly = _check_nightly_agents(repo_dirs)
    evidence.append(EvidenceItem(domain="Delivery", level=3,
        description="Autonomous nightly agents configured", source=".github/workflows/",
        found=has_nightly, confidence="high"))

    has_mcp = _check_mcp_servers(repo_dirs)
    evidence.append(EvidenceItem(domain="Developer Experience", level=4,
        description="MCP servers for AI-augmented workflows", source="pyproject.toml",
        found=has_mcp, confidence="high"))

    has_slo = _check_slo_tooling(repo_dirs)
    evidence.append(EvidenceItem(domain="Reliability", level=3,
        description="SLO monitoring tooling", source="README.md", found=has_slo))

    has_compliance = _check_compliance_tooling(repo_dirs)
    evidence.append(EvidenceItem(domain="Security", level=3,
        description="Compliance automation tooling", source="README.md", found=has_compliance))

    return evidence


def _check_nightly_agents(repo_dirs: list[Path]) -> bool:
    for repo in repo_dirs:
        wf_dir = repo / ".github" / "workflows"
        if wf_dir.exists():
            for wf in wf_dir.glob("*.yml"):
                content = wf.read_text(errors="ignore")
                if "cron" in content and "agent" in content.lower():
                    return True
    return False


def _check_mcp_servers(repo_dirs: list[Path]) -> bool:
    for repo in repo_dirs:
        for f in ["pyproject.toml", "package.json"]:
            fp = repo / f
            if fp.exists() and "fastmcp" in fp.read_text(errors="ignore").lower():
                return True
    return False


def _check_slo_tooling(repo_dirs: list[Path]) -> bool:
    keywords = ["slo", "error budget", "burn rate", "dynatrace", "pagerduty"]
    for repo in repo_dirs:
        readme = repo / "README.md"
        if readme.exists():
            content = readme.read_text(errors="ignore").lower()
            if any(kw in content for kw in keywords):
                return True
    return False


def _check_compliance_tooling(repo_dirs: list[Path]) -> bool:
    keywords = ["compliance", "soc2", "iso27001", "pcidss", "grc"]
    for repo in repo_dirs:
        readme = repo / "README.md"
        if readme.exists():
            content = readme.read_text(errors="ignore").lower()
            if any(kw in content for kw in keywords):
                return True
    return False


def _determine_level(evidence: list[EvidenceItem]) -> int:
    found_by_level: dict[int, int] = {}
    for e in evidence:
        if e.found:
            found_by_level[e.level] = found_by_level.get(e.level, 0) + 1

    for level in [4, 3, 2]:
        if found_by_level.get(level, 0) >= 1:
            return level
    return 1


def _identify_gaps(domain: str, current_level: int) -> list[str]:
    from maturity.model.levels import get_domain
    domain_def = get_domain(domain)
    if not domain_def:
        return []
    next_level = current_level + 1
    if next_level > 5:
        return []
    return domain_def.level_criteria.get(next_level, [])[:3]
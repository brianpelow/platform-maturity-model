"""Platform engineering maturity level definitions."""

from __future__ import annotations

from pydantic import BaseModel, Field


class MaturityLevel(BaseModel):
    """Definition of a maturity level."""

    level: int
    name: str
    description: str
    characteristics: list[str] = Field(default_factory=list)
    key_outcomes: list[str] = Field(default_factory=list)


class CapabilityDomain(BaseModel):
    """A platform engineering capability domain."""

    name: str
    description: str
    weight: float = Field(1.0, description="Relative weight in overall score")
    level_criteria: dict[int, list[str]] = Field(default_factory=dict)


MATURITY_LEVELS: list[MaturityLevel] = [
    MaturityLevel(level=1, name="Initial",
        description="Ad-hoc processes, hero-driven, high toil, reactive",
        characteristics=["Manual deployments", "No SLOs defined", "Firefighting culture",
                         "Siloed teams", "No self-service"],
        key_outcomes=["Basic CI exists", "Teams can deploy independently"]),
    MaturityLevel(level=2, name="Managed",
        description="Repeatable processes, basic automation, some standardization",
        characteristics=["Automated CI/CD pipelines", "Basic monitoring", "Incident process defined",
                         "Some golden paths", "Documentation improving"],
        key_outcomes=["Deployment frequency increasing", "MTTR measurable", "On-call process defined"]),
    MaturityLevel(level=3, name="Defined",
        description="Standardized processes, self-service emerging, data-informed",
        characteristics=["Golden path templates", "Developer portal", "SLOs defined and tracked",
                         "DORA metrics measured", "Security scanning automated"],
        key_outcomes=["Self-service for 50%+ of tasks", "DORA metrics at high band",
                      "Compliance automation in place"]),
    MaturityLevel(level=4, name="Measured",
        description="Data-driven decisions, proactive reliability, platform as product",
        characteristics=["DORA at elite band", "Error budget management", "Predictive alerting",
                         "Developer NPS tracked", "Cost optimization automated"],
        key_outcomes=["Elite DORA performance", "AI-augmented operations",
                      "Platform team as product team"]),
    MaturityLevel(level=5, name="Optimizing",
        description="Continuous improvement, AI-augmented, industry-leading",
        characteristics=["AI-driven incident response", "Autonomous pipeline healing",
                         "Continuous compliance", "Industry benchmark contributor"],
        key_outcomes=["Industry-leading delivery", "Regulatory excellence",
                      "Platform enables business differentiation"]),
]

CAPABILITY_DOMAINS: list[CapabilityDomain] = [
    CapabilityDomain(name="Delivery", description="CI/CD, deployment practices, release management",
        weight=1.2,
        level_criteria={
            1: ["Manual deployments", "No CI"],
            2: ["Automated CI", "Basic CD"],
            3: ["Golden path CI/CD", "Feature flags"],
            4: ["Elite DORA metrics", "Progressive delivery"],
            5: ["AI-augmented delivery", "Autonomous releases"],
        }),
    CapabilityDomain(name="Reliability", description="SLOs, incident response, MTTR, availability",
        weight=1.2,
        level_criteria={
            1: ["No SLOs", "Reactive incidents"],
            2: ["Basic monitoring", "Incident process"],
            3: ["SLOs defined", "Runbooks automated"],
            4: ["Error budgets", "Proactive reliability"],
            5: ["AI incident response", "Self-healing systems"],
        }),
    CapabilityDomain(name="Security", description="Shift-left security, compliance, CVE management",
        weight=1.1,
        level_criteria={
            1: ["Manual security reviews", "No SAST"],
            2: ["Basic SAST/SCA", "Vulnerability scanning"],
            3: ["Security in CI", "Compliance automation"],
            4: ["Policy as code", "Continuous compliance"],
            5: ["Zero-trust automation", "Predictive security"],
        }),
    CapabilityDomain(name="Developer Experience", description="Self-service, onboarding, tooling, productivity",
        weight=1.0,
        level_criteria={
            1: ["Long onboarding", "No self-service"],
            2: ["Basic docs", "Some templates"],
            3: ["Developer portal", "Golden paths"],
            4: ["NPS tracked", "Friction eliminated"],
            5: ["AI pair programming", "10x developer productivity"],
        }),
    CapabilityDomain(name="Observability", description="Metrics, logging, tracing, alerting",
        weight=1.0,
        level_criteria={
            1: ["Basic logging", "Manual monitoring"],
            2: ["Metrics dashboards", "Basic alerts"],
            3: ["Distributed tracing", "SLO dashboards"],
            4: ["Anomaly detection", "Predictive alerts"],
            5: ["AI root cause analysis", "Full observability"],
        }),
    CapabilityDomain(name="Governance", description="Change management, audit trails, compliance",
        weight=0.8,
        level_criteria={
            1: ["Manual change control", "No audit trail"],
            2: ["Basic change process", "Some logging"],
            3: ["Automated change evidence", "Compliance reports"],
            4: ["Continuous compliance", "Audit automation"],
            5: ["Real-time compliance", "Regulatory excellence"],
        }),
]


def get_level(level: int) -> MaturityLevel | None:
    return next((l for l in MATURITY_LEVELS if l.level == level), None)


def get_domain(name: str) -> CapabilityDomain | None:
    return next((d for d in CAPABILITY_DOMAINS if d.name == name), None)
"""Evidence models for maturity assessment."""

from __future__ import annotations

from pydantic import BaseModel, Field
from typing import Optional


class EvidenceItem(BaseModel):
    """A single piece of evidence supporting a maturity level."""

    domain: str
    level: int
    description: str
    source: str = ""
    confidence: str = Field("medium", description="high/medium/low")
    found: bool = False


class DomainAssessment(BaseModel):
    """Assessment result for a single capability domain."""

    domain: str
    assessed_level: int = 1
    evidence: list[EvidenceItem] = Field(default_factory=list)
    strengths: list[str] = Field(default_factory=list)
    gaps: list[str] = Field(default_factory=list)
    confidence: str = "medium"

    @property
    def evidence_count(self) -> int:
        return sum(1 for e in self.evidence if e.found)


class MaturityAssessment(BaseModel):
    """Complete platform maturity assessment."""

    org: str = ""
    assessed_at: str = ""
    industry: str = "fintech"
    overall_level: int = 1
    overall_score: float = 0.0
    domains: list[DomainAssessment] = Field(default_factory=list)
    narrative: str = ""
    top_strengths: list[str] = Field(default_factory=list)
    critical_gaps: list[str] = Field(default_factory=list)
    roadmap: list[str] = Field(default_factory=list)

    @property
    def level_name(self) -> str:
        names = {1: "Initial", 2: "Managed", 3: "Defined", 4: "Measured", 5: "Optimizing"}
        return names.get(self.overall_level, "Unknown")
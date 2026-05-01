"""Configuration for platform-maturity-model."""

from __future__ import annotations

import os
from pydantic import BaseModel, Field


class MaturityConfig(BaseModel):
    """Runtime configuration for platform-maturity-model."""

    openrouter_api_key: str = Field("", description="OpenRouter API key")
    github_token: str = Field("", description="GitHub API token")
    industry: str = Field("fintech", description="Industry context")
    org: str = Field("", description="GitHub organization")

    @classmethod
    def from_env(cls) -> "MaturityConfig":
        return cls(
            openrouter_api_key=os.environ.get("OPENROUTER_API_KEY", ""),
            github_token=os.environ.get("GITHUB_TOKEN", ""),
            industry=os.environ.get("MATURITY_INDUSTRY", "fintech"),
            org=os.environ.get("GITHUB_ORG", ""),
        )

    @property
    def has_api_key(self) -> bool:
        return bool(self.openrouter_api_key)
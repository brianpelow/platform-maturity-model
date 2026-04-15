# platform-maturity-model

> Open framework and CLI for assessing platform engineering maturity — 5-level model with automated evidence collection.

![CI](https://github.com/brianpelow/platform-maturity-model/actions/workflows/ci.yml/badge.svg)
![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)
![Python](https://img.shields.io/badge/python-3.12+-green.svg)

## Overview

`platform-maturity-model` provides a structured, evidence-based framework
for assessing and improving platform engineering maturity. It maps your
organization across 6 capability domains and 5 maturity levels, collects
automated evidence from your repos and tooling, and generates a prioritized
roadmap for leveling up.

Built for VP/CTO-level leaders in regulated financial services and
manufacturing who need to communicate platform investment priorities
to boards and leadership teams with data-backed justification.

## Maturity levels

| Level | Name | Description |
|-------|------|-------------|
| 1 | Initial | Ad-hoc, manual, hero-driven |
| 2 | Managed | Repeatable processes, basic automation |
| 3 | Defined | Standardized, documented, self-service emerging |
| 4 | Measured | Data-driven, SLOs defined, proactive |
| 5 | Optimizing | Continuous improvement, AI-augmented, industry-leading |

## Capability domains

- **Delivery** — CI/CD, deployment frequency, lead time
- **Reliability** — SLOs, incident response, MTTR
- **Security** — Shift-left, compliance automation, CVE management
- **Developer Experience** — Self-service, onboarding, tooling
- **Observability** — Metrics, logging, tracing, alerting
- **Governance** — Change management, audit trails, compliance

## Quick start

```bash
pip install platform-maturity-model

platform-maturity assess --repo-dir ./my-services
platform-maturity report --format markdown
platform-maturity roadmap --target-level 4
```

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md).

## License

Apache 2.0
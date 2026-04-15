"""Tests for maturity level definitions."""

from maturity.model.levels import MATURITY_LEVELS, CAPABILITY_DOMAINS, get_level, get_domain


def test_five_maturity_levels() -> None:
    assert len(MATURITY_LEVELS) == 5
    assert [l.level for l in MATURITY_LEVELS] == [1, 2, 3, 4, 5]


def test_level_names() -> None:
    names = {l.level: l.name for l in MATURITY_LEVELS}
    assert names[1] == "Initial"
    assert names[3] == "Defined"
    assert names[5] == "Optimizing"


def test_six_capability_domains() -> None:
    assert len(CAPABILITY_DOMAINS) == 6


def test_domain_names() -> None:
    names = {d.name for d in CAPABILITY_DOMAINS}
    assert "Delivery" in names
    assert "Reliability" in names
    assert "Security" in names
    assert "Developer Experience" in names
    assert "Observability" in names
    assert "Governance" in names


def test_get_level() -> None:
    level = get_level(3)
    assert level is not None
    assert level.name == "Defined"


def test_get_level_none() -> None:
    assert get_level(99) is None


def test_get_domain() -> None:
    domain = get_domain("Delivery")
    assert domain is not None
    assert domain.weight > 0


def test_all_levels_have_characteristics() -> None:
    for level in MATURITY_LEVELS:
        assert len(level.characteristics) > 0
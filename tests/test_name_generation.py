"""Tests for locale name generation — parametrized across all registered locales."""

import random
import pytest
from medsynth.locales import load_locale, REGISTRY

ALL_LOCALES = sorted(REGISTRY.keys())


@pytest.mark.parametrize("code", ALL_LOCALES)
def test_name_returns_required_keys(code):
    locale = load_locale(code)
    rng = random.Random(42)
    name = locale.generate_name("male", rng)
    assert isinstance(name, dict)
    assert "first_name" in name, f"{code}: missing 'first_name' key"
    assert "last_name" in name, f"{code}: missing 'last_name' key"
    assert "full_name" in name, f"{code}: missing 'full_name' key"


@pytest.mark.parametrize("code", ALL_LOCALES)
def test_full_name_contains_parts(code):
    locale = load_locale(code)
    rng = random.Random(42)
    name = locale.generate_name("male", rng)
    # full_name should contain the first_name somewhere
    assert name["first_name"] in name["full_name"], (
        f"{code}: first_name '{name['first_name']}' not in full_name '{name['full_name']}'"
    )


@pytest.mark.parametrize("code", ALL_LOCALES)
def test_both_genders_work(code):
    locale = load_locale(code)
    for gender in ("male", "female"):
        rng = random.Random(42)
        name = locale.generate_name(gender, rng)
        assert name["full_name"], f"{code}/{gender}: empty full_name"
        assert name["first_name"], f"{code}/{gender}: empty first_name"


@pytest.mark.parametrize("code", ALL_LOCALES)
def test_emergency_contact_name(code):
    locale = load_locale(code)
    rng = random.Random(42)
    name = locale.emergency_contact_name(rng)
    assert isinstance(name, str)
    assert " " in name  # should have at least two parts


@pytest.mark.parametrize("code", ALL_LOCALES)
def test_name_deterministic(code):
    locale = load_locale(code)
    name1 = locale.generate_name("male", random.Random(99))
    name2 = locale.generate_name("male", random.Random(99))
    assert name1 == name2


@pytest.mark.parametrize("code", ALL_LOCALES)
def test_name_variety(code):
    """Different seeds produce different names."""
    locale = load_locale(code)
    names = set()
    for seed in range(50):
        name = locale.generate_name("male", random.Random(seed))
        names.add(name["full_name"])
    assert len(names) > 5, f"{code}: only {len(names)} unique names from 50 seeds"

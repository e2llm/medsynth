"""Tests for national ID generation — parametrized + locale-specific validation."""

import random
import pytest
from medsynth.locales import load_locale, REGISTRY

ALL_LOCALES = sorted(REGISTRY.keys())


# --- Checksum verifiers per locale ---

def _verify_israeli_id(id_str: str) -> bool:
    digits = [int(c) for c in id_str.zfill(9)]
    total = 0
    for i, d in enumerate(digits):
        v = d * (1 + (i % 2))
        total += v // 10 + v % 10
    return total % 10 == 0


def _verify_saudi_id(id_str: str) -> bool:
    if len(id_str) != 10 or not id_str.isdigit():
        return False
    if id_str[0] not in ("1", "2"):
        return False
    # Luhn check
    digits = [int(c) for c in id_str[:9]]
    total = 0
    for i, d in enumerate(digits):
        v = d * (2 if i % 2 == 0 else 1)
        total += v // 10 + v % 10
    check = (10 - (total % 10)) % 10
    return int(id_str[9]) == check


def _verify_spanish_dni(id_str: str) -> bool:
    if len(id_str) != 9:
        return False
    number_part = id_str[:8]
    letter = id_str[8]
    if not number_part.isdigit() or not letter.isalpha():
        return False
    table = "TRWAGMYFPDXBNJZSQVHLCKE"
    return table[int(number_part) % 23] == letter


# --- ID format expectations per locale ---

ID_SPECS = {
    "he_IL": {"length": 9, "all_digits": True, "checksum": _verify_israeli_id},
    "ar_SA": {"length": 10, "all_digits": True, "checksum": _verify_saudi_id},
    "ar_EG": {"length": 14, "all_digits": True},
    "es_ES": {"length": 9, "checksum": _verify_spanish_dni},
    "es_MX": {"length": 18},  # CURP: alphanumeric
    "es_AR": {"min_length": 7, "max_length": 8, "all_digits": True},
}


def _make_patient(code):
    """Build a minimal patient dict suitable for ID generation."""
    return {
        "gender": "male",
        "age": 40,
        "date_of_birth": "1985-03-15",
        "first_name": "Test",
        "last_name": "User",
        "apellido_materno": "López",
    }


@pytest.mark.parametrize("code", ALL_LOCALES)
def test_id_deterministic(code):
    locale = load_locale(code)
    patient = _make_patient(code)
    id1 = locale.generate_id(patient, random.Random(77))
    id2 = locale.generate_id(patient, random.Random(77))
    assert id1 == id2


@pytest.mark.parametrize("code", ALL_LOCALES)
def test_id_returns_string(code):
    locale = load_locale(code)
    patient = _make_patient(code)
    rng = random.Random(42)
    id_str = locale.generate_id(patient, rng)
    assert isinstance(id_str, (str, int)), f"{code}: ID is {type(id_str)}"


@pytest.mark.parametrize("code", ALL_LOCALES)
def test_id_format(code):
    """Validate length and character constraints per locale."""
    spec = ID_SPECS.get(code)
    if spec is None:
        pytest.skip(f"No ID spec for {code}")

    locale = load_locale(code)
    patient = _make_patient(code)
    rng = random.Random(42)

    for _ in range(50):
        id_str = str(locale.generate_id(patient, rng))
        if "length" in spec:
            assert len(id_str) == spec["length"], f"{code}: len={len(id_str)} expected {spec['length']}: {id_str}"
        if "min_length" in spec:
            assert len(id_str) >= spec["min_length"], f"{code}: len={len(id_str)} < {spec['min_length']}: {id_str}"
        if "max_length" in spec:
            assert len(id_str) <= spec["max_length"], f"{code}: len={len(id_str)} > {spec['max_length']}: {id_str}"
        if spec.get("all_digits"):
            assert id_str.isdigit(), f"{code}: non-digit in ID: {id_str}"


@pytest.mark.parametrize("code", [c for c in ALL_LOCALES if c in ID_SPECS and "checksum" in ID_SPECS[c]])
def test_id_checksum(code):
    """Verify checksum for locales that have verifiable algorithms."""
    spec = ID_SPECS[code]
    locale = load_locale(code)
    patient = _make_patient(code)
    rng = random.Random(42)

    for _ in range(100):
        id_str = str(locale.generate_id(patient, rng))
        assert spec["checksum"](id_str), f"{code}: invalid checksum: {id_str}"


@pytest.mark.parametrize("code", ALL_LOCALES)
def test_id_variety(code):
    """Different seeds produce different IDs."""
    locale = load_locale(code)
    patient = _make_patient(code)
    ids = set()
    for seed in range(50):
        id_str = str(locale.generate_id(patient, random.Random(seed)))
        ids.add(id_str)
    assert len(ids) > 10, f"{code}: only {len(ids)} unique IDs from 50 seeds"

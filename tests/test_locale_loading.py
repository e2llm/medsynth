"""Tests for locale loading and validation — parametrized across all registered locales."""

import pytest
from medsynth.locales import load_locale, REGISTRY
from medsynth.locales.base import LocaleConfig, OcrPattern

ALL_LOCALES = sorted(REGISTRY.keys())


def test_load_unknown_raises():
    with pytest.raises(ValueError, match="Unknown locale"):
        load_locale("xx_XX")


def test_registry_not_empty():
    assert len(REGISTRY) >= 1


@pytest.mark.parametrize("code", ALL_LOCALES)
def test_load_locale(code):
    locale = load_locale(code)
    assert isinstance(locale, LocaleConfig)
    assert locale.code == code


@pytest.mark.parametrize("code", ALL_LOCALES)
def test_locale_config_completeness(code):
    locale = load_locale(code)
    assert len(locale.cities) > 0
    assert len(locale.streets) > 0
    assert len(locale.occupations) > 0
    assert len(locale.conditions) > 0
    assert len(locale.medications) > 0
    assert len(locale.departments) > 0
    assert len(locale.lab_tests) > 0
    assert len(locale.icd10_codes) > 0
    assert len(locale.facilities) > 0
    assert len(locale.facility_by_id) > 0
    assert len(locale.field_names) > 0
    assert len(locale.ocr_patterns) > 0
    assert len(locale.urgency_values) > 0
    assert locale.system_prompt
    assert locale.generic_location
    assert locale.address_format
    assert locale.generate_name is not None
    assert locale.generate_id is not None
    assert locale.emergency_contact_name is not None
    assert locale.format_patient_context is not None
    assert locale.format_clinical_prompt is not None


@pytest.mark.parametrize("code", ALL_LOCALES)
def test_ocr_patterns_valid(code):
    locale = load_locale(code)
    for p in locale.ocr_patterns:
        assert isinstance(p, OcrPattern)
        assert len(p.source) > 0
        # target may be empty (e.g. Arabic diacritic stripping)
        assert isinstance(p.target, str)
        assert p.weight > 0


@pytest.mark.parametrize("code", ALL_LOCALES)
def test_facility_ids_match_field_names(code):
    locale = load_locale(code)
    for fac in locale.facilities:
        assert fac["id"] in locale.field_names, f"Facility {fac['id']} missing from field_names"
        assert fac["id"] in locale.facility_by_id


@pytest.mark.parametrize("code", ALL_LOCALES)
def test_field_names_cover_required_concepts(code):
    locale = load_locale(code)
    required = {"patient_id", "patient_name", "age", "date", "free_text"}
    for fac_id, fnames in locale.field_names.items():
        for concept in required:
            assert concept in fnames, f"Facility {fac_id} missing concept {concept}"
            assert fnames[concept] is not None, f"Facility {fac_id} has None for {concept}"


@pytest.mark.parametrize("code", ALL_LOCALES)
def test_icd10_codes_cover_conditions(code):
    locale = load_locale(code)
    for condition in locale.conditions:
        assert condition in locale.icd10_codes, f"Condition '{condition}' missing ICD-10 code"


@pytest.mark.parametrize("code", ALL_LOCALES)
def test_lab_tests_structure(code):
    locale = load_locale(code)
    for test in locale.lab_tests:
        assert "name" in test
        assert "unit" in test
        assert "normal_range" in test
        assert "abnormal_range" in test
        assert len(test["normal_range"]) == 2
        assert len(test["abnormal_range"]) == 2


@pytest.mark.parametrize("code", ALL_LOCALES)
def test_facility_structure(code):
    locale = load_locale(code)
    for fac in locale.facilities:
        assert "id" in fac
        assert "name" in fac
        assert "doc_types" in fac
        assert "source" in fac
        assert "date_format" in fac
        assert "id_type" in fac
        assert fac["id_type"] in ("string", "int", "float")
        for dt in fac["doc_types"]:
            assert dt in fac["source"], f"Facility {fac['id']} missing source for {dt}"


@pytest.mark.parametrize("code", ALL_LOCALES)
def test_contradiction_templates(code):
    locale = load_locale(code)
    assert "smoking_yes" in locale.contradiction_templates
    assert "smoking_no" in locale.contradiction_templates
    assert "age" in locale.contradiction_templates
    assert "medication" in locale.contradiction_templates
    assert "{age}" in locale.contradiction_templates["age"]
    assert "{med}" in locale.contradiction_templates["medication"]


@pytest.mark.parametrize("code", ALL_LOCALES)
def test_fallback_strings(code):
    locale = load_locale(code)
    assert "no_diagnosis" in locale.fallback_strings
    assert "referral_default" in locale.fallback_strings

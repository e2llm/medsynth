"""Facility x DocType schema templates.

Each schema defines field mappings, types, and which fields exist for a
specific facility/doc-type combination.  The key insight: the SAME patient
concept (e.g. age) maps to different field names, types, and conventions
across facilities.
"""

from . import config
from .locales.base import LocaleConfig


def _age_value(patient: dict, facility: dict, rng, doc_date: str) -> object:
    """Return age in the facility's convention, computed from DOB + doc date."""
    from datetime import date as _date
    dob = _date.fromisoformat(patient["date_of_birth"])
    d = _date.fromisoformat(doc_date)
    age = (d - dob).days // 365
    if facility.get("age_format") == "range":
        bucket = config.AGE_RANGE_BUCKET
        low = (age // bucket) * bucket
        return f"{low}-{low + bucket}"
    return age


def _id_value(patient: dict, facility: dict) -> object:
    """Return patient ID in the facility's storage type."""
    raw = patient["id"]
    if facility["id_type"] == "int":
        return int(raw)
    if facility["id_type"] == "float":
        return float(int(raw))
    return raw


def _format_date(dt_str: str, facility: dict) -> str:
    """Format a date string according to facility convention."""
    from datetime import datetime
    dt = datetime.fromisoformat(dt_str)
    return dt.strftime(facility["date_format"])


def build_structured_fields(
    patient: dict,
    facility_id: str,
    doc_type: str,
    doc_date: str,
    rng,
    locale: LocaleConfig,
) -> dict:
    """Build the structured (non-free-text) fields for a document."""
    fnames = locale.field_names[facility_id]
    facility = locale.facility_by_id[facility_id]
    doc = {}

    def _set(concept: str, value):
        field = fnames.get(concept)
        if field is not None and value is not None:
            doc[field] = value

    # Universal fields
    _set("patient_id", _id_value(patient, facility))
    _set("patient_name", patient["full_name"])
    _set("age", _age_value(patient, facility, rng, doc_date))
    _set("gender", patient["gender"])
    _set("date", _format_date(doc_date, facility))
    _set("facility", facility["name"])
    _set("address", patient["address"])

    # Conditionally present fields
    _set("smoking", patient["smoking"])
    _set("blood_type", patient.get("blood_type"))
    _set("occupation", patient.get("occupation"))
    _set("conditions", patient.get("conditions"))
    _set("medications", patient.get("medications"))
    _set("icd10", patient.get("icd10_codes"))

    # Doc-type-specific fields
    if doc_type == "discharge":
        _set("department", rng.choice(locale.departments))
        _set("diagnosis", rng.choice(patient["conditions"]) if patient["conditions"] else locale.fallback_strings.get("no_diagnosis", ""))

    elif doc_type == "lab":
        num_tests = rng.randint(config.MIN_LAB_TESTS_PER_DOC, config.MAX_LAB_TESTS_PER_DOC)
        tests = rng.sample(locale.lab_tests, min(num_tests, len(locale.lab_tests)))
        lab_results = []
        for test in tests:
            is_abnormal = rng.random() < config.LAB_ABNORMAL_RATE
            r = test["abnormal_range"] if is_abnormal else test["normal_range"]
            if isinstance(r[0], float):
                value = round(rng.uniform(r[0], r[1]), 1)
            else:
                value = rng.randint(int(r[0]), int(r[1]))
            lab_results.append({
                fnames.get("lab_test_name", "test_name"): test["name"],
                fnames.get("lab_value", "result"): value,
                fnames.get("lab_unit", "units"): test["unit"],
                fnames.get("lab_reference", "ref_range"): f"{test['normal_range'][0]}-{test['normal_range'][1]}",
                fnames.get("lab_flag", "flag"): "H" if is_abnormal else "N",
            })
        doc["lab_results"] = lab_results

    elif doc_type == "visit":
        _set("department", rng.choice(locale.departments))
        _set("diagnosis", rng.choice(patient["conditions"]) if patient["conditions"] else locale.fallback_strings.get("no_diagnosis", ""))

    elif doc_type == "referral":
        _set("referral_to", rng.choice(locale.departments))
        _set("referral_reason", rng.choice(patient["conditions"]) if patient["conditions"] else locale.fallback_strings.get("referral_default", ""))
        _set("urgency", rng.choice(locale.urgency_values))

    doc["doc_type"] = doc_type
    return doc


# ---------------------------------------------------------------------------
# ES mapping types per facility x doctype
# ---------------------------------------------------------------------------

def get_es_mapping(facility_id: str, locale: LocaleConfig) -> dict:
    """Return ES mapping properties for a facility x doctype index."""
    fnames = locale.field_names[facility_id]
    facility = locale.facility_by_id[facility_id]
    props = {}

    def _add(concept: str, es_type: str, **kwargs):
        field = fnames.get(concept)
        if field is not None:
            mapping = {"type": es_type}
            mapping.update(kwargs)
            props[field] = mapping

    if facility["id_type"] == "int":
        _add("patient_id", "long")
    elif facility["id_type"] == "float":
        _add("patient_id", "float")
    else:
        _add("patient_id", "keyword")

    _add("patient_name", "text", fields={"keyword": {"type": "keyword"}})
    _add("facility", "keyword")
    _add("date", "keyword")
    _add("address", "text")

    if facility.get("age_format") == "range":
        _add("age", "keyword")
    else:
        _add("age", "integer")

    _add("gender", "keyword")
    _add("smoking", "boolean")
    _add("blood_type", "keyword")
    _add("occupation", "keyword")
    _add("conditions", "keyword")
    _add("medications", "keyword")
    _add("icd10", "keyword")
    _add("free_text", "text")
    _add("department", "keyword")
    _add("diagnosis", "text", fields={"keyword": {"type": "keyword"}})

    return props


def get_es_mapping_for_index(facility_id: str, doc_type: str, locale: LocaleConfig) -> dict:
    """Return full ES mapping for a facility x doctype index."""
    fnames = locale.field_names[facility_id]
    props = get_es_mapping(facility_id, locale)

    if doc_type == "lab":
        props["lab_results"] = {
            "type": "nested",
            "properties": {
                fnames.get("lab_test_name", "test_name"): {"type": "keyword"},
                fnames.get("lab_value", "result"): {"type": "float"},
                fnames.get("lab_unit", "units"): {"type": "keyword"},
                fnames.get("lab_reference", "ref_range"): {"type": "keyword"},
                fnames.get("lab_flag", "flag"): {"type": "keyword"},
            },
        }

    if doc_type == "referral":
        _fnames = fnames

        def _add_referral(concept, es_type, **kwargs):
            field = _fnames.get(concept)
            if field is not None:
                mapping = {"type": es_type}
                mapping.update(kwargs)
                props[field] = mapping

        _add_referral("referral_to", "keyword")
        _add_referral("referral_reason", "text")
        _add_referral("urgency", "keyword")

    props["doc_type"] = {"type": "keyword"}
    return {"mappings": {"properties": props}}


def index_name(facility_id: str, doc_type: str) -> str:
    """Return the ES index name for a facility x doctype combo."""
    return f"medical_{facility_id}_{doc_type}"


def all_index_configs(locale: LocaleConfig) -> list[tuple[str, str, dict]]:
    """Return (index_name, facility_id, mapping) for every valid combo."""
    results = []
    for fac in locale.facilities:
        for dt in fac["doc_types"]:
            name = index_name(fac["id"], dt)
            mapping = get_es_mapping_for_index(fac["id"], dt, locale)
            results.append((name, fac["id"], mapping))
    return results

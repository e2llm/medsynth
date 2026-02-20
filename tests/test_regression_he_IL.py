"""Regression test: refactored code with he_IL produces output identical to pre-refactor."""

import json
import os
import random
import tempfile
import pytest
from medsynth.generate import generate_documents

FIXTURE_DIR = os.path.join(os.path.dirname(__file__), "fixtures", "pre_refactor_seed42")


def _load_fixture():
    """Load all docs from the pre-refactor fixture."""
    data = {}
    for f in sorted(os.listdir(FIXTURE_DIR)):
        if not f.endswith(".ndjson"):
            continue
        idx_name = f.replace(".ndjson", "")
        with open(os.path.join(FIXTURE_DIR, f), encoding="utf-8") as fh:
            data[idx_name] = [json.loads(line) for line in fh]
    return data


def _generate_fresh():
    """Generate fresh output with the same parameters."""
    with tempfile.TemporaryDirectory() as tmpdir:
        counts = generate_documents(
            num_patients=10,
            seed=42,
            output_dir=tmpdir,
            model="gpt-4o",
            locale_code="he_IL",
            skip_freetext=True,
        )
        data = {}
        for f in sorted(os.listdir(tmpdir)):
            if not f.endswith(".ndjson"):
                continue
            idx_name = f.replace(".ndjson", "")
            with open(os.path.join(tmpdir, f), encoding="utf-8") as fh:
                data[idx_name] = [json.loads(line) for line in fh]
        return data, counts


@pytest.fixture(scope="module")
def regression_data():
    fixture = _load_fixture()
    fresh, counts = _generate_fresh()
    return fixture, fresh, counts


def test_same_indices_created(regression_data):
    fixture, fresh, _ = regression_data
    assert set(fixture.keys()) == set(fresh.keys())


def test_same_doc_counts(regression_data):
    fixture, fresh, _ = regression_data
    for idx_name in fixture:
        assert len(fixture[idx_name]) == len(fresh[idx_name]), (
            f"{idx_name}: {len(fixture[idx_name])} vs {len(fresh[idx_name])}"
        )


def test_same_field_names_per_index(regression_data):
    fixture, fresh, _ = regression_data
    for idx_name in fixture:
        for i, (old, new) in enumerate(zip(fixture[idx_name], fresh[idx_name])):
            assert set(old.keys()) == set(new.keys()), (
                f"{idx_name} doc {i}: {set(old.keys()) ^ set(new.keys())}"
            )


def test_same_field_types(regression_data):
    fixture, fresh, _ = regression_data
    for idx_name in fixture:
        for i, (old, new) in enumerate(zip(fixture[idx_name], fresh[idx_name])):
            for k in old:
                assert type(old[k]) == type(new[k]), (
                    f"{idx_name} doc {i} field {k}: {type(old[k]).__name__} vs {type(new[k]).__name__}"
                )


def test_zero_value_diffs(regression_data):
    """Byte-perfect value match (deterministic with skip-freetext)."""
    fixture, fresh, _ = regression_data
    diffs = []
    for idx_name in fixture:
        for i, (old, new) in enumerate(zip(fixture[idx_name], fresh[idx_name])):
            for k in old:
                if old[k] != new[k]:
                    diffs.append(f"{idx_name} doc {i} {k}: {old[k]!r} vs {new[k]!r}")
    assert diffs == [], f"Found {len(diffs)} diffs:\n" + "\n".join(diffs[:10])


def test_patient_ids_valid():
    """All Israeli IDs pass Luhn variant checksum."""
    fresh, _ = _generate_fresh()
    seen_ids = set()
    for idx_name, docs in fresh.items():
        for doc in docs:
            for k in ("patient_id", "מספר_זהות", "tz"):
                if k in doc:
                    raw = str(doc[k]).replace(".0", "")
                    if raw.isdigit():
                        seen_ids.add(raw)

    assert len(seen_ids) > 0
    for id_str in seen_ids:
        # Verify Luhn variant checksum
        digits = [int(c) for c in id_str.zfill(9)]
        total = 0
        for i, d in enumerate(digits):
            v = d * (1 + (i % 2))
            total += v // 10 + v % 10
        assert total % 10 == 0, f"Invalid Israeli ID checksum: {id_str}"


def test_age_formats():
    """Verify age format conventions per facility."""
    fresh, _ = _generate_fresh()
    for doc in fresh.get("medical_alon_discharge", []):
        assert isinstance(doc["patient_age"], int)
    for doc in fresh.get("medical_shaked_visit", []):
        assert isinstance(doc["age_group"], str)
        assert "-" in doc["age_group"]  # range string like "30-40"


def test_date_formats():
    """Verify date format conventions per facility."""
    fresh, _ = _generate_fresh()
    for doc in fresh.get("medical_alon_discharge", []):
        # YYYY-MM-DD
        assert len(doc["document_date"]) == 10
        assert doc["document_date"][4] == "-"
    for doc in fresh.get("medical_hadarim_discharge", []):
        # DD/MM/YYYY
        assert "/" in doc["תאריך"]

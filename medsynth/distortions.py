"""Distortion pipeline: OCR artifacts, garbage injection, contradictions."""

import random
import copy
from . import config
from .locales.base import LocaleConfig, OcrPattern


def apply_ocr_noise(
    text: str,
    rng: random.Random,
    ocr_patterns: list[OcrPattern],
    error_rate: float = None,
    space_drop_rate: float = None,
    space_insert_rate: float = None,
) -> str:
    """Apply OCR character confusion and artifacts to text.

    Supports single-char and multi-char patterns via longest-match-first scan.
    """
    if error_rate is None:
        error_rate = config.OCR_CHAR_ERROR_RATE
    if space_drop_rate is None:
        space_drop_rate = config.OCR_SPACE_DROP_RATE
    if space_insert_rate is None:
        space_insert_rate = config.OCR_SPACE_INSERT_RATE
    if not ocr_patterns and space_drop_rate == 0 and space_insert_rate == 0:
        return text

    # Index patterns by source string for O(1) lookup
    pattern_index: dict[str, list[OcrPattern]] = {}
    max_len = 1
    for p in ocr_patterns:
        pattern_index.setdefault(p.source, []).append(p)
        if len(p.source) > max_len:
            max_len = len(p.source)

    chars = text
    result = []
    i = 0
    while i < len(chars):
        c = chars[i]

        # Space noise
        if c == " " and rng.random() < space_drop_rate:
            i += 1
            continue

        if c != " " and rng.random() < space_insert_rate:
            result.append(" ")

        # Try OCR confusion (longest match first)
        if rng.random() < error_rate:
            matched = False
            for window in range(min(max_len, len(chars) - i), 0, -1):
                substring = chars[i:i + window]
                candidates = pattern_index.get(substring)
                if candidates:
                    # Weighted random selection
                    total_weight = sum(p.weight for p in candidates)
                    pick = rng.random() * total_weight
                    cumulative = 0.0
                    for p in candidates:
                        cumulative += p.weight
                        if pick <= cumulative:
                            result.append(p.target)
                            i += window
                            matched = True
                            break
                    if matched:
                        break
            if matched:
                continue

        result.append(c)
        i += 1

    return "".join(result)


def apply_digital_typos(text: str, rng: random.Random) -> str:
    """Apply minor typos to digitally-sourced text (doctor shorthand)."""
    chars = list(text)
    result = []
    for c in chars:
        if rng.random() < config.DIGITAL_TYPO_RATE and c not in " \n\t":
            if rng.random() < 0.5:
                continue
            result.append(c)
        result.append(c)
    return "".join(result)


def apply_ocr_to_field(value: str, rng: random.Random, locale: LocaleConfig) -> str:
    """Apply OCR noise to a medium-trust parsed field value.

    Uses a simple per-character replacement (1 rng call per char) to maintain
    deterministic RNG sequence compatibility with the pre-refactor code.
    """
    if not isinstance(value, str):
        return value
    # Build char→replacement map (first pattern wins for each source char)
    if not hasattr(apply_ocr_to_field, "_char_maps"):
        apply_ocr_to_field._char_maps = {}
    cache_key = locale.code
    if cache_key not in apply_ocr_to_field._char_maps:
        char_map = {}
        for p in locale.ocr_patterns:
            # Exclude digit→letter patterns (those only apply in full OCR noise)
            if len(p.source) == 1 and not p.source.isdigit() and p.source not in char_map:
                char_map[p.source] = p.target
        apply_ocr_to_field._char_maps[cache_key] = char_map
    char_map = apply_ocr_to_field._char_maps[cache_key]

    error_rate = config.OCR_FIELD_ERROR_RATE
    chars = list(value)
    result = []
    for c in chars:
        if rng.random() < error_rate:
            c = char_map.get(c, c)
        result.append(c)
    return "".join(result)


def _concept_field_names(locale: LocaleConfig, concept: str) -> set[str]:
    """Get all field names for a concept across all facilities."""
    names = set()
    for fnames in locale.field_names.values():
        field = fnames.get(concept)
        if field is not None:
            names.add(field)
    return names


def inject_garbage(doc: dict, rng: random.Random, locale: LocaleConfig) -> dict:
    """Inject garbage values into a document (~6% of records)."""
    if rng.random() > config.GARBAGE_RATE:
        return doc

    doc = copy.deepcopy(doc)
    garbage_type = rng.choice(["zero_age", "empty_field", "generic_location",
                                "wrong_type", "empty_text"])

    age_fields = _concept_field_names(locale, "age")
    address_fields = _concept_field_names(locale, "address")
    text_fields = _concept_field_names(locale, "free_text")

    if garbage_type == "zero_age":
        for key in doc:
            if key in age_fields or "age" in key.lower():
                doc[key] = 0
                break

    elif garbage_type == "empty_field":
        candidates = [k for k in doc if k not in ("doc_type",) and doc[k]]
        if candidates:
            doc[rng.choice(candidates)] = ""

    elif garbage_type == "generic_location":
        for key in doc:
            if key in address_fields or "address" in key.lower():
                doc[key] = locale.generic_location
                break

    elif garbage_type == "wrong_type":
        # Store a numeric field as a string or vice versa
        for key in doc:
            if isinstance(doc[key], int) and key not in ("doc_type",):
                doc[key] = str(doc[key])
                break
            elif isinstance(doc[key], str) and doc[key].isdigit():
                doc[key] = int(doc[key])
                break

    elif garbage_type == "empty_text":
        for key in doc:
            if key in text_fields or "text" in key.lower() or "notes" in key.lower():
                doc[key] = ""
                break

    return doc


def pick_contradiction(patient: dict, doc: dict, rng: random.Random, locale: LocaleConfig) -> dict | None:
    """Decide what contradiction to inject into free text."""
    if rng.random() > config.CONTRADICTION_RATE:
        return None

    templates = locale.contradiction_templates
    contradiction_type = rng.choice(["smoking", "age", "medication"])

    if contradiction_type == "smoking":
        structured_smoking = patient.get("smoking", False)
        text = templates["smoking_yes"] if not structured_smoking else templates["smoking_no"]
        return {
            "type": "smoking",
            "structured_value": structured_smoking,
            "text_should_say": text,
        }
    elif contradiction_type == "age":
        # Use the doc's computed age (per document date) instead of static patient age
        age_fields = _concept_field_names(locale, "age")
        real_age = None
        for k in doc:
            if k in age_fields:
                val = doc[k]
                if isinstance(val, int):
                    real_age = val
                break
        if real_age is None:
            return None
        fake_age = real_age + rng.choice(config.AGE_CONTRADICTION_OFFSETS)
        if fake_age < 0:
            fake_age = real_age + 10
        return {
            "type": "age",
            "structured_value": real_age,
            "text_should_say": templates["age"].format(age=fake_age),
        }
    elif contradiction_type == "medication":
        all_meds = set(locale.medications)
        patient_meds = set(patient.get("medications", []))
        extra_meds = list(all_meds - patient_meds)
        if extra_meds:
            med = rng.choice(extra_meds)
            return {
                "type": "medication",
                "structured_value": list(patient_meds),
                "text_should_say": templates["medication"].format(med=med),
            }

    return None


def apply_field_distortions(
    doc: dict,
    facility_id: str,
    doc_type: str,
    rng: random.Random,
    locale: LocaleConfig,
) -> dict:
    """Apply field-level distortions based on source type (OCR vs digital)."""
    facility = locale.facility_by_id[facility_id]
    source = facility["source"].get(doc_type, "digital")
    doc = copy.deepcopy(doc)

    if source == "ocr":
        for key, value in doc.items():
            if key in ("doc_type", "lab_results"):
                continue
            if isinstance(value, str) and len(value) > 2:
                doc[key] = apply_ocr_to_field(value, rng, locale)
            elif isinstance(value, list):
                doc[key] = [
                    apply_ocr_to_field(v, rng, locale) if isinstance(v, str) else v
                    for v in value
                ]

    # ICD10 digit swap (occasional, both sources)
    for key, value in doc.items():
        if isinstance(value, list):
            new_list = []
            for v in value:
                if isinstance(v, str) and len(v) >= 3 and v[0].isalpha() and rng.random() < config.ICD10_DIGIT_SWAP_RATE:
                    chars = list(v)
                    digit_positions = [i for i, c in enumerate(chars) if c.isdigit()]
                    if len(digit_positions) >= 2:
                        a, b = rng.sample(digit_positions, 2)
                        chars[a], chars[b] = chars[b], chars[a]
                    v = "".join(chars)
                new_list.append(v)
            doc[key] = new_list

    return doc

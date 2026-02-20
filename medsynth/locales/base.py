"""Locale data model: OcrPattern and LocaleConfig."""

from dataclasses import dataclass, field
from typing import Callable


@dataclass
class OcrPattern:
    """A single OCR confusion pattern (single-char or multi-char).

    source: clean text (e.g. "rn", "ר", "ب")
    target: OCR output (e.g. "m", "ד", "ت")
    weight: relative frequency (1.0 = most common)
    """
    source: str
    target: str
    weight: float = 1.0


@dataclass
class LocaleConfig:
    """All locale-specific content for synthetic medical data generation."""

    code: str                       # "he_IL", "ar_SA", "es_MX"
    language: str                   # "Hebrew", "Arabic", "Spanish"
    country: str                    # "Israel", "Saudi Arabia", "Mexico"

    # Demographics
    cities: list[str] = field(default_factory=list)
    streets: list[str] = field(default_factory=list)
    occupations: list[str] = field(default_factory=list)
    address_format: str = "{street} {num}, {city}"

    # Names — locale-defined structure
    generate_name: Callable = field(default=None)
    emergency_contact_name: Callable = field(default=None)

    # Medical
    conditions: list[str] = field(default_factory=list)
    medications: list[str] = field(default_factory=list)
    departments: list[str] = field(default_factory=list)
    lab_tests: list[dict] = field(default_factory=list)
    icd10_codes: dict[str, str] = field(default_factory=dict)

    # Facilities (the core variance engine)
    facilities: list[dict] = field(default_factory=list)
    facility_by_id: dict[str, dict] = field(default_factory=dict)
    field_names: dict[str, dict] = field(default_factory=dict)

    # OCR — unified pattern model
    ocr_patterns: list[OcrPattern] = field(default_factory=list)

    # National ID
    generate_id: Callable = field(default=None)

    # Free text generation
    system_prompt: str = ""
    facility_styles: dict[str, str] = field(default_factory=dict)
    doc_type_contexts: dict[str, str] = field(default_factory=dict)
    medical_abbreviations: str = ""
    format_patient_context: Callable = field(default=None)
    contradiction_templates: dict = field(default_factory=dict)
    fallback_strings: dict = field(default_factory=dict)

    # Prompt assembly
    format_clinical_prompt: Callable = field(default=None)

    # Misc locale-specific
    generic_location: str = ""
    gender_labels: dict[str, str] = field(default_factory=dict)
    urgency_values: list[str] = field(default_factory=list)

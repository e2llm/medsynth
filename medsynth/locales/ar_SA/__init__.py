"""Arabic/Saudi Arabia locale — assembles all ar_SA data into a LocaleConfig."""

from ..base import LocaleConfig
from .demographics import (
    CITIES, STREETS, OCCUPATIONS, generate_name, emergency_contact_name,
)
from .medical import (
    CONDITIONS, MEDICATIONS, DEPARTMENTS, LAB_TESTS, ICD10_CODES,
)
from .facilities import FACILITIES, FACILITY_BY_ID, FIELD_NAMES
from .freetext import (
    SYSTEM_PROMPT, FACILITY_STYLES, DOC_TYPE_CONTEXTS,
    MEDICAL_ABBREVIATIONS, format_patient_context,
    format_clinical_prompt,
    CONTRADICTION_TEMPLATES, FALLBACK_STRINGS,
)
from .national_id import generate_id

from ..scripts.arabic import ARABIC_OCR_PATTERNS

LOCALE = LocaleConfig(
    code="ar_SA",
    language="Arabic",
    country="Saudi Arabia",

    # Demographics
    cities=CITIES,
    streets=STREETS,
    occupations=OCCUPATIONS,
    address_format="{street} {num}, {city}",
    generate_name=generate_name,
    emergency_contact_name=emergency_contact_name,

    # Medical
    conditions=CONDITIONS,
    medications=MEDICATIONS,
    departments=DEPARTMENTS,
    lab_tests=LAB_TESTS,
    icd10_codes=ICD10_CODES,

    # Facilities
    facilities=FACILITIES,
    facility_by_id=FACILITY_BY_ID,
    field_names=FIELD_NAMES,

    # OCR
    ocr_patterns=ARABIC_OCR_PATTERNS,

    # National ID
    generate_id=generate_id,

    # Free text
    system_prompt=SYSTEM_PROMPT,
    facility_styles=FACILITY_STYLES,
    doc_type_contexts=DOC_TYPE_CONTEXTS,
    medical_abbreviations=MEDICAL_ABBREVIATIONS,
    format_patient_context=format_patient_context,
    format_clinical_prompt=format_clinical_prompt,
    contradiction_templates=CONTRADICTION_TEMPLATES,
    fallback_strings=FALLBACK_STRINGS,

    # Misc
    generic_location="المملكة العربية السعودية",
    gender_labels={"male": "ذكر", "female": "أنثى"},
    urgency_values=["عاجل", "عادي", "غير عاجل"],
)

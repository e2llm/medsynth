"""Locale-agnostic defaults for synthetic medical data generation."""

from datetime import date

# ---------------------------------------------------------------------------
# Universal medical constants
# ---------------------------------------------------------------------------
BLOOD_TYPES = ["A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"]

# ---------------------------------------------------------------------------
# Patient generation
# ---------------------------------------------------------------------------
DOB_START = date(1940, 1, 1)         # earliest possible date of birth
DOB_RANGE_DAYS = 28000               # ~76 years of DOB spread
MAX_CONDITIONS_PER_PATIENT = 5
MAX_MEDICATIONS_PER_PATIENT = 6
MAX_HOUSE_NUMBER = 120
SMOKING_PREVALENCE = 0.25            # probability a patient is a smoker

# ---------------------------------------------------------------------------
# Document generation
# ---------------------------------------------------------------------------
DOC_DATE_START = date(2023, 1, 1)
DOC_DATE_END = date(2025, 12, 31)
MIN_FACILITIES_PER_PATIENT = 2
MAX_FACILITIES_PER_PATIENT = 4
MIN_DOCS_PER_VISIT = 1
MAX_DOCS_PER_VISIT = 2

# ---------------------------------------------------------------------------
# Lab results
# ---------------------------------------------------------------------------
MIN_LAB_TESTS_PER_DOC = 3
MAX_LAB_TESTS_PER_DOC = 8
LAB_ABNORMAL_RATE = 0.3              # probability a lab result is abnormal
AGE_RANGE_BUCKET = 10                # bucket size for age range strings (e.g. "30-40")

# ---------------------------------------------------------------------------
# Distortion rates
# ---------------------------------------------------------------------------
GARBAGE_RATE = 0.06                  # ~6% of records get garbage injection
CONTRADICTION_RATE = 0.18            # ~18% get structured-vs-text contradiction
OCR_CHAR_ERROR_RATE = 0.03           # per-character in OCR text
OCR_FIELD_ERROR_RATE = 0.015         # per-character in OCR parsed fields (half of text rate)
OCR_SPACE_DROP_RATE = 0.02           # probability of dropping a space in OCR text
OCR_SPACE_INSERT_RATE = 0.008        # probability of inserting a space in OCR text
DIGITAL_TYPO_RATE = 0.005            # per-character in digital text
ICD10_DIGIT_SWAP_RATE = 0.05         # probability of swapping digits in an ICD code
AGE_CONTRADICTION_OFFSETS = [-10, -5, 5, 10, 15]  # fake age deltas for contradictions

# ---------------------------------------------------------------------------
# LLM — default: Ollama + Llama 4 Maverick (local, no API key needed)
# ---------------------------------------------------------------------------
DEFAULT_API_BASE = "http://localhost:11434/v1"   # Ollama
DEFAULT_MODEL = "llama4:maverick"
LLM_TEMPERATURE = 0.8
LLM_MAX_TOKENS = 800

# --- Alternative providers (uncomment one block) -------------------------
#
# # OpenAI (GPT-4o) — set LLM_API_KEY or OPENAI_API_KEY env var
# DEFAULT_API_BASE = "https://api.openai.com/v1"
# DEFAULT_MODEL = "gpt-4o"
#
# # Anthropic Claude Haiku 4.5 — needs OpenAI-compatible proxy (e.g. LiteLLM)
# DEFAULT_API_BASE = "http://localhost:4000/v1"   # LiteLLM proxy
# DEFAULT_MODEL = "claude-haiku-4-5"
#
# # Moonshot Kimi K2 — set MOONSHOT_API_KEY env var
# DEFAULT_API_BASE = "https://api.moonshot.ai/v1"
# DEFAULT_MODEL = "kimi-k2-0711-preview"

# ---------------------------------------------------------------------------
# Generation defaults
# ---------------------------------------------------------------------------
DEFAULT_NUM_PATIENTS = 500
DEFAULT_SEED = 42
DEFAULT_OUTPUT_DIR = "output"
DEFAULT_LOCALE = "he_IL"

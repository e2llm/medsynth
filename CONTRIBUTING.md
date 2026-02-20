# Contributing to MedSynth

PRs welcome. Here's how to get started.

## Setup

```bash
git clone https://github.com/e2llm/medsynth.git
cd medsynth
pip install -e ".[dev]"
pytest tests/ -v
```

## Adding a New Locale

This is the most common contribution. Each locale lives in `medsynth/locales/<code>/` (e.g. `he_IL`, `ar_SA`, `es_MX`).

### Required files

```
medsynth/locales/<code>/
├── __init__.py        # Builds and returns a LocaleConfig
├── demographics.py    # Names, cities, streets, occupations
├── medical.py         # Conditions, medications, lab tests, departments
├── national_id.py     # Country-specific ID generation
└── facilities.py      # Hospitals/clinics with schema definitions
```

### Steps

1. Copy an existing locale as a starting point (pick one with a similar script — e.g. `ar_SA` for Arabic, `es_MX` for Latin)
2. Implement all files following the same structure
3. Register the locale in `medsynth/locales/__init__.py`
4. Add OCR patterns appropriate for the script (see `medsynth/locales/base.py:OcrPattern`)
5. Add sample data: `medsynth --locale <code> --num-patients 50 --seed 42 --skip-freetext --output-dir medsynth/sample_data/<code> --force`
6. Run tests: `pytest tests/ -v` (parametric tests auto-discover new locales)

### Key design points

- **Schema variance**: Different facilities should use different field names, date formats, and ID storage types. This is the core value of MedSynth.
- **OCR patterns**: Should reflect real scanning artifacts for the locale's script. See existing patterns for Hebrew (shape confusion), Arabic (dot groups), and Latin (diacritic loss).
- **National IDs**: Must follow the real format for the country (checksum, encoding rules, etc.).
- **Names**: Use culturally appropriate name lists. For locales with patronymics or multiple surnames, include those in the name dict.

## Other Contributions

- **Bug fixes**: Include a test if possible
- **New doc types**: Add to facility `doc_types` lists and handle in `medsynth/schemas.py:build_structured_fields()`
- **Distortion patterns**: See `medsynth/distortions.py`

## Tests

```bash
pytest tests/ -v
```

Most tests are parametric across all locales — adding a locale automatically gets test coverage for name generation, ID format, locale config completeness, etc.

## Style

- No external dependencies beyond `openai` and `python-dotenv`
- Keep locale data self-contained (no shared data files between locales)
- Deterministic output for the same seed (when using `--skip-freetext`)

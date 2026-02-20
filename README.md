# MedSynth

Multi-lingual synthetic healthcare data generator. Produces realistic medical records with intentional OCR artifacts and schema variance — simulating real-world messy healthcare data.

## The Problem

Healthcare AI development is bottlenecked by data access.

Real patient records are legally restricted (HIPAA, GDPR, Uruguay's Ley 18.331), expensive to anonymize, and nearly impossible to share across borders. Researchers spend months navigating data access before writing a single line of AI code.

Meanwhile, most synthetic data generators produce clean, English-only records that look nothing like actual hospital data — which is scanned paper, multi-lingual, inconsistently formatted, and full of OCR errors.

MedSynth generates data that looks like the real thing — including the mess.

## What Makes This Different

| Feature | MedSynth | Typical Generators |
|---------|----------|-------------------|
| **Languages** | 6 locales (Hebrew, Arabic, Spanish) | English only |
| **OCR artifacts** | Realistic scan errors per script | Clean text |
| **Schema variance** | Different formats per facility | Single schema |
| **ID systems** | Country-specific (Teudat Zehut, CURP, DNI) | Generic |
| **Privacy** | Zero real patient data | Often derived from real records |

### OCR Realism

Real medical records are scanned paper. MedSynth simulates actual scanning artifacts:

- **Arabic**: Dot-group confusions (ب↔ت↔ث), tashkeel stripping
- **Hebrew**: Shape-based confusions (ר↔ד, ח↔כ)
- **Latin**: rn→m merges, diacritic loss (ñ→n), 0↔O swaps

### Schema Variance

Different hospitals format records differently. MedSynth produces variant schemas across facilities so AI systems learn to handle real-world inconsistency — not just clean demos.

## Installation

```bash
pip install -e .
```

### Quick Start

```bash
git clone https://github.com/e2llm/medsynth.git
cd medsynth && pip install -e .

# Structured data only (no LLM needed)
medsynth --locale he_IL --num-patients 10 --skip-freetext -v

# With free text via Ollama (default — no API key needed)
ollama pull llama4:maverick
medsynth --locale he_IL --num-patients 10 -v
```

Free text generation uses any OpenAI-compatible API. Default: Ollama + Llama 4 Maverick (local). No API key needed for basic generation or local Ollama.

## Output Format

MedSynth outputs NDJSON files — one per facility × document type:

```
output/
├── medical_alon_discharge.ndjson
├── medical_alon_lab.ndjson
├── medical_alon_referral.ndjson
├── medical_hadarim_discharge.ndjson
├── medical_hadarim_visit.ndjson
├── ...
```

### Example: The Mess

**Alon hospital — digital, English field names:**
```json
{"patient_id": "165667015", "patient_name": "משה אזולאי", "patient_age": 77, "gender": "male", "document_date": "2023-07-01", "facility_name": "בית חולים האלון", "conditions": ["השמנת יתר", "דיכאון", "COPD"], "smoking_status": true, "department": "אורולוגיה", "primary_diagnosis": "השמנת יתר", "doc_type": "discharge"}
```

**Hadarim hospital — OCR source, Hebrew field names, different ID type:**
```json
{"מספר_זהות": 161559406, "שם_מטופל": "יעל גולן", "גיל": 31, "מין": "female", "תאריך": "29/04/2024", "מוסד_רפואי": "מרכז רפואי הדרים", "מחלות_רקע": ["סוכרת סוג 2", "אי ספיקת כליות כרונית"], "מחלקה": "פנימית א", "אבחנה_ראשית": "סוכרת סוג 2", "doc_type": "discharge"}
```
Different field names (`patient_id` → `מספר_זהות`), different date format (`2023-07-01` → `29/04/2024`), ID as integer instead of string.

**Saudi Arabia — Arabic fields, age as range string:**
```json
{"رقم_الهوية": 1496965326, "الاسم": "عبدالرحمن بن راشد الأحمدي", "العمر": "50-60", "الجنس": "male", "التاريخ": "2023-06", "المركز": "مركز الرعاية الصحية الأولية", "الأمراض": ["فرط شحميات الدم"], "التشخيص": "فرط شحميات الدم", "doc_type": "discharge"}
```
Age stored as range string (`"50-60"` not `57`), date truncated to month (`"2023-06"`).

**Mexico — CURP national ID, Spanish field names:**
```json
{"patient_id": "AULJ460528MDFGPN03", "patient_name": "Juana Aguilar Figueroa", "patient_age": 77, "gender": "female", "document_date": "2024-01-10", "facility_name": "Hospital Nacional del Norte", "conditions": ["insuficiencia renal crónica", "obesidad", "gota"], "department": "oncología", "doc_type": "discharge"}
```
18-character CURP encodes name, DOB, gender, and state — completely different from Israeli 9-digit Luhn IDs.

## CLI Usage

```bash
# Default: Ollama + Llama 4 Maverick (local, no API key)
medsynth --locale he_IL --num-patients 500 --seed 42 -v

# Structured data only — no LLM needed
medsynth --locale es_MX --num-patients 50 --seed 42 --skip-freetext -v

# OpenAI GPT-4o
export LLM_API_KEY="sk-..."
medsynth --api-base https://api.openai.com/v1 --model gpt-4o -v

# Moonshot Kimi K2
export LLM_API_KEY="your-moonshot-key"
medsynth --api-base https://api.moonshot.ai/v1 --model kimi-k2-0711-preview -v

# Anthropic Claude Haiku (via LiteLLM or any OpenAI-compatible proxy)
medsynth --api-base http://localhost:4000/v1 --model claude-haiku-4-5 -v
```

### Options

| Flag | Default | Description |
|------|---------|-------------|
| `--locale` | `he_IL` | Locale code |
| `--num-patients` | `500` | Number of patients to generate |
| `--seed` | `42` | Random seed for reproducibility |
| `--output-dir` | `output` | Output directory for NDJSON files |
| `--model` | `llama4:maverick` | LLM model name |
| `--api-base` | `http://localhost:11434/v1` | API base URL (any OpenAI-compatible endpoint) |
| `--api-key` | — | API key (or set `LLM_API_KEY` / `OPENAI_API_KEY` env var) |
| `--skip-freetext` | off | Skip LLM calls for free text |
| `-v` / `--verbose` | off | Verbose output |

## Python API

```python
from medsynth import generate_documents, load_locale

# Generate documents (default: Ollama + Llama 4 Maverick)
counts = generate_documents(
    num_patients=50,
    seed=42,
    output_dir="output",
    locale_code="es_ES",
    skip_freetext=True,  # set False to generate free text via LLM
    verbose=True,
)

# Use a different provider
counts = generate_documents(
    num_patients=50,
    seed=42,
    output_dir="output",
    model="gpt-4o",
    api_base="https://api.openai.com/v1",
    api_key="sk-...",
    locale_code="es_ES",
)

# Load a locale directly
locale = load_locale("ar_SA")
print(locale.code, len(locale.facilities))
```

## Supported Locales

| Code | Region | Script | Facilities |
|------|--------|--------|------------|
| `he_IL` | Israel | Hebrew | Alon, Hadarim, Shaked, Ofek |
| `ar_SA` | Saudi Arabia | Arabic | Riyadh Medical City, Royal Military, PHC, Al Hayat Labs |
| `ar_EG` | Egypt | Arabic | Nile Central, Delta University, Tahrir, Al Mokhtabar |
| `es_ES` | Spain | Latin | Reina Ficticia, San Rafael, Atencion Primaria, Iberia Labs |
| `es_MX` | Mexico | Latin | Nacional del Norte, Federal del Centro, Centro de Salud, Azteca Labs |
| `es_AR` | Argentina | Latin | Hospital del Plata, San Martin, CAPS, Austral Labs |

## Sample Data

Pre-generated sample data (50 patients, seed 42) ships with the package:

```python
from importlib.resources import files

sample_dir = files("medsynth") / "sample_data" / "he_IL"
```

## Tests

```bash
pip install -e ".[dev]"
pytest tests/ -v
```

## Use Cases

- **Healthcare NLP testing** — validate extraction pipelines against known-correct synthetic records
- **AI agent development** — train/test agents that query unstructured medical text
- **OCR pipeline validation** — test document understanding against realistic scan artifacts
- **Cross-border healthcare IT** — test systems handling multiple languages/formats
- **Compliance testing** — validate anonymization systems with synthetic ground truth
- **Education** — teach healthcare informatics without privacy concerns

## Who We Are

[e2llm](https://github.com/e2llm) — healthcare data intelligence.

We build systems that make unstructured medical data queryable: document understanding (OCR → structured), semantic search (natural language → patient cohorts), and multi-lingual medical NLP. Working with healthcare organizations across MENA and Latin America.

## Contact

- **Email**: info@e2llm.com
- **For**: Custom locale development, integration with production pipelines, air-gapped deployment consulting, enterprise support

## Contributing

PRs welcome. See [issues](https://github.com/e2llm/medsynth/issues) for open tasks.

## Disclaimer

**MedSynth is an independent open-source project by [e2llm](https://github.com/e2llm). It is not affiliated with, endorsed by, or related to any company or entity operating under the same or a similar name.** Any resemblance in naming is purely coincidental.

This tool generates entirely synthetic data for software testing, demos, and research. No real patient information is used or produced. Facility names are fictional — inspired by real institutions for realism, but all generated records are entirely synthetic.

This is not medical software and must not be used for clinical decisions.

Free text generation calls an LLM API. The default (Ollama) runs locally at no cost. When using cloud providers (OpenAI, Moonshot, Anthropic), review their usage policies and be aware of associated costs.

## License

MIT

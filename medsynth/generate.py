#!/usr/bin/env python3
"""Main orchestrator: generate synthetic medical records with realistic variance."""

import argparse
import json
import os
import random
import sys
from datetime import timedelta
from urllib.parse import urlparse

from . import config
from .locales import load_locale
from .patients import generate_patients
from .schemas import build_structured_fields, index_name
from .distortions import (
    apply_field_distortions,
    apply_ocr_noise,
    apply_digital_typos,
    inject_garbage,
    pick_contradiction,
)
from .freetext import generate_clinical_text


def _random_doc_date(rng: random.Random) -> str:
    """Generate a random document date within the configured range."""
    delta = (config.DOC_DATE_END - config.DOC_DATE_START).days
    d = config.DOC_DATE_START + timedelta(days=rng.randint(0, delta))
    return d.isoformat()


def _is_local_endpoint(url: str) -> bool:
    """Check if a URL points to a local endpoint."""
    hostname = urlparse(url).hostname or ""
    return hostname in ("localhost", "127.0.0.1", "::1", "0.0.0.0") or hostname.endswith(".local")


def generate_documents(
    num_patients: int,
    seed: int,
    output_dir: str,
    model: str | None = None,
    api_base: str | None = None,
    api_key: str | None = None,
    locale_code: str | None = None,
    skip_freetext: bool = False,
    verbose: bool = False,
    force: bool = False,
    # Backwards compat — ignored if model is set
    openai_model: str | None = None,
) -> dict[str, int]:
    """Generate all documents and write NDJSON files."""
    model = model or openai_model
    locale = load_locale(locale_code or config.DEFAULT_LOCALE)
    rng = random.Random(seed + 1)  # offset from patient seed to avoid RNG correlation
    os.makedirs(output_dir, exist_ok=True)

    if not force and os.path.isdir(output_dir):
        existing = [f for f in os.listdir(output_dir) if f.endswith(".ndjson")]
        if existing:
            raise FileExistsError(
                f"{output_dir}/ contains {len(existing)} .ndjson files. "
                f"Use --force to overwrite."
            )

    # Step 1: Generate patient pool
    if verbose:
        print(f"Generating {num_patients} patients (seed={seed}, locale={locale.code})...")
    patients = generate_patients(num_patients, seed, locale)

    # Step 2: Assign facilities and generate documents
    index_docs: dict[str, list[dict]] = {}
    total_docs = 0
    freetext_queue: list[dict] = []

    for p_idx, patient in enumerate(patients):
        num_facilities = rng.randint(
            config.MIN_FACILITIES_PER_PATIENT,
            config.MAX_FACILITIES_PER_PATIENT,
        )
        facilities = rng.sample(locale.facilities, min(num_facilities, len(locale.facilities)))

        for facility in facilities:
            num_docs = rng.randint(config.MIN_DOCS_PER_VISIT, config.MAX_DOCS_PER_VISIT)
            doc_types = rng.sample(facility["doc_types"], min(num_docs, len(facility["doc_types"])))

            for doc_type in doc_types:
                doc_date = _random_doc_date(rng)
                idx_name = index_name(facility["id"], doc_type)

                doc = build_structured_fields(
                    patient, facility["id"], doc_type, doc_date, rng, locale
                )

                contradiction = pick_contradiction(patient, doc, rng, locale)
                doc = apply_field_distortions(doc, facility["id"], doc_type, rng, locale)
                doc = inject_garbage(doc, rng, locale)

                if idx_name not in index_docs:
                    index_docs[idx_name] = []

                doc_idx = len(index_docs[idx_name])
                index_docs[idx_name].append(doc)
                total_docs += 1

                freetext_queue.append({
                    "index": idx_name,
                    "doc_idx": doc_idx,
                    "patient": patient,
                    "facility_id": facility["id"],
                    "doc_type": doc_type,
                    "contradiction": contradiction,
                    "source": facility["source"].get(doc_type, "digital"),
                })

        if verbose and (p_idx + 1) % 50 == 0:
            print(f"  Processed {p_idx + 1}/{num_patients} patients ({total_docs} docs so far)")

    if verbose:
        print(f"Generated {total_docs} structured documents across {len(index_docs)} indices")

    # Step 3: Generate free text
    if not skip_freetext:
        if verbose:
            print(f"Generating free text for {len(freetext_queue)} documents...")

        for i, item in enumerate(freetext_queue):
            doc = index_docs[item["index"]][item["doc_idx"]]

            # Get free text field name from locale
            fnames = locale.field_names[item["facility_id"]]
            text_field = fnames.get("free_text", "clinical_notes")

            try:
                text = generate_clinical_text(
                    patient=item["patient"],
                    facility_id=item["facility_id"],
                    doc_type=item["doc_type"],
                    locale=locale,
                    contradiction=item["contradiction"],
                    model=model,
                    api_base=api_base,
                    api_key=api_key,
                )

                if item["source"] == "ocr":
                    text = apply_ocr_noise(text, rng, locale.ocr_patterns)
                else:
                    text = apply_digital_typos(text, rng)

                doc[text_field] = text
            except Exception as e:
                if verbose:
                    print(f"  Warning: free text generation failed for doc {i}: {e}")
                doc[text_field] = ""

            if verbose and (i + 1) % 100 == 0:
                print(f"  Generated text for {i + 1}/{len(freetext_queue)} documents")
    else:
        if verbose:
            print("Skipping free text generation (--skip-freetext)")
        for item in freetext_queue:
            doc = index_docs[item["index"]][item["doc_idx"]]
            fnames = locale.field_names[item["facility_id"]]
            text_field = fnames.get("free_text", "clinical_notes")
            doc[text_field] = "[free text generation skipped]"

    # Step 4: Write NDJSON files
    if verbose:
        print(f"Writing NDJSON files to {output_dir}/")

    counts = {}
    for idx_name, docs in index_docs.items():
        filepath = os.path.join(output_dir, f"{idx_name}.ndjson")
        with open(filepath, "w", encoding="utf-8") as f:
            for doc in docs:
                f.write(json.dumps(doc, ensure_ascii=False) + "\n")
        counts[idx_name] = len(docs)
        if verbose:
            print(f"  {idx_name}: {len(docs)} documents")

    return counts


def main():
    parser = argparse.ArgumentParser(
        description="Generate synthetic medical records with realistic schema variance"
    )
    parser.add_argument("--num-patients", type=int, default=config.DEFAULT_NUM_PATIENTS)
    parser.add_argument("--seed", type=int, default=config.DEFAULT_SEED)
    parser.add_argument("--output-dir", default=config.DEFAULT_OUTPUT_DIR)
    parser.add_argument("--model", default=config.DEFAULT_MODEL,
                        help=f"LLM model name (default: {config.DEFAULT_MODEL})")
    parser.add_argument("--api-base", default=None,
                        help=f"API base URL (default: {config.DEFAULT_API_BASE})")
    parser.add_argument("--api-key", default=None,
                        help="API key (or set LLM_API_KEY / OPENAI_API_KEY env var)")
    parser.add_argument("--locale", default=config.DEFAULT_LOCALE,
                        help="Locale code (default: he_IL)")
    parser.add_argument("--skip-freetext", action="store_true",
                        help="Skip LLM calls for free text generation")
    parser.add_argument("--force", action="store_true",
                        help="Overwrite existing output files")
    parser.add_argument("--verbose", "-v", action="store_true")
    args = parser.parse_args()

    # Load .env if present
    try:
        from dotenv import load_dotenv
        load_dotenv()
    except ImportError:
        pass

    # Resolve API base — CLI > env > config default
    api_base = args.api_base or os.environ.get("LLM_API_BASE", config.DEFAULT_API_BASE)

    # Only require an API key for remote providers (not Ollama)
    if not args.skip_freetext and not _is_local_endpoint(api_base):
        key = (
            args.api_key
            or os.environ.get("LLM_API_KEY")
            or os.environ.get("OPENAI_API_KEY")
            or os.environ.get("MOONSHOT_API_KEY")
        )
        if not key:
            print(
                "Error: API key not set for remote provider. "
                "Use --api-key, set LLM_API_KEY env var, or use --skip-freetext.",
                file=sys.stderr,
            )
            sys.exit(1)

    counts = generate_documents(
        num_patients=args.num_patients,
        seed=args.seed,
        output_dir=args.output_dir,
        model=args.model,
        api_base=api_base,
        api_key=args.api_key,
        locale_code=args.locale,
        skip_freetext=args.skip_freetext,
        verbose=args.verbose,
        force=args.force,
    )

    print(f"\nDone. {sum(counts.values())} documents across {len(counts)} indices.")
    for name, count in sorted(counts.items()):
        print(f"  {name}: {count}")


if __name__ == "__main__":
    main()

"""LLM-powered clinical free text generation.

Default: Ollama + Llama 4 Maverick (local, no API key).
Any OpenAI-compatible endpoint works — set --api-base and --model.
"""

import os
import time
from openai import OpenAI, APIConnectionError, APITimeoutError, RateLimitError
from . import config
from .locales.base import LocaleConfig

_RETRYABLE = (APIConnectionError, APITimeoutError, RateLimitError)
_MAX_RETRIES = 3

_client = None


def _get_client(api_base: str | None = None, api_key: str | None = None) -> OpenAI:
    global _client
    if _client is None:
        base = api_base or os.environ.get("LLM_API_BASE", config.DEFAULT_API_BASE)
        key = (
            api_key
            or os.environ.get("LLM_API_KEY")
            or os.environ.get("OPENAI_API_KEY")
            or os.environ.get("MOONSHOT_API_KEY")
            or "ollama"  # Ollama ignores the key but the client requires one
        )
        _client = OpenAI(base_url=base, api_key=key)
    return _client


def reset_client():
    """Reset cached client (useful when switching providers in tests)."""
    global _client
    _client = None


def generate_clinical_text(
    patient: dict,
    facility_id: str,
    doc_type: str,
    locale: LocaleConfig,
    contradiction: dict | None = None,
    model: str | None = None,
    api_base: str | None = None,
    api_key: str | None = None,
) -> str:
    """Generate clinical narrative via any OpenAI-compatible API.

    Retries transient errors up to 3 times.
    """
    model = model or os.environ.get("LLM_MODEL", config.DEFAULT_MODEL)
    client = _get_client(api_base, api_key)

    prompt = locale.format_clinical_prompt(
        patient=patient,
        facility_id=facility_id,
        doc_type=doc_type,
        contradiction=contradiction,
    )

    for attempt in range(_MAX_RETRIES):
        try:
            response = client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": locale.system_prompt},
                    {"role": "user", "content": prompt},
                ],
                temperature=config.LLM_TEMPERATURE,
                max_tokens=config.LLM_MAX_TOKENS,
            )
            return response.choices[0].message.content.strip()
        except _RETRYABLE:
            if attempt == _MAX_RETRIES - 1:
                raise
            time.sleep(2 ** attempt)


def generate_clinical_text_batch(
    items: list[dict],
    locale: LocaleConfig,
    model: str | None = None,
    api_base: str | None = None,
    api_key: str | None = None,
) -> list[str]:
    """Generate multiple clinical texts sequentially."""
    results = []
    for item in items:
        text = generate_clinical_text(
            patient=item["patient"],
            facility_id=item["facility_id"],
            doc_type=item["doc_type"],
            locale=locale,
            contradiction=item.get("contradiction"),
            model=model,
            api_base=api_base,
            api_key=api_key,
        )
        results.append(text)
    return results

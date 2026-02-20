"""Locale registry and loader."""

import importlib
from .base import LocaleConfig, OcrPattern

REGISTRY = {
    "he_IL": "medsynth.locales.he_IL",
    "ar_SA": "medsynth.locales.ar_SA",
    "es_ES": "medsynth.locales.es_ES",
    "ar_EG": "medsynth.locales.ar_EG",
    "es_MX": "medsynth.locales.es_MX",
    "es_AR": "medsynth.locales.es_AR",
}


def load_locale(code: str) -> LocaleConfig:
    """Load a locale by code. Raises ValueError for unknown locales."""
    if code not in REGISTRY:
        available = ", ".join(sorted(REGISTRY.keys()))
        raise ValueError(f"Unknown locale '{code}'. Available: {available}")
    module = importlib.import_module(REGISTRY[code])
    return module.LOCALE


__all__ = ["LocaleConfig", "OcrPattern", "load_locale", "REGISTRY"]

"""MedSynth — synthetic medical record generator with realistic schema variance across locales."""

from .locales import load_locale, REGISTRY
from .locales.base import LocaleConfig, OcrPattern

__version__ = "0.1.0"


def generate_documents(*args, **kwargs):
    """Generate all documents and write NDJSON files. See medsynth.generate for full signature."""
    from .generate import generate_documents as _generate
    return _generate(*args, **kwargs)

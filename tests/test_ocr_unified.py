"""Tests for the unified OCR noise engine."""

import random
import pytest
from medsynth.distortions import apply_ocr_noise
from medsynth.locales import load_locale
from medsynth.locales.base import OcrPattern
from medsynth.locales.scripts.hebrew import HEBREW_OCR_PATTERNS
from medsynth.locales.scripts.latin import LATIN_OCR_PATTERNS


def test_hebrew_single_char():
    """Hebrew OCR should produce character confusions."""
    rng = random.Random(42)
    text = "רפואי הרופא בדק" * 10  # repeat for statistical chance
    result = apply_ocr_noise(text, rng, HEBREW_OCR_PATTERNS, error_rate=0.5)
    assert result != text
    # At high error rate, at least some confusions should fire
    assert any(c in result for c in "דחכזנצס")  # confusion targets


def test_latin_multi_char():
    """Latin OCR should produce multi-char merges like rn→m."""
    rng = random.Random(42)
    # Use high error rate and repeat text to ensure statistical coverage
    text = "modern internal clinical" * 20
    result = apply_ocr_noise(text, rng, LATIN_OCR_PATTERNS, error_rate=0.8)
    assert result != text


def test_empty_patterns():
    """Empty pattern list should pass text through unchanged."""
    rng = random.Random(42)
    text = "hello world"
    result = apply_ocr_noise(text, rng, [], error_rate=0.5)
    assert result == text


def test_deterministic():
    """Same seed should produce same output."""
    patterns = HEBREW_OCR_PATTERNS
    text = "בדיקת דם מלאה לבדיקת סוכר"
    result1 = apply_ocr_noise(text, random.Random(123), patterns, error_rate=0.1)
    result2 = apply_ocr_noise(text, random.Random(123), patterns, error_rate=0.1)
    assert result1 == result2


def test_space_noise():
    """Space drop and insert should fire at expected rates."""
    rng = random.Random(42)
    text = "word " * 500  # lots of spaces
    result = apply_ocr_noise(
        text, rng, [],
        error_rate=0.0,
        space_drop_rate=0.5,
        space_insert_rate=0.0,
    )
    original_spaces = text.count(" ")
    result_spaces = result.count(" ")
    # At 50% drop rate, roughly half the spaces should be gone
    assert result_spaces < original_spaces


def test_space_insert():
    """Space insertion should add spaces."""
    rng = random.Random(42)
    text = "abcdefghij" * 100
    result = apply_ocr_noise(
        text, rng, [],
        error_rate=0.0,
        space_drop_rate=0.0,
        space_insert_rate=0.5,
    )
    assert result.count(" ") > 0


def test_weighted_selection():
    """Higher-weight patterns should fire more often."""
    heavy = OcrPattern("a", "X", 100.0)
    light = OcrPattern("a", "Y", 0.01)
    patterns = [heavy, light]
    rng = random.Random(42)
    text = "a" * 1000
    result = apply_ocr_noise(text, rng, patterns, error_rate=1.0, space_drop_rate=0.0, space_insert_rate=0.0)
    x_count = result.count("X")
    y_count = result.count("Y")
    assert x_count > y_count * 10  # X should dominate


def test_latin_patterns_non_empty():
    assert len(LATIN_OCR_PATTERNS) > 0
    for p in LATIN_OCR_PATTERNS:
        assert isinstance(p, OcrPattern)


def test_hebrew_patterns_non_empty():
    assert len(HEBREW_OCR_PATTERNS) > 0
    for p in HEBREW_OCR_PATTERNS:
        assert isinstance(p, OcrPattern)

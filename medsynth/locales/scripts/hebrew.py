"""Hebrew script OCR patterns — single-char pair swaps + number-letter subs."""

from ..base import OcrPattern

# Bidirectional character confusion pairs (from real Hebrew OCR errors)
HEBREW_OCR_PATTERNS = [
    # Character pair confusions (bidirectional)
    OcrPattern("ר", "ד", 1.0),
    OcrPattern("ד", "ר", 1.0),
    OcrPattern("ה", "ח", 1.0),
    OcrPattern("ח", "ה", 1.0),
    OcrPattern("ב", "כ", 1.0),
    OcrPattern("כ", "ב", 1.0),
    OcrPattern("ו", "ז", 1.0),
    OcrPattern("ז", "ו", 1.0),
    OcrPattern("ג", "נ", 1.0),
    OcrPattern("נ", "ג", 1.0),
    OcrPattern("ע", "צ", 1.0),
    OcrPattern("צ", "ע", 1.0),
    OcrPattern("ם", "ס", 1.0),
    OcrPattern("ס", "ם", 1.0),
    OcrPattern("ת", "ח", 0.8),
    OcrPattern("ח", "ת", 0.8),
    # Number→letter OCR substitutions
    OcrPattern("1", "ו", 0.5),
    OcrPattern("0", "ס", 0.5),
    OcrPattern("6", "ב", 0.5),
    OcrPattern("9", "ף", 0.5),
]

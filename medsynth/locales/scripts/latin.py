"""Latin script OCR patterns — multi-char merges, single-char swaps, diacritic loss."""

from ..base import OcrPattern

LATIN_OCR_PATTERNS = [
    # Multi-char merges (segmentation failures)
    OcrPattern("rn", "m", 1.0),
    OcrPattern("m", "rn", 0.6),
    OcrPattern("cl", "d", 0.9),
    OcrPattern("d", "cl", 0.4),
    OcrPattern("vv", "w", 0.8),
    OcrPattern("w", "vv", 0.4),
    OcrPattern("ri", "n", 0.7),
    OcrPattern("li", "h", 0.6),
    OcrPattern("nn", "m", 0.5),
    # Single-char swaps
    OcrPattern("0", "O", 0.8),
    OcrPattern("O", "0", 0.8),
    OcrPattern("1", "l", 0.8),
    OcrPattern("l", "1", 0.8),
    OcrPattern("1", "I", 0.6),
    OcrPattern("I", "1", 0.6),
    OcrPattern("5", "S", 0.5),
    OcrPattern("S", "5", 0.5),
    OcrPattern("8", "B", 0.5),
    OcrPattern("B", "8", 0.5),
    OcrPattern("e", "c", 0.4),
    OcrPattern("c", "e", 0.4),
    OcrPattern("n", "h", 0.4),
    OcrPattern("h", "n", 0.4),
    OcrPattern("u", "v", 0.3),
    OcrPattern("v", "u", 0.3),
    # Diacritic loss (Spanish-relevant)
    OcrPattern("ñ", "n", 1.0),
    OcrPattern("á", "a", 1.0),
    OcrPattern("é", "e", 1.0),
    OcrPattern("í", "i", 1.0),
    OcrPattern("ó", "o", 1.0),
    OcrPattern("ú", "u", 1.0),
    OcrPattern("ü", "u", 1.0),
]

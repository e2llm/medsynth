"""Arabic script OCR patterns — dot-group confusions + diacritic stripping."""

from ..base import OcrPattern


def _group_confusions(chars: list[str], weight: float) -> list[OcrPattern]:
    """Generate all pairwise confusion patterns within a group."""
    patterns = []
    for i, src in enumerate(chars):
        for j, tgt in enumerate(chars):
            if i != j:
                patterns.append(OcrPattern(src, tgt, weight))
    return patterns


ARABIC_OCR_PATTERNS = [
    # --- Dot-group confusions (same base shape, differ only in dots) ---

    # Tooth: ba, ta, tha, nun, ya
    *_group_confusions(["ب", "ت", "ث", "ن", "ي"], 1.0),

    # Cup: jim, ha, kha
    *_group_confusions(["ج", "ح", "خ"], 1.0),

    # Hook: dal, dhal
    *_group_confusions(["د", "ذ"], 1.0),

    # Descender: ra, zay
    *_group_confusions(["ر", "ز"], 1.0),

    # Wave: sin, shin
    *_group_confusions(["س", "ش"], 1.0),

    # Closed oval: sad, dad
    *_group_confusions(["ص", "ض"], 1.0),

    # Tall oval: ta, dha
    *_group_confusions(["ط", "ظ"], 1.0),

    # Eye: ayn, ghayn
    *_group_confusions(["ع", "غ"], 1.0),

    # Loop: fa, qaf
    *_group_confusions(["ف", "ق"], 1.0),

    # --- Additional confusions ---

    # ha <-> ta marbuta
    OcrPattern("ه", "ة", 0.6),
    OcrPattern("ة", "ه", 0.6),

    # alif maqsura <-> ya
    OcrPattern("ى", "ي", 0.6),
    OcrPattern("ي", "ى", 0.6),

    # alif <-> lam
    OcrPattern("ا", "ل", 0.6),
    OcrPattern("ل", "ا", 0.6),

    # --- Diacritic / tashkeel stripping ---

    OcrPattern("\u064E", "", 0.8),  # fatha
    OcrPattern("\u064F", "", 0.8),  # damma
    OcrPattern("\u0650", "", 0.8),  # kasra
    OcrPattern("\u0652", "", 0.8),  # sukun
    OcrPattern("\u0651", "", 0.8),  # shadda
    OcrPattern("\u064B", "", 0.8),  # tanwin fathatan
    OcrPattern("\u064C", "", 0.8),  # tanwin dammatan
    OcrPattern("\u064D", "", 0.8),  # tanwin kasratan
]

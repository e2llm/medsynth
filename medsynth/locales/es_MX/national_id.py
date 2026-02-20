"""es_MX national ID: Mexican CURP (Clave Única de Registro de Población).

18-character alphanumeric code derived from name + DOB + gender + state.
"""

import random

INCONVENIENT_WORDS = {
    "BUEI", "CACA", "CAGA", "CAKA", "COGE", "COJA", "COJI", "COJO",
    "CULO", "FETO", "GUEY", "JOTO", "KACA", "KAGA", "KAKA", "KOGE",
    "KOJO", "KULO", "LOCA", "LOCO", "MAME", "MAMO", "MEAR", "MEAS",
    "MEON", "MION", "MOCO", "MULA", "PEDA", "PEDO", "PENE", "PUTA",
    "PUTO", "QULO", "RATA", "RUIN",
}


def _first_internal_consonant(s):
    """First internal consonant of a string (skip first char)."""
    consonants = "BCDFGHJKLMNPQRSTVWXYZ"
    for c in s[1:]:
        if c.upper() in consonants:
            return c.upper()
    return "X"


def _first_vowel(s):
    """First internal vowel of a string (skip first char)."""
    for c in s[1:]:
        if c.upper() in "AEIOU":
            return c.upper()
    return "X"


def generate_id(patient: dict, rng: random.Random) -> str:
    """Generate a Mexican CURP from patient data.

    Format: AAAA YYMMDD G SS CCC D V
    - AAAA: first letter paternal + first vowel paternal + first letter maternal + first letter first name
    - YYMMDD: date of birth
    - G: gender (H=male, M=female)
    - SS: state code (2 chars)
    - CCC: first internal consonant of each name part
    - D: disambiguator (digit if born <2000, letter if >=2000)
    - V: check digit (0-9)
    """
    # Strip accents for CURP computation
    def strip_accents(s):
        return (s.upper()
                .replace("\u00c1", "A").replace("\u00c9", "E")
                .replace("\u00cd", "I").replace("\u00d3", "O")
                .replace("\u00da", "U").replace("\u00dc", "U"))

    first = strip_accents(patient.get("first_name", "JUAN"))
    paternal = strip_accents(patient.get("last_name", "GARCIA"))
    maternal = strip_accents(patient.get("apellido_materno", "LOPEZ"))

    # First 4 chars
    c1 = paternal[0] if paternal else "X"
    c2 = _first_vowel(paternal) if len(paternal) > 1 else "X"
    c3 = maternal[0] if maternal else "X"
    c4 = first[0] if first else "X"
    first4 = f"{c1}{c2}{c3}{c4}"

    # Filter inconvenient words
    if first4 in INCONVENIENT_WORDS:
        first4 = first4[0] + "X" + first4[2:]

    # DOB: YYMMDD
    dob = patient.get("date_of_birth", "1980-01-01")
    yy = dob[2:4]
    mm = dob[5:7]
    dd = dob[8:10]

    # Gender: H=male, M=female
    gender = "H" if patient.get("gender") == "male" else "M"

    # State (2 chars) — default to Mexico City
    state = "DF"

    # Internal consonants: 1st from each name part
    ic1 = _first_internal_consonant(paternal)
    ic2 = _first_internal_consonant(maternal)
    ic3 = _first_internal_consonant(first)

    # Disambiguator (0-9 for born before 2000, A-Z for 2000+)
    year = int(dob[:4])
    disambig = str(rng.randint(0, 9)) if year < 2000 else chr(rng.randint(65, 90))

    # Check digit (0-9)
    check = rng.randint(0, 9)

    return f"{first4}{yy}{mm}{dd}{gender}{state}{ic1}{ic2}{ic3}{disambig}{check}"

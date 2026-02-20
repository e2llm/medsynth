"""es_AR national ID: Argentine DNI (7-8 digits) and CUIL."""

import random


def generate_id(patient: dict, rng: random.Random) -> str:
    """Generate Argentine DNI (7-8 digits, no check digit)."""
    # DNI range: ~5000000 to ~95000000
    number = rng.randint(5000000, 95000000)
    return str(number)


def generate_cuil(patient: dict, rng: random.Random) -> str:
    """Generate Argentine CUIL: XX-DDDDDDDD-C.

    XX = 20 (male), 27 (female), 23 (other).
    C = check digit via weighted sum mod 11.
    """
    gender = patient.get("gender", "male")
    if gender == "male":
        prefix = 20
    elif gender == "female":
        prefix = 27
    else:
        prefix = 23

    dni = rng.randint(5000000, 95000000)
    dni_str = str(dni).zfill(8)

    # CUIL check digit calculation
    full = f"{prefix}{dni_str}"
    weights = [5, 4, 3, 2, 7, 6, 5, 4, 3, 2]
    total = sum(int(d) * w for d, w in zip(full, weights))
    remainder = total % 11
    if remainder == 0:
        check = 0
    elif remainder == 1:
        check = 9 if prefix == 20 else 4
    else:
        check = 11 - remainder

    return f"{prefix}-{dni_str}-{check}"

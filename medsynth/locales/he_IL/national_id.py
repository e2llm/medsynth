"""he_IL national ID: Israeli 9-digit ID with Luhn variant checksum."""

import random


def generate_id(patient: dict, rng: random.Random) -> str:
    """Generate a valid Israeli ID with control digit (Luhn variant).

    patient is accepted for interface consistency but not used (Israeli IDs
    don't encode patient data).
    """
    digits = [rng.randint(0, 9) for _ in range(8)]
    total = 0
    for i, d in enumerate(digits):
        v = d * (1 + (i % 2))
        total += v // 10 + v % 10
    check = (10 - (total % 10)) % 10
    digits.append(check)
    return "".join(str(d) for d in digits)

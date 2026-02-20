"""ar_SA national ID: Saudi 10-digit ID with Luhn mod-10 checksum."""

import random


def generate_id(patient: dict, rng: random.Random) -> str:
    """Generate a valid Saudi national ID.

    10 digits: starts with 1 (citizen, 80%) or 2 (resident, 20%).
    Luhn mod-10 checksum on the last digit.

    patient is accepted for interface consistency but not used
    (Saudi IDs don't encode patient data).
    """
    # First digit: 1 (citizen) or 2 (resident)
    first = 1 if rng.random() < 0.8 else 2
    digits = [first] + [rng.randint(0, 9) for _ in range(8)]

    # Luhn checksum: even positions (0-indexed) are doubled
    total = 0
    for i, d in enumerate(digits):
        v = d * (2 if i % 2 == 0 else 1)
        total += v // 10 + v % 10
    check = (10 - (total % 10)) % 10
    digits.append(check)

    return "".join(str(d) for d in digits)

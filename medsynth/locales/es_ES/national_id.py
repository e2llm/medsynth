"""es_ES national ID: Spanish DNI — 8 digits + 1 control letter."""

import random


def generate_id(patient: dict, rng: random.Random) -> str:
    """Generate a valid Spanish DNI (8 digits + control letter).

    patient is accepted for interface consistency but not used.
    """
    number = rng.randint(10000000, 99999999)
    letters = "TRWAGMYFPDXBNJZSQVHLCKE"
    letter = letters[number % 23]
    return f"{number}{letter}"

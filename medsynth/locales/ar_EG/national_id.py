"""ar_EG national ID: Egyptian 14-digit ID encoding century, DOB, governorate, sequence, gender, check."""

import random


def generate_id(patient: dict, rng: random.Random) -> str:
    """Generate an Egyptian national ID (14 digits).

    Format: C-YYMMDD-GG-SSS-X-D (14 digits)
    - C: century (2=1900s, 3=2000s)
    - YYMMDD: date of birth
    - GG: governorate code (01-35)
    - SSS: 3-digit sequence number
    - X: gender digit (odd=male, even=female)
    - D: check digit
    """
    dob = patient.get("date_of_birth", "1980-01-01")
    year = int(dob[:4])
    century = 2 if year < 2000 else 3

    yy = f"{year % 100:02d}"
    mm = dob[5:7]
    dd = dob[8:10]

    gov = f"{rng.randint(1, 35):02d}"
    seq = f"{rng.randint(0, 999):03d}"

    gender = patient.get("gender", "male")
    gender_digit = rng.choice([1, 3, 5, 7, 9]) if gender == "male" else rng.choice([2, 4, 6, 8])

    partial = f"{century}{yy}{mm}{dd}{gov}{seq}{gender_digit}"
    check = sum(int(d) for d in partial) % 10

    return f"{partial}{check}"

"""Generate ground-truth patient pool."""

import random
from datetime import date, timedelta
from . import config
from .locales.base import LocaleConfig


def generate_patients(num_patients: int, seed: int, locale: LocaleConfig) -> list[dict]:
    """Return a list of ground-truth patient profiles."""
    rng = random.Random(seed)
    patients = []

    for _ in range(num_patients):
        gender = rng.choice(["male", "female"])
        name = locale.generate_name(gender, rng)
        dob = config.DOB_START + timedelta(days=rng.randint(0, config.DOB_RANGE_DAYS))
        age = (config.DOC_DATE_END - dob).days // 365
        num_conditions = rng.randint(0, config.MAX_CONDITIONS_PER_PATIENT)
        conditions = rng.sample(locale.conditions, min(num_conditions, len(locale.conditions)))
        num_meds = rng.randint(0, config.MAX_MEDICATIONS_PER_PATIENT)
        medications = rng.sample(locale.medications, min(num_meds, len(locale.medications)))

        city = rng.choice(locale.cities)
        street = rng.choice(locale.streets)
        house_num = rng.randint(1, config.MAX_HOUSE_NUMBER)

        # Generate ID here to preserve RNG sequence (original position in dict literal).
        # For locales where ID encodes patient data, a partial dict can be passed.
        partial_patient = {
            "first_name": name["first_name"],
            "last_name": name["last_name"],
            "full_name": name["full_name"],
            "gender": gender,
            "date_of_birth": dob.isoformat(),
            "age": age,
            "city": city,
        }
        patient_id = locale.generate_id(partial_patient, rng)

        patient = {
            "id": patient_id,
            "first_name": name["first_name"],
            "last_name": name["last_name"],
            "full_name": name["full_name"],
            "gender": gender,
            "date_of_birth": dob.isoformat(),
            "age": age,
            "address": locale.address_format.format(street=street, num=house_num, city=city),
            "city": city,
            "conditions": conditions,
            "icd10_codes": [locale.icd10_codes[c] for c in conditions if c in locale.icd10_codes],
            "medications": medications,
            "smoking": rng.random() < config.SMOKING_PREVALENCE,
            "blood_type": rng.choice(config.BLOOD_TYPES),
            "occupation": rng.choice(locale.occupations),
            "emergency_contact": locale.emergency_contact_name(rng),
        }
        patients.append(patient)

    return patients

"""ar_SA demographics: names, cities, streets, occupations."""

import random

MALE_GIVEN_NAMES = [
    "أحمد", "محمد", "عبدالله", "خالد", "فهد", "سلطان", "عبدالرحمن", "سعد",
    "فيصل", "نايف", "بندر", "تركي", "سعود", "عمر", "يوسف", "إبراهيم",
    "عبدالعزيز", "مشعل", "ماجد", "وليد", "حمد", "ناصر", "صالح", "راشد",
]

FEMALE_GIVEN_NAMES = [
    "نورة", "فاطمة", "سارة", "مريم", "عائشة", "هند", "لطيفة", "منيرة",
    "أمل", "ريم", "دانة", "لمى", "غادة", "هيفاء", "بسمة", "رنا",
    "جواهر", "نوف", "شيماء", "ابتسام", "حصة", "مها", "العنود", "لولوة",
]

FATHER_NAMES = [
    "محمد", "عبدالله", "عبدالرحمن", "سعود", "فهد", "صالح", "إبراهيم",
    "أحمد", "خالد", "عمر", "سعد", "ناصر", "عبدالعزيز", "سلطان",
    "حمد", "يوسف", "علي", "حسن", "راشد", "ماجد",
]

FAMILY_NAMES = [
    "العلي", "الشمري", "القحطاني", "العتيبي", "الدوسري", "الحربي",
    "المطيري", "الغامدي", "الزهراني", "السبيعي", "العنزي", "الرشيدي",
    "البلوي", "الجهني", "الثقفي", "المالكي", "السلمي", "الشهري",
    "الشهراني", "العسيري", "الخالدي", "المحمدي", "الأحمدي", "السعدي",
]

CITIES = [
    "الرياض", "جدة", "مكة المكرمة", "المدينة المنورة", "الدمام",
    "الخبر", "الظهران", "أبها", "تبوك", "حائل",
    "الطائف", "بريدة", "خميس مشيط", "نجران", "جازان",
    "ينبع", "الجبيل", "القطيف", "الأحساء", "عرعر",
]

STREETS = [
    "طريق الملك فهد", "طريق الملك عبدالله", "شارع التحلية",
    "شارع الأمير محمد بن عبدالعزيز", "طريق الملك عبدالعزيز",
    "شارع العليا", "شارع الستين", "طريق خريص",
    "طريق الدمام", "شارع الأمير سلطان", "طريق المدينة",
    "شارع فلسطين", "شارع الأندلس", "طريق الملك سلمان",
]

OCCUPATIONS = [
    "مهندس", "طبيب", "معلم", "محاسب", "ممرض", "سائق", "مقاول",
    "موظف حكومي", "ضابط", "تاجر", "محامي", "صيدلي", "فني", "مبرمج",
    "عسكري", "متقاعد", "طالب", "كاتب", "مدير", "رجل أعمال",
]


def generate_name(gender: str, rng: random.Random) -> dict:
    """Generate a Saudi Arabic name with patronymic.

    Returns dict with given, father, family, full_name.
    Full name = "{given} بن {father} {family}" for male,
                "{given} بنت {father} {family}" for female.
    """
    given = rng.choice(MALE_GIVEN_NAMES if gender == "male" else FEMALE_GIVEN_NAMES)
    father = rng.choice(FATHER_NAMES)
    family = rng.choice(FAMILY_NAMES)
    connector = "بن" if gender == "male" else "بنت"
    full_name = f"{given} {connector} {father} {family}"
    return {
        "given": given,
        "father": father,
        "family": family,
        "first_name": given,
        "last_name": family,
        "full_name": full_name,
    }


def emergency_contact_name(rng: random.Random) -> str:
    """Generate a random full name for emergency contact."""
    gender = rng.choice(["male", "female"])
    given = rng.choice(MALE_GIVEN_NAMES if gender == "male" else FEMALE_GIVEN_NAMES)
    father = rng.choice(FATHER_NAMES)
    family = rng.choice(FAMILY_NAMES)
    connector = "بن" if gender == "male" else "بنت"
    return f"{given} {connector} {father} {family}"

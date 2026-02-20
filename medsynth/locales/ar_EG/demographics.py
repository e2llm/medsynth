"""ar_EG demographics: names, cities, streets, occupations."""

import random

MALE_GIVEN_NAMES = [
    "محمد", "أحمد", "علي", "حسن", "إبراهيم", "عمر", "مصطفى", "خالد",
    "ياسر", "طارق", "محمود", "عبدالله", "كريم", "عمرو", "سامي", "هشام",
    "وائل", "شريف", "أشرف", "رامي", "حسام", "تامر", "مينا", "جورج",
]

FEMALE_GIVEN_NAMES = [
    "فاطمة", "نور", "سارة", "مريم", "ياسمين", "هبة", "إيمان", "دينا",
    "رنا", "سلمى", "هدى", "منى", "ليلى", "عبير", "نادية", "سمر",
    "غادة", "آية", "إسراء", "مروة", "داليا", "شيماء", "مارينا", "كريستين",
]

FATHER_NAMES = [
    "محمد", "أحمد", "علي", "حسن", "إبراهيم", "مصطفى", "عبدالله", "خالد",
    "محمود", "حسين", "عمر", "سعيد", "فؤاد", "رشدي", "جمال", "صلاح",
    "عادل", "ماهر", "سمير", "رمضان",
]

FAMILY_NAMES = [
    "الشريف", "المصري", "السيد", "حسن", "علي", "إبراهيم", "عبدالحميد",
    "الفقي", "الجندي", "البنا", "الشافعي", "المنشاوي", "عبدالرحمن",
    "الحسيني", "النجار", "الخولي", "الدسوقي", "البدري", "السباعي",
    "الطنطاوي", "العربي", "حبيب", "فرج", "مرسي",
]

CITIES = [
    "القاهرة", "الإسكندرية", "الجيزة", "شبرا الخيمة", "بورسعيد",
    "السويس", "المنصورة", "طنطا", "الزقازيق", "أسيوط",
    "المنيا", "سوهاج", "الفيوم", "بني سويف", "دمياط",
    "الإسماعيلية", "أسوان", "الأقصر", "قنا", "كفر الشيخ",
]

STREETS = [
    "شارع التحرير", "شارع رمسيس", "شارع الهرم", "شارع فيصل",
    "كورنيش النيل", "شارع الجمهورية", "شارع مصطفى النحاس",
    "شارع عباس العقاد", "شارع جامعة الدول العربية", "طريق النصر",
    "شارع الثورة", "شارع بورسعيد", "شارع السودان", "شارع شبرا",
]

OCCUPATIONS = [
    "مهندس", "طبيب", "مدرس", "محاسب", "ممرض", "سائق", "عامل",
    "موظف حكومي", "ضابط شرطة", "تاجر", "محامي", "صيدلي", "فني",
    "مبرمج", "مجند", "متقاعد", "طالب", "صحفي", "مدير", "مزارع",
]


def generate_name(gender: str, rng: random.Random) -> dict:
    """Generate an Egyptian name: given + father + family."""
    given = rng.choice(MALE_GIVEN_NAMES if gender == "male" else FEMALE_GIVEN_NAMES)
    father = rng.choice(FATHER_NAMES)
    family = rng.choice(FAMILY_NAMES)
    return {
        "first_name": given,
        "father_name": father,
        "family_name": family,
        "last_name": family,
        "full_name": f"{given} {father} {family}",
    }


def emergency_contact_name(rng: random.Random) -> str:
    """Generate a random full name for emergency contact."""
    given = rng.choice(MALE_GIVEN_NAMES + FEMALE_GIVEN_NAMES)
    father = rng.choice(FATHER_NAMES)
    family = rng.choice(FAMILY_NAMES)
    return f"{given} {father} {family}"

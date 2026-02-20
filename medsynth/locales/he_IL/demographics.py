"""he_IL demographics: names, cities, streets, occupations."""

import random

MALE_FIRST_NAMES = [
    "יוסף", "משה", "דוד", "אברהם", "יעקב", "מוחמד", "אחמד", "חיים",
    "שלמה", "דניאל", "עומר", "איתי", "נועם", "אריאל", "יונתן", "אלון",
    "רון", "גיל", "עידו", "תומר", "אורי", "מתן", "ליאם", "אדם",
]

FEMALE_FIRST_NAMES = [
    "שרה", "רחל", "לאה", "מרים", "חנה", "פאטמה", "נועה", "יעל",
    "תמר", "שירה", "מאיה", "ליאן", "אמילי", "הילה", "דנה", "רותם",
    "עדי", "אורלי", "מיכל", "ענת", "סיגל", "גלית", "אפרת", "ורד",
]

LAST_NAMES = [
    "כהן", "לוי", "מזרחי", "פרץ", "ביטון", "דהן", "אברהם", "פרידמן",
    "שלום", "מלכה", "אזולאי", "חדד", "יוסף", "דוד", "גולן", "בן דוד",
    "עמר", "שמעוני", "אלון", "רוזנברג", "ברק", "חיון", "סויסה", "אוחנה",
]

CITIES = [
    "תל אביב", "ירושלים", "חיפה", "באר שבע", "ראשון לציון",
    "פתח תקווה", "אשדוד", "נתניה", "חולון", "בני ברק",
    "רמת גן", "אשקלון", "בת ים", "הרצליה", "כפר סבא",
    "רעננה", "לוד", "רמלה", "עכו", "נצרת",
    "טבריה", "צפת", "קריית שמונה", "דימונה", "אילת",
]

STREETS = [
    "הרצל", "בן גוריון", "ז'בוטינסקי", "רוטשילד", "אלנבי",
    "דיזנגוף", "בלפור", "ויצמן", "סוקולוב", "ביאליק",
    "שדרות ירושלים", "שדרות העצמאות", "דרך השלום", "רחוב הנביאים",
]

OCCUPATIONS = [
    "מהנדס", "מורה", "אחות", "רופא", "עורך דין", "חשבונאי",
    "נהג", "קבלן", "פועל בניין", "מזכירה", "עובד סוציאלי",
    "שוטר", "חייל", "סטודנט", "גמלאי", "עקרת בית",
    "מתכנת", "טכנאי", "צלם", "עיתונאי", "שף",
]


def generate_name(gender: str, rng: random.Random) -> dict:
    """Generate a Hebrew name. Returns dict with first_name, last_name, full_name."""
    first = rng.choice(MALE_FIRST_NAMES if gender == "male" else FEMALE_FIRST_NAMES)
    last = rng.choice(LAST_NAMES)
    return {
        "first_name": first,
        "last_name": last,
        "full_name": f"{first} {last}",
    }


def emergency_contact_name(rng: random.Random) -> str:
    """Generate a random full name for emergency contact."""
    first = rng.choice(MALE_FIRST_NAMES + FEMALE_FIRST_NAMES)
    last = rng.choice(LAST_NAMES)
    return f"{first} {last}"

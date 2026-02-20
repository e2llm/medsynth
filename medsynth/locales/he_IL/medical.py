"""he_IL medical data: conditions, medications, departments, lab tests, ICD-10."""

CONDITIONS = [
    "סוכרת סוג 2", "יתר לחץ דם", "מחלת לב כלילית", "COPD",
    "אסתמה", "אי ספיקת כליות כרונית", "דלקת מפרקים", "השמנת יתר",
    "דיכאון", "דמנציה", "אוסטאופורוזיס", "אנמיה",
    "שבץ מוחי", "אי ספיקת לב", "פרפור פרוזדורים",
    "היפרליפידמיה", "גאוט", "מחלת כבד שומני",
]

MEDICATIONS = [
    "מטפורמין", "אינסולין", "אספירין", "אמלודיפין", "אטורבסטטין",
    "אומפרזול", "רמיפריל", "מטופרולול", "סימבסטטין", "לוסרטן",
    "קלופידוגרל", "וורפרין", "פרוקסטין", "דיקלופנק", "איבופרופן",
    "גבפנטין", "אלנדרונט", "לבותירוקסין", "הידרוכלורותיאזיד",
]

DEPARTMENTS = [
    "פנימית א", "פנימית ב", "קרדיולוגיה", "נוירולוגיה",
    "כירורגיה כללית", "אורתופדיה", "ריאות", "אורולוגיה",
    "גסטרואנטרולוגיה", "נפרולוגיה", "אנדוקרינולוגיה",
    "אונקולוגיה", "גריאטריה", "מיון",
]

ICD10_CODES = {
    "סוכרת סוג 2": "E11",
    "יתר לחץ דם": "I10",
    "מחלת לב כלילית": "I25",
    "COPD": "J44",
    "אסתמה": "J45",
    "אי ספיקת כליות כרונית": "N18",
    "דלקת מפרקים": "M19",
    "השמנת יתר": "E66",
    "דיכאון": "F32",
    "דמנציה": "F03",
    "אוסטאופורוזיס": "M81",
    "אנמיה": "D64",
    "שבץ מוחי": "I63",
    "אי ספיקת לב": "I50",
    "פרפור פרוזדורים": "I48",
    "היפרליפידמיה": "E78",
    "גאוט": "M10",
    "מחלת כבד שומני": "K76",
}

LAB_TESTS = [
    {"name": "גלוקוז", "unit": "mg/dL", "normal_range": (70, 100), "abnormal_range": (101, 400)},
    {"name": "המוגלובין", "unit": "g/dL", "normal_range": (12.0, 17.5), "abnormal_range": (6.0, 11.9)},
    {"name": "HbA1c", "unit": "%", "normal_range": (4.0, 5.6), "abnormal_range": (5.7, 14.0)},
    {"name": "קריאטינין", "unit": "mg/dL", "normal_range": (0.7, 1.3), "abnormal_range": (1.4, 8.0)},
    {"name": "כולסטרול כללי", "unit": "mg/dL", "normal_range": (0, 200), "abnormal_range": (201, 350)},
    {"name": "LDL", "unit": "mg/dL", "normal_range": (0, 100), "abnormal_range": (101, 250)},
    {"name": "HDL", "unit": "mg/dL", "normal_range": (40, 100), "abnormal_range": (10, 39)},
    {"name": "טריגליצרידים", "unit": "mg/dL", "normal_range": (0, 150), "abnormal_range": (151, 500)},
    {"name": "TSH", "unit": "mIU/L", "normal_range": (0.4, 4.0), "abnormal_range": (0.01, 0.39)},
    {"name": "סודיום", "unit": "mEq/L", "normal_range": (136, 145), "abnormal_range": (120, 135)},
    {"name": "אשלגן", "unit": "mEq/L", "normal_range": (3.5, 5.0), "abnormal_range": (2.5, 3.4)},
    {"name": "WBC", "unit": "K/uL", "normal_range": (4.5, 11.0), "abnormal_range": (1.0, 4.4)},
    {"name": "PLT", "unit": "K/uL", "normal_range": (150, 400), "abnormal_range": (50, 149)},
    {"name": "ALT", "unit": "U/L", "normal_range": (7, 56), "abnormal_range": (57, 500)},
    {"name": "AST", "unit": "U/L", "normal_range": (10, 40), "abnormal_range": (41, 400)},
    {"name": "GFR", "unit": "mL/min", "normal_range": (90, 120), "abnormal_range": (15, 89)},
]

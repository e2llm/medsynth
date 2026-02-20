"""ar_EG medical data: conditions, medications, departments, lab tests, ICD-10.

Egyptian medical terminology uses Modern Standard Arabic, identical to ar_SA.
"""

CONDITIONS = [
    "داء السكري النوع الثاني", "ارتفاع ضغط الدم", "مرض الشريان التاجي", "COPD",
    "الربو", "القصور الكلوي المزمن", "التهاب المفاصل", "السمنة",
    "الاكتئاب", "الخرف", "هشاشة العظام", "فقر الدم",
    "السكتة الدماغية", "قصور القلب", "الرجفان الأذيني",
    "فرط شحميات الدم", "النقرس", "مرض الكبد الدهني",
]

MEDICATIONS = [
    "ميتفورمين", "أنسولين", "أسبرين", "أملوديبين", "أتورفاستاتين",
    "أوميبرازول", "راميبريل", "ميتوبرولول", "سيمفاستاتين", "لوسارتان",
    "كلوبيدوغريل", "وارفارين", "باروكسيتين", "ديكلوفيناك", "إيبوبروفين",
    "غابابنتين", "أليندرونات", "ليفوثيروكسين", "هيدروكلوروثيازيد",
]

DEPARTMENTS = [
    "الباطنة", "القلب", "الأعصاب",
    "الجراحة العامة", "العظام", "الصدر", "المسالك البولية",
    "الجهاز الهضمي", "الكلى", "الغدد الصماء",
    "الأورام", "الشيخوخة", "الطوارئ",
]

ICD10_CODES = {
    "داء السكري النوع الثاني": "E11",
    "ارتفاع ضغط الدم": "I10",
    "مرض الشريان التاجي": "I25",
    "COPD": "J44",
    "الربو": "J45",
    "القصور الكلوي المزمن": "N18",
    "التهاب المفاصل": "M19",
    "السمنة": "E66",
    "الاكتئاب": "F32",
    "الخرف": "F03",
    "هشاشة العظام": "M81",
    "فقر الدم": "D64",
    "السكتة الدماغية": "I63",
    "قصور القلب": "I50",
    "الرجفان الأذيني": "I48",
    "فرط شحميات الدم": "E78",
    "النقرس": "M10",
    "مرض الكبد الدهني": "K76",
}

LAB_TESTS = [
    {"name": "جلوكوز", "unit": "mg/dL", "normal_range": (70, 100), "abnormal_range": (101, 400)},
    {"name": "هيموغلوبين", "unit": "g/dL", "normal_range": (12.0, 17.5), "abnormal_range": (6.0, 11.9)},
    {"name": "HbA1c", "unit": "%", "normal_range": (4.0, 5.6), "abnormal_range": (5.7, 14.0)},
    {"name": "كرياتينين", "unit": "mg/dL", "normal_range": (0.7, 1.3), "abnormal_range": (1.4, 8.0)},
    {"name": "كولسترول كلي", "unit": "mg/dL", "normal_range": (0, 200), "abnormal_range": (201, 350)},
    {"name": "LDL", "unit": "mg/dL", "normal_range": (0, 100), "abnormal_range": (101, 250)},
    {"name": "HDL", "unit": "mg/dL", "normal_range": (40, 100), "abnormal_range": (10, 39)},
    {"name": "دهون ثلاثية", "unit": "mg/dL", "normal_range": (0, 150), "abnormal_range": (151, 500)},
    {"name": "TSH", "unit": "mIU/L", "normal_range": (0.4, 4.0), "abnormal_range": (0.01, 0.39)},
    {"name": "صوديوم", "unit": "mEq/L", "normal_range": (136, 145), "abnormal_range": (120, 135)},
    {"name": "بوتاسيوم", "unit": "mEq/L", "normal_range": (3.5, 5.0), "abnormal_range": (2.5, 3.4)},
    {"name": "WBC", "unit": "K/uL", "normal_range": (4.5, 11.0), "abnormal_range": (1.0, 4.4)},
    {"name": "PLT", "unit": "K/uL", "normal_range": (150, 400), "abnormal_range": (50, 149)},
    {"name": "ALT", "unit": "U/L", "normal_range": (7, 56), "abnormal_range": (57, 500)},
    {"name": "AST", "unit": "U/L", "normal_range": (10, 40), "abnormal_range": (41, 400)},
    {"name": "GFR", "unit": "mL/min", "normal_range": (90, 120), "abnormal_range": (15, 89)},
]

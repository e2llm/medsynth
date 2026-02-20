"""es_ES medical data: conditions, medications, departments, lab tests, ICD-10."""

CONDITIONS = [
    "diabetes tipo 2", "hipertensión arterial", "enfermedad coronaria", "EPOC",
    "asma", "insuficiencia renal crónica", "artritis", "obesidad",
    "depresión", "demencia", "osteoporosis", "anemia",
    "ictus", "insuficiencia cardíaca", "fibrilación auricular",
    "hiperlipidemia", "gota", "enfermedad hepática grasa",
]

MEDICATIONS = [
    "metformina", "insulina", "aspirina", "amlodipino", "atorvastatina",
    "omeprazol", "ramipril", "metoprolol", "simvastatina", "losartán",
    "clopidogrel", "warfarina", "paroxetina", "diclofenaco", "ibuprofeno",
    "gabapentina", "alendronato", "levotiroxina", "hidroclorotiazida",
]

DEPARTMENTS = [
    "medicina interna", "cardiología", "neurología", "cirugía general",
    "traumatología", "neumología", "urología", "digestivo",
    "nefrología", "endocrinología", "oncología", "geriatría",
    "urgencias", "UCI",
]

ICD10_CODES = {
    "diabetes tipo 2": "E11",
    "hipertensión arterial": "I10",
    "enfermedad coronaria": "I25",
    "EPOC": "J44",
    "asma": "J45",
    "insuficiencia renal crónica": "N18",
    "artritis": "M19",
    "obesidad": "E66",
    "depresión": "F32",
    "demencia": "F03",
    "osteoporosis": "M81",
    "anemia": "D64",
    "ictus": "I63",
    "insuficiencia cardíaca": "I50",
    "fibrilación auricular": "I48",
    "hiperlipidemia": "E78",
    "gota": "M10",
    "enfermedad hepática grasa": "K76",
}

LAB_TESTS = [
    {"name": "glucosa", "unit": "mg/dL", "normal_range": (70, 100), "abnormal_range": (101, 400)},
    {"name": "hemoglobina", "unit": "g/dL", "normal_range": (12.0, 17.5), "abnormal_range": (6.0, 11.9)},
    {"name": "HbA1c", "unit": "%", "normal_range": (4.0, 5.6), "abnormal_range": (5.7, 14.0)},
    {"name": "creatinina", "unit": "mg/dL", "normal_range": (0.7, 1.3), "abnormal_range": (1.4, 8.0)},
    {"name": "colesterol total", "unit": "mg/dL", "normal_range": (0, 200), "abnormal_range": (201, 350)},
    {"name": "LDL", "unit": "mg/dL", "normal_range": (0, 100), "abnormal_range": (101, 250)},
    {"name": "HDL", "unit": "mg/dL", "normal_range": (40, 100), "abnormal_range": (10, 39)},
    {"name": "triglicéridos", "unit": "mg/dL", "normal_range": (0, 150), "abnormal_range": (151, 500)},
    {"name": "TSH", "unit": "mIU/L", "normal_range": (0.4, 4.0), "abnormal_range": (0.01, 0.39)},
    {"name": "sodio", "unit": "mEq/L", "normal_range": (136, 145), "abnormal_range": (120, 135)},
    {"name": "potasio", "unit": "mEq/L", "normal_range": (3.5, 5.0), "abnormal_range": (2.5, 3.4)},
    {"name": "WBC", "unit": "K/uL", "normal_range": (4.5, 11.0), "abnormal_range": (1.0, 4.4)},
    {"name": "PLT", "unit": "K/uL", "normal_range": (150, 400), "abnormal_range": (50, 149)},
    {"name": "ALT", "unit": "U/L", "normal_range": (7, 56), "abnormal_range": (57, 500)},
    {"name": "AST", "unit": "U/L", "normal_range": (10, 40), "abnormal_range": (41, 400)},
    {"name": "GFR", "unit": "mL/min", "normal_range": (90, 120), "abnormal_range": (15, 89)},
]

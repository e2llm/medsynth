"""ar_SA free text generation config: prompts, styles, abbreviations, templates."""

SYSTEM_PROMPT = "أنت طبيب سعودي تكتب تقارير طبية. اكتب بالعربية مع استخدام المصطلحات الطبية الإنجليزية عند الحاجة. لا تضف شروحات أو نصوص وصفية — فقط التقرير الطبي."

FACILITY_STYLES = {
    "riyadh": "أسلوب مفصل ومنظم بمعايير FHIR. تقارير شاملة بمصطلحات إنجليزية طبية. مبنى واضح: التاريخ المرضي، الفحص، الخطة العلاجية، التوصيات.",
    "malaki": "أسلوب مختلط عربي/إنجليزي. استخدام اختصارات طبية إنجليزية شائعة (DM, HTN, IHD). مبنى شبه رسمي مع ملاحظات سريرية.",
    "hayat": "أسلوب مختصر جداً. ملاحظات قصيرة لنتائج المختبر فقط. جملة أو جملتان.",
    "phc": "أسلوب قصير ومباشر. تسجيل سريري بسيط. اختصارات كثيرة. بدون هيكل موحد.",
}

DOC_TYPE_CONTEXTS = {
    "discharge": "تقرير خروج من المستشفى. يشمل: سبب الدخول، المسار العلاجي، العلاجات، التوصيات للمتابعة.",
    "lab": "ملاحظات على نتائج المختبر. مختصر جداً — تفسير سريري للنتائج.",
    "visit": "ملخص زيارة عيادة. الشكوى الرئيسية، الفحص، الانطباع، الخطة.",
    "referral": "خطاب إحالة لاستشارة/علاج. الخلفية المرضية، سبب الإحالة، الأولوية.",
}

MEDICAL_ABBREVIATIONS = "DM (السكري), HTN (ارتفاع الضغط), IHD (مرض القلب), COPD (الانسداد الرئوي), CKD (الفشل الكلوي), AF (الرجفان الأذيني)"

CONTRADICTION_TEMPLATES = {
    "smoking_yes": "مدخن منذ 20 سنة",
    "smoking_no": "غير مدخن، لم يدخن أبداً",
    "age": "عمره {age} سنة",
    "medication": "يتناول {med} بشكل منتظم",
}

FALLBACK_STRINGS = {
    "no_conditions": "لا يوجد أمراض مزمنة",
    "no_medications": "لا يتناول أدوية",
    "no_diagnosis": "لا يوجد",
    "referral_default": "للتقييم",
}


def format_patient_context(patient: dict) -> str:
    """Format patient data for LLM prompt (Arabic)."""
    conditions_str = ", ".join(patient["conditions"]) if patient["conditions"] else "لا يوجد أمراض مزمنة"
    medications_str = ", ".join(patient["medications"]) if patient["medications"] else "لا يتناول أدوية"
    return (
        f"بيانات المريض:\n"
        f"- الاسم: {patient['full_name']}\n"
        f"- العمر: {patient['age']}\n"
        f"- الجنس: {'ذكر' if patient['gender'] == 'male' else 'أنثى'}\n"
        f"- الأمراض المزمنة: {conditions_str}\n"
        f"- الأدوية: {medications_str}\n"
        f"- التدخين: {'نعم' if patient['smoking'] else 'لا'}"
    )


def format_clinical_prompt(
    patient: dict,
    facility_id: str,
    doc_type: str,
    contradiction: dict | None = None,
) -> str:
    """Assemble the full clinical text generation prompt (Arabic with English code-switching)."""
    patient_context = format_patient_context(patient)

    prompt = f"""اكتب نصاً سريرياً طبياً بالعربية لمستند من نوع: {DOC_TYPE_CONTEXTS[doc_type]}

{patient_context}

أسلوب المنشأة: {FACILITY_STYLES[facility_id]}

تعليمات:
- اكتب 1-3 فقرات فقط
- استخدم الاختصارات الطبية المعتمدة: {MEDICAL_ABBREVIATIONS}
- استخدم المصطلحات الطبية الإنجليزية عند الحاجة (code-switching طبيعي كما يكتب الأطباء السعوديون)
- أضف أخطاء إملائية بسيطة (1-2) كأنها من طبيب يكتب بسرعة
- لا تضف عناوين أو تنسيق خاص — فقط نص متصل"""

    if contradiction:
        prompt += f"""

مهم: في النص، اذكر بوضوح أن {contradiction['text_should_say']}. يجب أن يبدو طبيعياً كجزء من التقرير الطبي."""

    prompt += """
- إذا كان مناسباً، اذكر تفاصيل إضافية غير موجودة في البيانات المهيكلة (مثلاً: الحالة الاجتماعية، الحساسية، تفاصيل التاريخ المرضي)"""

    return prompt

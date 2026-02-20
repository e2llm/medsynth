"""ar_EG free text generation config: prompts, styles, abbreviations, templates."""

SYSTEM_PROMPT = "أنت طبيب مصري تكتب تقارير طبية. اكتب بالعربية مع استخدام المصطلحات الطبية الإنجليزية عند الحاجة. لا تضف شروحات — فقط التقرير الطبي."

FACILITY_STYLES = {
    "nile": "أسلوب أكاديمي مفصل. تقارير طويلة بهيكل واضح: التاريخ المرضي، الفحص، التشخيص، الخطة العلاجية والتوصيات.",
    "delta": "أسلوب متوسط بالعربية. استخدام اختصارات طبية شائعة. مبنى شبه رسمي مع تفاصيل سريرية كافية.",
    "almokhtabar": "أسلوب مختصر جداً. ملاحظات قصيرة على نتائج المعمل فقط. جملة أو اثنتين.",
    "tahrir": "أسلوب قصير ومباشر. تسجيل سريري مختصر. اختصارات كثيرة. بدون هيكل موحد.",
}

DOC_TYPE_CONTEXTS = {
    "discharge": "ملخص خروج من المستشفى. يشمل: سبب الدخول، المسار العلاجي، العلاجات، توصيات المتابعة.",
    "lab": "ملاحظات على نتائج المعمل. مختصر جداً — تفسير سريري للنتائج.",
    "visit": "ملخص زيارة العيادة. الشكوى الرئيسية، الفحص، الانطباع، الخطة.",
    "referral": "خطاب إحالة للاستشارة/العلاج. الخلفية المرضية، سبب الإحالة، الأولوية.",
}

MEDICAL_ABBREVIATIONS = "DM (سكري), HTN (ضغط), IHD (قلب), CKD (كلى), COPD (انسداد رئوي), ECG (رسم قلب), CBC (صورة دم), LFT (وظائف كبد), KFT (وظائف كلى)"

CONTRADICTION_TEMPLATES = {
    "smoking_yes": "مدخن من 20 سنة",
    "smoking_no": "مش بيدخن خالص",
    "age": "عنده {age} سنة",
    "medication": "بياخد {med} بانتظام",
}

FALLBACK_STRINGS = {
    "no_conditions": "مفيش أمراض مزمنة",
    "no_medications": "مش بياخد أدوية",
    "no_diagnosis": "لا يوجد",
    "referral_default": "للفحص",
}


def format_patient_context(patient: dict) -> str:
    """Format patient data for LLM prompt (Arabic)."""
    conditions_str = "، ".join(patient["conditions"]) if patient["conditions"] else "مفيش أمراض مزمنة"
    medications_str = "، ".join(patient["medications"]) if patient["medications"] else "مش بياخد أدوية"
    return (
        f"بيانات المريض:\n"
        f"- الاسم: {patient['full_name']}\n"
        f"- السن: {patient['age']}\n"
        f"- النوع: {'ذكر' if patient['gender'] == 'male' else 'أنثى'}\n"
        f"- الأمراض المزمنة: {conditions_str}\n"
        f"- الأدوية: {medications_str}\n"
        f"- التدخين: {'أيوه' if patient['smoking'] else 'لأ'}"
    )


def format_clinical_prompt(
    patient: dict,
    facility_id: str,
    doc_type: str,
    contradiction: dict | None = None,
) -> str:
    """Assemble the full clinical text generation prompt (Arabic)."""
    patient_context = format_patient_context(patient)

    prompt = f"""اكتب نص طبي سريري بالعربية لمستند من نوع: {DOC_TYPE_CONTEXTS[doc_type]}

{patient_context}

أسلوب المنشأة: {FACILITY_STYLES[facility_id]}

تعليمات:
- اكتب من 1 إلى 3 فقرات فقط
- استخدم الاختصارات الطبية المتعارف عليها: {MEDICAL_ABBREVIATIONS}
- أضف خطأ إملائي بسيط أو اثنين زي ما الدكتور بيكتب بسرعة
- متضفش عناوين أو تنسيق خاص — نص عادي بس"""

    if contradiction:
        prompt += f"""

مهم: في النص، اذكر بوضوح إن {contradiction['text_should_say']}. لازم يبان طبيعي كجزء من التقرير الطبي."""

    prompt += """
- لو مناسب، اذكر تفاصيل إضافية مش موجودة في البيانات المنظمة (مثلاً: الحالة الاجتماعية، حساسية، تفاصيل التاريخ المرضي)"""

    return prompt

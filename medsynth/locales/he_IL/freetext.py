"""he_IL free text generation config: prompts, styles, abbreviations, templates."""

SYSTEM_PROMPT = "אתה רופא ישראלי שכותב סיכומים רפואיים. כתוב בעברית בלבד. אל תוסיף הסברים או מטא-טקסט — רק את הסיכום הרפואי עצמו."

FACILITY_STYLES = {
    "alon": "סגנון מפורט ומקצועי. סיכומים ארוכים עם מבנה ברור: רקע, מהלך, סיכום והמלצות.",
    "hadarim": "סגנון ממוצע. שימוש בקיצורים רפואיים נפוצים (ס.ד, ל.ד, ח.ד). מבנה חצי-פורמלי.",
    "ofek": "סגנון תמציתי מאוד. רק הערות קצרות לתוצאות מעבדה. 1-2 משפטים.",
    "shaked": "סגנון קצר וישיר. רישום קליני מינימלי. קיצורים רבים. ללא מבנה אחיד.",
}

DOC_TYPE_CONTEXTS = {
    "discharge": "סיכום שחרור מאשפוז. כולל: סיבת אשפוז, מהלך, טיפולים, המלצות לקהילה.",
    "lab": "הערות לתוצאות מעבדה. קצר מאוד — פרשנות קלינית של התוצאות.",
    "visit": "סיכום ביקור מרפאה. תלונה עיקרית, בדיקה, רושם, תוכנית.",
    "referral": "מכתב הפניה לייעוץ/טיפול. רקע, סיבת ההפניה, דחיפות.",
}

MEDICAL_ABBREVIATIONS = "ס.ד (סוכרת), ל.ד (לחץ דם), ח.ד (חדר), טל\"ד (טונוס לחץ דם), צנ\"ל (צנתור לב), א.ק.ג (אלקטרוקרדיוגרמה)"

CONTRADICTION_TEMPLATES = {
    "smoking_yes": "מעשן 20 שנה",
    "smoking_no": "לא מעשן, מעולם לא עישן",
    "age": "בן {age}",
    "medication": "נוטל {med} באופן קבוע",
}

FALLBACK_STRINGS = {
    "no_conditions": "ללא מחלות רקע ידועות",
    "no_medications": "ללא תרופות קבועות",
    "no_diagnosis": "ללא",
    "referral_default": "בירור",
}


def format_patient_context(patient: dict) -> str:
    """Format patient data for LLM prompt."""
    conditions_str = ", ".join(patient["conditions"]) if patient["conditions"] else "ללא מחלות רקע ידועות"
    medications_str = ", ".join(patient["medications"]) if patient["medications"] else "ללא תרופות קבועות"
    return (
        f"פרטי המטופל:\n"
        f"- שם: {patient['full_name']}\n"
        f"- גיל: {patient['age']}\n"
        f"- מין: {'זכר' if patient['gender'] == 'male' else 'נקבה'}\n"
        f"- מחלות רקע: {conditions_str}\n"
        f"- תרופות: {medications_str}\n"
        f"- עישון: {'כן' if patient['smoking'] else 'לא'}"
    )


def format_clinical_prompt(
    patient: dict,
    facility_id: str,
    doc_type: str,
    contradiction: dict | None = None,
) -> str:
    """Assemble the full clinical text generation prompt (Hebrew)."""
    patient_context = format_patient_context(patient)

    prompt = f"""כתוב טקסט קליני רפואי בעברית עבור מסמך מסוג: {DOC_TYPE_CONTEXTS[doc_type]}

{patient_context}

סגנון המוסד: {FACILITY_STYLES[facility_id]}

הנחיות:
- כתוב 1-3 פסקאות בלבד
- השתמש בקיצורים רפואיים מקובלים: {MEDICAL_ABBREVIATIONS}
- הוסף שגיאות כתיב קלות (1-2) כמו רופא שכותב מהר
- אל תוסיף כותרות או פורמט מיוחד — רק טקסט רץ"""

    if contradiction:
        prompt += f"""

חשוב: בטקסט, הזכר בצורה ברורה ש{contradiction['text_should_say']}. זה צריך להיראות טבעי כחלק מהסיכום הרפואי."""

    prompt += """
- אם מתאים, הזכר פרטים נוספים שלא מופיעים בנתונים המובנים (למשל: מצב משפחתי, אלרגיות, פרטי אנמנזה)"""

    return prompt

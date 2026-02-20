"""es_ES free text generation config: prompts, styles, abbreviations, templates."""

SYSTEM_PROMPT = "Eres un médico español que redacta informes clínicos. Escribe en español. No añadas explicaciones ni texto adicional — solo el informe médico."

FACILITY_STYLES = {
    "reina": "Estilo detallado y profesional. Informes extensos con estructura clara: antecedentes, evolución, resumen y recomendaciones al alta.",
    "san_rafael": "Estilo medio. Uso de abreviaturas médicas habituales (HTA, DM, FA). Estructura semi-formal con párrafos breves.",
    "iberia": "Estilo muy conciso. Solo notas breves para resultados de laboratorio. 1-2 frases.",
    "atencion": "Estilo corto y directo. Registro clínico mínimo. Muchas abreviaturas. Sin estructura uniforme.",
}

DOC_TYPE_CONTEXTS = {
    "discharge": "Informe de alta hospitalaria. Incluye: motivo de ingreso, evolución, tratamientos, recomendaciones al alta.",
    "lab": "Notas sobre resultados de laboratorio. Muy breve — interpretación clínica de los resultados.",
    "visit": "Resumen de consulta ambulatoria. Motivo de consulta, exploración, impresión diagnóstica, plan.",
    "referral": "Carta de derivación para valoración/tratamiento. Antecedentes, motivo de derivación, urgencia.",
}

MEDICAL_ABBREVIATIONS = "HTA (hipertensión), DM (diabetes), EPOC, IAM (infarto agudo), ICC (insuficiencia cardíaca), FA (fibrilación auricular), IRC (insuficiencia renal), TAC (tomografía)"

CONTRADICTION_TEMPLATES = {
    "smoking_yes": "fumador de 20 años",
    "smoking_no": "no fumador, nunca ha fumado",
    "age": "paciente de {age} años",
    "medication": "en tratamiento con {med}",
}

FALLBACK_STRINGS = {
    "no_conditions": "sin antecedentes de interés",
    "no_medications": "sin tratamiento habitual",
    "no_diagnosis": "sin diagnóstico",
    "referral_default": "estudio",
}


def format_patient_context(patient: dict) -> str:
    """Format patient data for LLM prompt."""
    conditions_str = ", ".join(patient["conditions"]) if patient["conditions"] else "sin antecedentes de interés"
    medications_str = ", ".join(patient["medications"]) if patient["medications"] else "sin tratamiento habitual"
    return (
        f"Datos del paciente:\n"
        f"- Nombre: {patient['full_name']}\n"
        f"- Edad: {patient['age']}\n"
        f"- Sexo: {'hombre' if patient['gender'] == 'male' else 'mujer'}\n"
        f"- Antecedentes: {conditions_str}\n"
        f"- Medicación: {medications_str}\n"
        f"- Tabaquismo: {'sí' if patient['smoking'] else 'no'}"
    )


def format_clinical_prompt(
    patient: dict,
    facility_id: str,
    doc_type: str,
    contradiction: dict | None = None,
) -> str:
    """Assemble the full clinical text generation prompt (Spanish)."""
    patient_context = format_patient_context(patient)

    prompt = f"""Escribe un texto clínico médico en español para un documento de tipo: {DOC_TYPE_CONTEXTS[doc_type]}

{patient_context}

Estilo del centro: {FACILITY_STYLES[facility_id]}

Instrucciones:
- Escribe 1-3 párrafos únicamente
- Usa abreviaturas médicas habituales: {MEDICAL_ABBREVIATIONS}
- Añade errores ortográficos leves (1-2) como un médico que escribe rápido
- No añadas títulos ni formato especial — solo texto corrido"""

    if contradiction:
        prompt += f"""

Importante: en el texto, menciona claramente que {contradiction['text_should_say']}. Debe parecer natural como parte del informe médico."""

    prompt += """
- Si es pertinente, menciona detalles adicionales que no aparecen en los datos estructurados (p. ej.: estado civil, alergias, detalles de anamnesis)"""

    return prompt

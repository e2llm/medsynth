"""es_MX free text generation config: prompts, styles, abbreviations, templates."""

SYSTEM_PROMPT = "Eres un médico mexicano que redacta notas clínicas. Escribe en español. No agregues explicaciones — solo la nota médica."

FACILITY_STYLES = {
    "nacional": "Estilo detallado e institucional. Notas extensas con estructura clara: antecedentes, evolución, resumen y recomendaciones al egreso.",
    "federal": "Estilo intermedio. Uso de abreviaturas médicas comunes (HAS, DM2, ICC). Formato semi-formal con datos clínicos relevantes.",
    "azteca": "Estilo muy breve. Solo comentarios cortos sobre resultados de laboratorio. 1-2 oraciones.",
    "centro_salud": "Estilo corto y directo. Registro clínico mínimo. Muchas abreviaturas. Sin formato uniforme.",
}

DOC_TYPE_CONTEXTS = {
    "discharge": "Nota de egreso hospitalario. Incluye: motivo de ingreso, evolución, tratamiento, indicaciones al alta.",
    "lab": "Observaciones a resultados de laboratorio. Muy breve — interpretación clínica de los resultados.",
    "visit": "Nota de consulta externa. Motivo de consulta, exploración física, impresión diagnóstica, plan.",
    "referral": "Hoja de referencia para valoración o tratamiento. Antecedentes, motivo de referencia, urgencia.",
}

MEDICAL_ABBREVIATIONS = "HAS (hipertensión), DM2 (diabetes), EPOC, IAM (infarto), ICC (insuficiencia cardíaca), FA (fibrilación auricular), ERC (enfermedad renal), TAC (tomografía)"

CONTRADICTION_TEMPLATES = {
    "smoking_yes": "fumador desde hace 20 años",
    "smoking_no": "no fumador, niega tabaquismo",
    "age": "paciente masculino/femenino de {age} años",
    "medication": "bajo tratamiento con {med}",
}

FALLBACK_STRINGS = {
    "no_conditions": "niega antecedentes patológicos",
    "no_medications": "sin medicamentos actuales",
    "no_diagnosis": "sin diagnóstico",
    "referral_default": "valoración",
}


def format_patient_context(patient: dict) -> str:
    """Format patient data for LLM prompt (Mexican Spanish)."""
    conditions_str = ", ".join(patient["conditions"]) if patient["conditions"] else "niega antecedentes patológicos"
    medications_str = ", ".join(patient["medications"]) if patient["medications"] else "sin medicamentos actuales"
    return (
        f"Datos del paciente:\n"
        f"- Nombre: {patient['full_name']}\n"
        f"- Edad: {patient['age']}\n"
        f"- Sexo: {'masculino' if patient['gender'] == 'male' else 'femenino'}\n"
        f"- Antecedentes: {conditions_str}\n"
        f"- Medicamentos: {medications_str}\n"
        f"- Tabaquismo: {'sí' if patient['smoking'] else 'no'}"
    )


def format_clinical_prompt(
    patient: dict,
    facility_id: str,
    doc_type: str,
    contradiction: dict | None = None,
) -> str:
    """Assemble the full clinical text generation prompt (Mexican Spanish)."""
    patient_context = format_patient_context(patient)

    prompt = f"""Escribe una nota clínica médica en español para un documento de tipo: {DOC_TYPE_CONTEXTS[doc_type]}

{patient_context}

Estilo del establecimiento: {FACILITY_STYLES[facility_id]}

Indicaciones:
- Escribe de 1 a 3 párrafos solamente
- Usa abreviaturas médicas comunes: {MEDICAL_ABBREVIATIONS}
- Incluye 1-2 errores ortográficos leves como los que comete un médico al escribir rápido
- No agregues títulos ni formato especial — solo texto corrido"""

    if contradiction:
        prompt += f"""

Importante: En el texto, menciona claramente que {contradiction['text_should_say']}. Debe verse natural como parte de la nota médica."""

    prompt += """
- Si es pertinente, menciona detalles adicionales que no aparezcan en los datos estructurados (por ejemplo: estado civil, alergias, datos de anamnesis)"""

    return prompt

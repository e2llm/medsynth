"""es_AR free text generation config: prompts, styles, abbreviations, templates."""

SYSTEM_PROMPT = "Sos un médico argentino que escribe informes clínicos. Escribí en español rioplatense. No agregues explicaciones — solo el informe médico."

FACILITY_STYLES = {
    "plata": "Estilo detallado y profesional. Informes extensos con estructura clara: antecedentes, evolución, resumen y recomendaciones al alta.",
    "san_martin": "Estilo medio. Uso de abreviaturas médicas habituales (HTA, DBT, FA). Estructura semi-formal con párrafos breves.",
    "austral": "Estilo muy conciso. Solo notas breves para resultados de laboratorio. 1-2 oraciones.",
    "caps": "Estilo corto y directo. Registro clínico mínimo. Muchas abreviaturas. Sin estructura uniforme.",
}

DOC_TYPE_CONTEXTS = {
    "discharge": "Epicrisis de internación. Incluye: motivo de internación, evolución, tratamientos, recomendaciones al alta.",
    "lab": "Notas sobre resultados de laboratorio. Muy breve — interpretación clínica de los resultados.",
    "visit": "Resumen de consulta ambulatoria. Motivo de consulta, examen físico, impresión diagnóstica, plan.",
    "referral": "Interconsulta o derivación para evaluación/tratamiento. Antecedentes, motivo de derivación, urgencia.",
}

MEDICAL_ABBREVIATIONS = "HTA (hipertensión), DBT (diabetes), EPOC, IAM (infarto), IC (insuficiencia cardíaca), FA (fibrilación auricular), IRC (insuficiencia renal), TC (tomografía)"

CONTRADICTION_TEMPLATES = {
    "smoking_yes": "fumador de 20 años",
    "smoking_no": "no fumador, niega tabaquismo",
    "age": "paciente de {age} años",
    "medication": "medicado con {med}",
}

FALLBACK_STRINGS = {
    "no_conditions": "sin antecedentes patológicos de relevancia",
    "no_medications": "sin medicación habitual",
    "no_diagnosis": "sin diagnóstico",
    "referral_default": "evaluación",
}


def format_patient_context(patient: dict) -> str:
    """Format patient data for LLM prompt (Argentine Spanish)."""
    conditions_str = ", ".join(patient["conditions"]) if patient["conditions"] else "sin antecedentes patológicos de relevancia"
    medications_str = ", ".join(patient["medications"]) if patient["medications"] else "sin medicación habitual"
    return (
        f"Datos del paciente:\n"
        f"- Nombre: {patient['full_name']}\n"
        f"- Edad: {patient['age']}\n"
        f"- Sexo: {'masculino' if patient['gender'] == 'male' else 'femenino'}\n"
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
    """Assemble the full clinical text generation prompt (Argentine Spanish)."""
    patient_context = format_patient_context(patient)

    prompt = f"""Escribí un texto clínico médico en español rioplatense para un documento de tipo: {DOC_TYPE_CONTEXTS[doc_type]}

{patient_context}

Estilo del centro: {FACILITY_STYLES[facility_id]}

Instrucciones:
- Escribí 1-3 párrafos únicamente
- Usá abreviaturas médicas habituales: {MEDICAL_ABBREVIATIONS}
- Agregá errores ortográficos leves (1-2) como un médico que escribe rápido
- No agregues títulos ni formato especial — solo texto corrido"""

    if contradiction:
        prompt += f"""

Importante: en el texto, mencioná claramente que {contradiction['text_should_say']}. Tiene que parecer natural como parte del informe médico."""

    prompt += """
- Si es pertinente, mencioná detalles adicionales que no aparecen en los datos estructurados (ej.: estado civil, alergias, detalles de anamnesis)"""

    return prompt

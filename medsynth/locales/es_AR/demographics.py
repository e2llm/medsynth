"""es_AR demographics: names, cities, streets, occupations."""

import random

MALE_FIRST_NAMES = [
    "Juan", "Martín", "Santiago", "Mateo", "Nicolás", "Agustín", "Tomás", "Lautaro",
    "Facundo", "Gonzalo", "Sebastián", "Federico", "Lucas", "Ignacio", "Joaquín", "Franco",
    "Maximiliano", "Rodrigo", "Ezequiel", "Patricio", "Diego", "Hernán", "Damián", "Leandro",
]

FEMALE_FIRST_NAMES = [
    "Sofía", "Valentina", "Camila", "Lucía", "Martina", "Agustina", "Florencia", "Milagros",
    "Rocío", "Celeste", "Julieta", "Carolina", "Micaela", "Candela", "Pilar", "Romina",
    "Victoria", "Belén", "Antonella", "Sol", "Aldana", "Macarena", "Josefina", "Abril",
]

PATERNAL_SURNAMES = [
    "González", "Rodríguez", "García", "Fernández", "López", "Martínez", "Pérez", "Gómez",
    "Sánchez", "Romero", "Díaz", "Torres", "Álvarez", "Ruiz", "Ramírez", "Flores",
    "Acosta", "Benítez", "Medina", "Herrera", "Suárez", "Aguirre", "Ríos", "Castro",
]

MATERNAL_SURNAMES = [
    "Morales", "Gutiérrez", "Rojas", "Cabrera", "Molina", "Ortiz", "Silva", "Pereyra",
    "Giménez", "Domínguez", "Figueroa", "Córdoba", "Lucero", "Ojeda", "Muñoz", "Paz",
    "Peralta", "Ferreyra", "Bustos", "Ledesma", "Godoy", "Villalba", "Sosa", "Quiroga",
]

CITIES = [
    "Buenos Aires", "Córdoba", "Rosario", "Mendoza", "Tucumán",
    "La Plata", "Mar del Plata", "Salta", "Santa Fe", "San Juan",
    "Resistencia", "Corrientes", "Posadas", "Neuquén", "Formosa",
    "San Luis", "Santiago del Estero", "Paraná", "Bahía Blanca", "Río Gallegos",
]

STREETS = [
    "Avenida 9 de Julio", "Avenida Corrientes", "Calle Florida", "Avenida Santa Fe",
    "Calle Rivadavia", "Avenida de Mayo", "Avenida Libertador", "Calle San Martín",
    "Calle Belgrano", "Avenida Independencia", "Calle Lavalle", "Avenida Callao",
    "Calle Sarmiento", "Avenida Córdoba",
]

OCCUPATIONS = [
    "ingeniero", "médico", "docente", "abogado", "enfermero",
    "colectivero", "albañil", "empleado público", "policía", "comerciante",
    "contador", "farmacéutico", "técnico", "programador", "militar",
    "jubilado", "estudiante", "periodista", "chef", "trabajador rural",
]


def generate_name(gender: str, rng: random.Random) -> dict:
    """Generate an Argentine name. Single surname is common; 30% chance of adding maternal surname."""
    first = rng.choice(MALE_FIRST_NAMES if gender == "male" else FEMALE_FIRST_NAMES)
    paternal = rng.choice(PATERNAL_SURNAMES)
    result = {
        "first_name": first,
        "last_name": paternal,
        "full_name": f"{first} {paternal}",
    }
    if rng.random() < 0.3:
        maternal = rng.choice(MATERNAL_SURNAMES)
        result["last_name"] = f"{paternal} {maternal}"
        result["full_name"] = f"{first} {paternal} {maternal}"
    return result


def emergency_contact_name(rng: random.Random) -> str:
    """Generate a random full name for emergency contact."""
    first = rng.choice(MALE_FIRST_NAMES + FEMALE_FIRST_NAMES)
    paternal = rng.choice(PATERNAL_SURNAMES)
    return f"{first} {paternal}"

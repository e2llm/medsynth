"""es_ES demographics: names, cities, streets, occupations."""

import random

MALE_FIRST_NAMES = [
    "Carlos", "Miguel", "José", "Antonio", "Francisco", "David", "Juan", "Manuel",
    "Pedro", "Javier", "Daniel", "Rafael", "Fernando", "Alejandro", "Pablo", "Sergio",
    "Andrés", "Marcos", "Álvaro", "Adrián", "Diego", "Raúl", "Óscar", "Jorge",
]

FEMALE_FIRST_NAMES = [
    "María", "Carmen", "Ana", "Isabel", "Laura", "Lucía", "Marta", "Elena",
    "Cristina", "Sara", "Paula", "Andrea", "Pilar", "Rosa", "Teresa", "Sofía",
    "Beatriz", "Raquel", "Inés", "Nuria", "Silvia", "Alba", "Eva", "Patricia",
]

PATERNAL_SURNAMES = [
    "García", "Rodríguez", "Martínez", "López", "González", "Hernández", "Pérez", "Sánchez",
    "Romero", "Torres", "Díaz", "Ruiz", "Moreno", "Jiménez", "Álvarez", "Muñoz",
    "Domínguez", "Vázquez", "Castro", "Ortega", "Ramos", "Marín", "Iglesias", "Navarro",
]

MATERNAL_SURNAMES = [
    "Fernández", "Gutiérrez", "Serrano", "Blanco", "Molina", "Morales", "Suárez", "Ortiz",
    "Delgado", "Rubio", "Medina", "Herrero", "Caballero", "Calvo", "León", "Prieto",
    "Reyes", "Fuentes", "Aguilar", "Gil", "Pascual", "Carrasco", "Guerrero", "Santos",
]

CITIES = [
    "Madrid", "Barcelona", "Valencia", "Sevilla", "Zaragoza",
    "Málaga", "Murcia", "Palma", "Bilbao", "Alicante",
    "Córdoba", "Valladolid", "Vigo", "Gijón", "Hospitalet de Llobregat",
    "Vitoria-Gasteiz", "Granada", "A Coruña", "Elche", "Oviedo",
]

STREETS = [
    "Calle Gran Vía", "Calle Mayor", "Paseo de la Castellana", "Avenida de la Constitución",
    "Calle Alcalá", "Rambla de Catalunya", "Calle Serrano", "Calle Princesa",
    "Avenida Diagonal", "Calle Arenal", "Paseo del Prado", "Calle Toledo",
    "Avenida de América", "Calle Velázquez",
]

OCCUPATIONS = [
    "ingeniero", "médico", "profesor", "abogado", "enfermero",
    "conductor", "albañil", "funcionario", "policía", "comerciante",
    "contable", "farmacéutico", "técnico", "programador", "militar",
    "jubilado", "estudiante", "periodista", "chef", "agricultor",
]


def generate_name(gender: str, rng: random.Random) -> dict:
    """Generate a Spanish name. Returns dict with first_name, paternal_surname, maternal_surname, last_name, full_name."""
    first = rng.choice(MALE_FIRST_NAMES if gender == "male" else FEMALE_FIRST_NAMES)
    paternal = rng.choice(PATERNAL_SURNAMES)
    maternal = rng.choice(MATERNAL_SURNAMES)
    return {
        "first_name": first,
        "paternal_surname": paternal,
        "maternal_surname": maternal,
        "last_name": paternal,
        "full_name": f"{first} {paternal} {maternal}",
    }


def emergency_contact_name(rng: random.Random) -> str:
    """Generate a random full name for emergency contact."""
    first = rng.choice(MALE_FIRST_NAMES + FEMALE_FIRST_NAMES)
    paternal = rng.choice(PATERNAL_SURNAMES)
    maternal = rng.choice(MATERNAL_SURNAMES)
    return f"{first} {paternal} {maternal}"

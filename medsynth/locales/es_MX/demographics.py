"""es_MX demographics: names, cities, streets, occupations, states."""

import random

MALE_FIRST_NAMES = [
    "José", "Juan", "Luis", "Carlos", "Miguel", "Francisco", "Alejandro", "Diego",
    "Eduardo", "Ricardo", "Fernando", "Jorge", "Jesús", "Rafael", "Manuel", "Arturo",
    "Héctor", "Sergio", "Roberto", "David", "Pedro", "Ángel", "Raúl", "Enrique",
]

FEMALE_FIRST_NAMES = [
    "María", "Guadalupe", "Ana", "Sofía", "Fernanda", "Valentina", "Daniela", "Mariana",
    "Camila", "Andrea", "Paola", "Gabriela", "Alejandra", "Verónica", "Patricia", "Claudia",
    "Sandra", "Adriana", "Leticia", "Rosa", "Laura", "Esperanza", "Juana", "Teresa",
]

PATERNAL_SURNAMES = [
    "García", "Hernández", "Martínez", "López", "González", "Rodríguez", "Pérez", "Sánchez",
    "Ramírez", "Torres", "Flores", "Rivera", "Gómez", "Díaz", "Cruz", "Morales",
    "Reyes", "Gutiérrez", "Ortiz", "Ramos", "Mendoza", "Aguilar", "Castillo", "Jiménez",
]

MATERNAL_SURNAMES = [
    "Vargas", "Chávez", "Romero", "Herrera", "Medina", "Domínguez", "Castro", "Guerrero",
    "Vázquez", "Ruiz", "Álvarez", "Mendoza", "Salazar", "Delgado", "Contreras", "Rojas",
    "Sandoval", "Cervantes", "Ríos", "Estrada", "Figueroa", "Acosta", "Silva", "Orozco",
]

CITIES = [
    "Ciudad de México", "Guadalajara", "Monterrey", "Puebla", "Tijuana",
    "León", "Juárez", "Zapopan", "Mérida", "San Luis Potosí",
    "Aguascalientes", "Hermosillo", "Saltillo", "Mexicali", "Culiacán",
    "Querétaro", "Chihuahua", "Morelia", "Cancún", "Toluca",
]

STATES = {
    "Aguascalientes": "AS",
    "Baja California": "BC",
    "Baja California Sur": "BS",
    "Campeche": "CC",
    "Chiapas": "CS",
    "Chihuahua": "CH",
    "Ciudad de México": "DF",
    "Coahuila": "CL",
    "Colima": "CM",
    "Durango": "DG",
    "Guanajuato": "GT",
    "Guerrero": "GR",
    "Hidalgo": "HG",
    "Jalisco": "JC",
    "México": "MC",
    "Michoacán": "MN",
    "Morelos": "MS",
    "Nayarit": "NT",
    "Nuevo León": "NL",
    "Oaxaca": "OC",
    "Puebla": "PL",
    "Querétaro": "QT",
    "Quintana Roo": "QR",
    "San Luis Potosí": "SP",
    "Sinaloa": "SL",
    "Sonora": "SR",
    "Tabasco": "TC",
    "Tamaulipas": "TS",
    "Tlaxcala": "TL",
    "Veracruz": "VZ",
    "Yucatán": "YN",
    "Zacatecas": "ZS",
}

CITY_TO_STATE = {
    "Ciudad de México": "DF",
    "Guadalajara": "JC",
    "Monterrey": "NL",
    "Puebla": "PL",
    "Tijuana": "BC",
    "León": "GT",
    "Juárez": "CH",
    "Zapopan": "JC",
    "Mérida": "YN",
    "San Luis Potosí": "SP",
    "Aguascalientes": "AS",
    "Hermosillo": "SR",
    "Saltillo": "CL",
    "Mexicali": "BC",
    "Culiacán": "SL",
    "Querétaro": "QT",
    "Chihuahua": "CH",
    "Morelia": "MN",
    "Cancún": "QR",
    "Toluca": "MC",
}

STREETS = [
    "Avenida Insurgentes", "Paseo de la Reforma", "Avenida Revolución",
    "Calle Madero", "Avenida Juárez", "Boulevard Miguel de Cervantes",
    "Calzada de Tlalpan", "Avenida Universidad", "Calle 5 de Mayo",
    "Avenida Hidalgo", "Calle Morelos", "Boulevard López Mateos",
    "Avenida Chapultepec", "Calle Independencia",
]

OCCUPATIONS = [
    "ingeniero", "médico", "maestro", "abogado", "enfermero",
    "chofer", "albañil", "empleado federal", "policía", "comerciante",
    "contador", "farmacéutico", "técnico", "programador", "militar",
    "jubilado", "estudiante", "periodista", "cocinero", "campesino",
]


def generate_name(gender: str, rng: random.Random) -> dict:
    """Generate a Mexican name. Returns dict with first_name, apellido_paterno, apellido_materno, last_name, full_name."""
    first = rng.choice(MALE_FIRST_NAMES if gender == "male" else FEMALE_FIRST_NAMES)
    paternal = rng.choice(PATERNAL_SURNAMES)
    maternal = rng.choice(MATERNAL_SURNAMES)
    return {
        "first_name": first,
        "apellido_paterno": paternal,
        "apellido_materno": maternal,
        "last_name": paternal,
        "full_name": f"{first} {paternal} {maternal}",
    }


def emergency_contact_name(rng: random.Random) -> str:
    """Generate a random full name for emergency contact."""
    first = rng.choice(MALE_FIRST_NAMES + FEMALE_FIRST_NAMES)
    paternal = rng.choice(PATERNAL_SURNAMES)
    maternal = rng.choice(MATERNAL_SURNAMES)
    return f"{first} {paternal} {maternal}"

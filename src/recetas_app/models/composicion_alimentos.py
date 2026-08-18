"""Tabla de composición nutricional de alimentos comunes (por 100 g).

Valores de referencia aproximados basados en bases de datos públicas de
composición de alimentos (USDA FoodData Central / BEDCA). Las claves están
normalizadas: minúsculas y sin acentos.
"""

TABLA_NUTRIENTES: dict[str, dict[str, float]] = {
    "harina": {"kcal": 364, "proteinas_g": 10.3, "grasas_g": 1.0, "carbohidratos_g": 76.3},
    "azucar": {"kcal": 387, "proteinas_g": 0.0, "grasas_g": 0.0, "carbohidratos_g": 100.0},
    "huevo": {"kcal": 155, "proteinas_g": 13.0, "grasas_g": 11.0, "carbohidratos_g": 1.1},
    "leche": {"kcal": 61, "proteinas_g": 3.2, "grasas_g": 3.3, "carbohidratos_g": 4.8},
    "mantequilla": {"kcal": 717, "proteinas_g": 0.9, "grasas_g": 81.0, "carbohidratos_g": 0.1},
    "aceite de oliva": {"kcal": 884, "proteinas_g": 0.0, "grasas_g": 100.0, "carbohidratos_g": 0.0},
    "aceite": {"kcal": 884, "proteinas_g": 0.0, "grasas_g": 100.0, "carbohidratos_g": 0.0},
    "arroz": {"kcal": 365, "proteinas_g": 7.1, "grasas_g": 0.7, "carbohidratos_g": 80.0},
    "pollo": {"kcal": 165, "proteinas_g": 31.0, "grasas_g": 3.6, "carbohidratos_g": 0.0},
    "carne de res": {"kcal": 250, "proteinas_g": 26.0, "grasas_g": 15.0, "carbohidratos_g": 0.0},
    "ternera": {"kcal": 172, "proteinas_g": 21.0, "grasas_g": 9.0, "carbohidratos_g": 0.0},
    "cerdo": {"kcal": 242, "proteinas_g": 27.0, "grasas_g": 14.0, "carbohidratos_g": 0.0},
    "pescado": {"kcal": 86, "proteinas_g": 17.8, "grasas_g": 1.0, "carbohidratos_g": 0.0},
    "atun": {"kcal": 116, "proteinas_g": 26.0, "grasas_g": 1.0, "carbohidratos_g": 0.0},
    "salmon": {"kcal": 208, "proteinas_g": 20.0, "grasas_g": 13.0, "carbohidratos_g": 0.0},
    "tomate": {"kcal": 18, "proteinas_g": 0.9, "grasas_g": 0.2, "carbohidratos_g": 3.9},
    "cebolla": {"kcal": 40, "proteinas_g": 1.1, "grasas_g": 0.1, "carbohidratos_g": 9.3},
    "ajo": {"kcal": 149, "proteinas_g": 6.4, "grasas_g": 0.5, "carbohidratos_g": 33.0},
    "patata": {"kcal": 77, "proteinas_g": 2.0, "grasas_g": 0.1, "carbohidratos_g": 17.0},
    "zanahoria": {"kcal": 41, "proteinas_g": 0.9, "grasas_g": 0.2, "carbohidratos_g": 10.0},
    "lechuga": {"kcal": 15, "proteinas_g": 1.4, "grasas_g": 0.2, "carbohidratos_g": 2.9},
    "pepino": {"kcal": 15, "proteinas_g": 0.7, "grasas_g": 0.1, "carbohidratos_g": 3.6},
    "pimiento": {"kcal": 31, "proteinas_g": 1.0, "grasas_g": 0.3, "carbohidratos_g": 6.0},
    "queso crema": {"kcal": 342, "proteinas_g": 5.9, "grasas_g": 34.0, "carbohidratos_g": 4.1},
    "queso parmesano": {"kcal": 392, "proteinas_g": 35.8, "grasas_g": 25.8, "carbohidratos_g": 4.1},
    "queso": {"kcal": 402, "proteinas_g": 25.0, "grasas_g": 33.0, "carbohidratos_g": 1.3},
    "pan": {"kcal": 265, "proteinas_g": 9.0, "grasas_g": 3.2, "carbohidratos_g": 49.0},
    "pasta": {"kcal": 371, "proteinas_g": 13.0, "grasas_g": 1.5, "carbohidratos_g": 75.0},
    "espagueti": {"kcal": 371, "proteinas_g": 13.0, "grasas_g": 1.5, "carbohidratos_g": 75.0},
    "sal": {"kcal": 0.0, "proteinas_g": 0.0, "grasas_g": 0.0, "carbohidratos_g": 0.0},
    "pimienta": {"kcal": 251, "proteinas_g": 10.0, "grasas_g": 3.3, "carbohidratos_g": 64.0},
    "manzana": {"kcal": 52, "proteinas_g": 0.3, "grasas_g": 0.2, "carbohidratos_g": 14.0},
    "platano": {"kcal": 89, "proteinas_g": 1.1, "grasas_g": 0.3, "carbohidratos_g": 23.0},
    "limon": {"kcal": 29, "proteinas_g": 1.1, "grasas_g": 0.3, "carbohidratos_g": 9.0},
    "chocolate": {"kcal": 546, "proteinas_g": 4.9, "grasas_g": 31.0, "carbohidratos_g": 61.0},
    "cacao": {"kcal": 228, "proteinas_g": 19.6, "grasas_g": 13.7, "carbohidratos_g": 57.9},
    "nata": {"kcal": 340, "proteinas_g": 2.1, "grasas_g": 36.0, "carbohidratos_g": 3.0},
    "yogur": {"kcal": 61, "proteinas_g": 3.5, "grasas_g": 3.3, "carbohidratos_g": 4.7},
    "garbanzos": {"kcal": 164, "proteinas_g": 8.9, "grasas_g": 2.6, "carbohidratos_g": 27.4},
    "lentejas": {"kcal": 116, "proteinas_g": 9.0, "grasas_g": 0.4, "carbohidratos_g": 20.0},
    "jamon": {"kcal": 145, "proteinas_g": 21.0, "grasas_g": 6.0, "carbohidratos_g": 1.5},
    "avena": {"kcal": 389, "proteinas_g": 16.9, "grasas_g": 6.9, "carbohidratos_g": 66.0},
    "miel": {"kcal": 304, "proteinas_g": 0.3, "grasas_g": 0.0, "carbohidratos_g": 82.0},
    "perejil": {"kcal": 36, "proteinas_g": 3.0, "grasas_g": 0.8, "carbohidratos_g": 6.3},
    "espinaca": {"kcal": 23, "proteinas_g": 2.9, "grasas_g": 0.4, "carbohidratos_g": 3.6},
    "brocoli": {"kcal": 34, "proteinas_g": 2.8, "grasas_g": 0.4, "carbohidratos_g": 6.6},
    "calabacin": {"kcal": 17, "proteinas_g": 1.2, "grasas_g": 0.3, "carbohidratos_g": 3.1},
    "berenjena": {"kcal": 25, "proteinas_g": 1.0, "grasas_g": 0.2, "carbohidratos_g": 6.0},
    "aguacate": {"kcal": 160, "proteinas_g": 2.0, "grasas_g": 14.7, "carbohidratos_g": 8.5},
    "almendras": {"kcal": 579, "proteinas_g": 21.0, "grasas_g": 50.0, "carbohidratos_g": 22.0},
    "nueces": {"kcal": 654, "proteinas_g": 15.0, "grasas_g": 65.0, "carbohidratos_g": 14.0},
}

# Peso aproximado en gramos de "1 unidad" para ingredientes que se suelen
# contar por piezas (p. ej. "3 huevos"). Claves normalizadas igual que arriba.
PESO_UNIDAD_G: dict[str, float] = {
    "huevo": 50,
    "manzana": 150,
    "platano": 120,
    "limon": 100,
    "tomate": 120,
    "cebolla": 110,
    "patata": 150,
    "zanahoria": 70,
    "pepino": 200,
    "pimiento": 120,
    "aguacate": 200,
}

# Conversión de unidades de medida habituales en recetas a gramos.
UNIDADES_A_GRAMOS: dict[str, float] = {
    "kilogramo": 1000, "kilogramos": 1000, "kilo": 1000, "kilos": 1000, "kg": 1000,
    "gramo": 1, "gramos": 1, "gr": 1, "g": 1,
    "litro": 1000, "litros": 1000, "l": 1000,
    "mililitro": 1, "mililitros": 1, "ml": 1,
    "cucharadita": 5, "cucharaditas": 5, "cdta": 5, "cdtas": 5,
    "cucharada": 15, "cucharadas": 15, "cda": 15, "cdas": 15,
    "taza": 240, "tazas": 240,
    "diente": 3, "dientes": 3,
    "loncha": 20, "lonchas": 20,
    "rodaja": 15, "rodajas": 15,
    "pizca": 0.5, "pizcas": 0.5,
}

# Unidades que expresan un conteo de piezas (usan PESO_UNIDAD_G en su lugar).
UNIDADES_CONTEO = {"unidad", "unidades", "pieza", "piezas"}

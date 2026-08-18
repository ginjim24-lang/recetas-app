from __future__ import annotations

import re
import unicodedata
from dataclasses import dataclass

from recetas_app.models.composicion_alimentos import (
    PESO_UNIDAD_G,
    TABLA_NUTRIENTES,
    UNIDADES_A_GRAMOS,
    UNIDADES_CONTEO,
)
from recetas_app.models.receta import Receta

_PESO_UNIDAD_DEFECTO_G = 100.0

_PATRON_INGREDIENTE = re.compile(
    r"""
    ^\s*
    (?P<cantidad>\d+(?:[.,]\d+)?(?:\s*/\s*\d+)?)?
    \s*
    (?P<unidad>
        kilogramos?|kilos?|kg|
        gramos?|gr|g|
        litros?|l|
        mililitros?|ml|
        cucharaditas?|cdtas?|
        cucharadas?|cdas?|
        tazas?|
        dientes?|
        lonchas?|
        rodajas?|
        pizcas?|
        unidades?|piezas?
    )?
    \s*
    (?:de\s+)?
    (?P<alimento>.+?)
    \s*$
    """,
    re.IGNORECASE | re.VERBOSE,
)


@dataclass
class ResumenNutricional:
    kcal_total: float
    proteinas_g_total: float
    grasas_g_total: float
    carbohidratos_g_total: float
    kcal_por_porcion: float
    proteinas_g_por_porcion: float
    grasas_g_por_porcion: float
    carbohidratos_g_por_porcion: float
    ingredientes_no_reconocidos: list[str]


def _quitar_acentos(texto: str) -> str:
    normalizado = unicodedata.normalize("NFKD", texto)
    return "".join(caracter for caracter in normalizado if not unicodedata.combining(caracter))


def _normalizar(texto: str) -> str:
    return _quitar_acentos(texto).lower().strip()


def _parsear_cantidad(texto: str) -> float:
    texto = texto.strip().replace(",", ".")
    if "/" in texto:
        numerador, denominador = texto.split("/")
        return float(numerador) / float(denominador)
    return float(texto)


def parsear_ingrediente(texto: str) -> tuple[float | None, str | None, str]:
    """Extrae (cantidad, unidad, alimento) de una línea de ingrediente libre."""
    coincidencia = _PATRON_INGREDIENTE.match(texto)
    if not coincidencia:
        return None, None, _normalizar(texto)

    cantidad_texto = coincidencia.group("cantidad")
    unidad_texto = coincidencia.group("unidad")
    alimento = _normalizar(coincidencia.group("alimento"))

    cantidad = _parsear_cantidad(cantidad_texto) if cantidad_texto else None
    unidad = _normalizar(unidad_texto) if unidad_texto else None

    return cantidad, unidad, alimento


def _buscar_alimento(nombre: str) -> tuple[str, dict[str, float]] | None:
    if nombre in TABLA_NUTRIENTES:
        return nombre, TABLA_NUTRIENTES[nombre]

    candidatos = [
        clave
        for clave in TABLA_NUTRIENTES
        if re.search(rf"\b{re.escape(clave)}s?\b", nombre)
    ]
    if not candidatos:
        return None

    mejor = max(candidatos, key=len)
    return mejor, TABLA_NUTRIENTES[mejor]


def _gramos_equivalentes(cantidad: float | None, unidad: str | None, alimento_clave: str) -> float:
    cantidad = cantidad if cantidad is not None else 1.0

    if unidad is None or unidad in UNIDADES_CONTEO:
        peso_unidad = PESO_UNIDAD_G.get(alimento_clave, _PESO_UNIDAD_DEFECTO_G)
        return cantidad * peso_unidad

    return cantidad * UNIDADES_A_GRAMOS.get(unidad, _PESO_UNIDAD_DEFECTO_G)


def calcular_nutricion_receta(receta: Receta) -> ResumenNutricional:
    kcal = proteinas = grasas = carbohidratos = 0.0
    no_reconocidos: list[str] = []

    for texto_ingrediente in receta.ingredientes:
        cantidad, unidad, alimento_texto = parsear_ingrediente(texto_ingrediente)
        encontrado = _buscar_alimento(alimento_texto)
        if encontrado is None:
            no_reconocidos.append(texto_ingrediente)
            continue

        clave, nutrientes_100g = encontrado
        gramos = _gramos_equivalentes(cantidad, unidad, clave)
        factor = gramos / 100.0

        kcal += nutrientes_100g["kcal"] * factor
        proteinas += nutrientes_100g["proteinas_g"] * factor
        grasas += nutrientes_100g["grasas_g"] * factor
        carbohidratos += nutrientes_100g["carbohidratos_g"] * factor

    porciones = receta.porciones or 1

    return ResumenNutricional(
        kcal_total=round(kcal, 1),
        proteinas_g_total=round(proteinas, 1),
        grasas_g_total=round(grasas, 1),
        carbohidratos_g_total=round(carbohidratos, 1),
        kcal_por_porcion=round(kcal / porciones, 1),
        proteinas_g_por_porcion=round(proteinas / porciones, 1),
        grasas_g_por_porcion=round(grasas / porciones, 1),
        carbohidratos_g_por_porcion=round(carbohidratos / porciones, 1),
        ingredientes_no_reconocidos=no_reconocidos,
    )

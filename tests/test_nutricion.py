import pytest

from recetas_app.models.nutricion import calcular_nutricion_receta, parsear_ingrediente
from recetas_app.models.receta import Receta


def _receta(**overrides) -> Receta:
    datos = dict(
        nombre="Receta de prueba",
        categoria="Entrada",
        ingredientes=["200 g harina"],
        pasos=["Mezclar"],
        tiempo_preparacion_min=10,
        porciones=2,
    )
    datos.update(overrides)
    return Receta(**datos)


@pytest.mark.parametrize(
    "texto,cantidad,unidad,alimento",
    [
        ("200 g harina", 200.0, "g", "harina"),
        ("3 huevos", 3.0, None, "huevos"),
        ("Sal", None, None, "sal"),
        ("1 taza de leche", 1.0, "taza", "leche"),
        ("1/2 taza de azúcar", 0.5, "taza", "azucar"),
        ("2 dientes de ajo", 2.0, "dientes", "ajo"),
        ("100 ml aceite de oliva", 100.0, "ml", "aceite de oliva"),
        ("1,5 kg patatas", 1.5, "kg", "patatas"),
    ],
)
def test_parsear_ingrediente(texto, cantidad, unidad, alimento):
    resultado = parsear_ingrediente(texto)
    assert resultado == (cantidad, unidad, alimento)


def test_calcular_nutricion_totales_gramos():
    receta = _receta(ingredientes=["200 g harina"], porciones=1)
    resumen = calcular_nutricion_receta(receta)

    # harina: 364 kcal / 100 g -> 200 g = 728 kcal
    assert resumen.kcal_total == pytest.approx(728.0)
    assert resumen.proteinas_g_total == pytest.approx(20.6)
    assert resumen.ingredientes_no_reconocidos == []


def test_calcular_nutricion_con_unidad_contable():
    receta = _receta(ingredientes=["2 huevos"], porciones=1)
    resumen = calcular_nutricion_receta(receta)

    # huevo: 155 kcal/100g, peso unidad 50g -> 2 huevos = 100g -> 155 kcal
    assert resumen.kcal_total == pytest.approx(155.0)


def test_calcular_nutricion_sin_cantidad_usa_una_unidad():
    receta = _receta(ingredientes=["Tomate"], porciones=1)
    resumen = calcular_nutricion_receta(receta)

    # tomate: 18 kcal/100g, peso unidad 120g -> 1.2 * 18 = 21.6 kcal
    assert resumen.kcal_total == pytest.approx(21.6)


def test_calcular_nutricion_divide_por_porciones():
    receta = _receta(ingredientes=["200 g harina"], porciones=4)
    resumen = calcular_nutricion_receta(receta)

    assert resumen.kcal_total == pytest.approx(728.0)
    assert resumen.kcal_por_porcion == pytest.approx(182.0)


def test_calcular_nutricion_ingrediente_no_reconocido():
    receta = _receta(ingredientes=["200 g harina", "3 unicornios mágicos"], porciones=1)
    resumen = calcular_nutricion_receta(receta)

    assert resumen.ingredientes_no_reconocidos == ["3 unicornios mágicos"]
    # solo cuenta la harina
    assert resumen.kcal_total == pytest.approx(728.0)


def test_calcular_nutricion_combina_varios_ingredientes():
    receta = _receta(
        ingredientes=["100 g azúcar", "100 g harina"],
        porciones=1,
    )
    resumen = calcular_nutricion_receta(receta)

    assert resumen.kcal_total == pytest.approx(387.0 + 364.0)
    assert resumen.carbohidratos_g_total == pytest.approx(100.0 + 76.3)

from recetas_app.models.lista_compra import generar_lista_compra
from recetas_app.models.receta import Receta


def _receta(**overrides) -> Receta:
    datos = dict(
        nombre="Receta",
        categoria="Entrada",
        ingredientes=["1 kg Tomate", "2 Cebolla"],
        pasos=["Cocinar"],
        tiempo_preparacion_min=10,
        porciones=2,
    )
    datos.update(overrides)
    return Receta(**datos)


def test_lista_compra_vacia_sin_recetas():
    assert generar_lista_compra([]) == []


def test_lista_compra_combina_ingredientes_de_varias_recetas():
    receta1 = _receta(ingredientes=["Tomate", "Cebolla"])
    receta2 = _receta(ingredientes=["Pollo", "Sal"])

    resultado = generar_lista_compra([receta1, receta2])

    assert resultado == ["Cebolla", "Pollo", "Sal", "Tomate"]


def test_lista_compra_deduplica_ingredientes_repetidos_sin_distinguir_mayusculas():
    receta1 = _receta(ingredientes=["Tomate", "Sal"])
    receta2 = _receta(ingredientes=["tomate", "Pimienta"])

    resultado = generar_lista_compra([receta1, receta2])

    assert resultado == ["Pimienta", "Sal", "Tomate"]

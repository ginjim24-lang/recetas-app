import pytest

from recetas_app.models.receta import Receta, RecetaInvalidaError


def _receta_valida(**overrides) -> Receta:
    datos = dict(
        nombre="Tortilla de patatas",
        categoria="Plato principal",
        ingredientes=["4 huevos", "3 patatas", "1 cebolla"],
        pasos=["Pelar y freír las patatas", "Batir los huevos", "Cuajar la tortilla"],
        tiempo_preparacion_min=30,
        porciones=4,
    )
    datos.update(overrides)
    return Receta(**datos)


def test_receta_valida_no_lanza_error():
    receta = _receta_valida()
    receta.validate()


def test_receta_sin_nombre_es_invalida():
    receta = _receta_valida(nombre="")
    with pytest.raises(RecetaInvalidaError):
        receta.validate()


def test_receta_sin_ingredientes_es_invalida():
    receta = _receta_valida(ingredientes=[])
    with pytest.raises(RecetaInvalidaError):
        receta.validate()


def test_receta_sin_pasos_es_invalida():
    receta = _receta_valida(pasos=[])
    with pytest.raises(RecetaInvalidaError):
        receta.validate()


def test_tiempo_preparacion_no_positivo_es_invalido():
    receta = _receta_valida(tiempo_preparacion_min=0)
    with pytest.raises(RecetaInvalidaError):
        receta.validate()


def test_porciones_no_positivas_es_invalido():
    receta = _receta_valida(porciones=-1)
    with pytest.raises(RecetaInvalidaError):
        receta.validate()


def test_to_dict_y_from_dict_son_simetricos():
    receta = _receta_valida()
    reconstruida = Receta.from_dict(receta.to_dict())
    assert reconstruida == receta

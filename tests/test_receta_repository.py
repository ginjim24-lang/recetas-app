import pytest

from recetas_app.models.receta import Receta, RecetaInvalidaError
from recetas_app.models.receta_repository import RecetaNoEncontradaError, RecetaRepository


def _receta(**overrides) -> Receta:
    datos = dict(
        nombre="Ensalada César",
        categoria="Entrada",
        ingredientes=["Lechuga", "Pollo", "Queso parmesano"],
        pasos=["Cortar la lechuga", "Mezclar todos los ingredientes"],
        tiempo_preparacion_min=15,
        porciones=2,
    )
    datos.update(overrides)
    return Receta(**datos)


@pytest.fixture
def repo(tmp_path) -> RecetaRepository:
    return RecetaRepository(tmp_path / "recetas.json")


def test_archivo_se_crea_vacio_si_no_existe(tmp_path):
    ruta = tmp_path / "sub" / "recetas.json"
    repo = RecetaRepository(ruta)
    assert ruta.exists()
    assert repo.listar() == []


def test_crear_y_listar(repo):
    receta = repo.crear(_receta())
    assert repo.listar() == [receta]


def test_crear_receta_invalida_lanza_error(repo):
    with pytest.raises(RecetaInvalidaError):
        repo.crear(_receta(nombre=""))


def test_obtener_por_id(repo):
    receta = repo.crear(_receta())
    encontrada = repo.obtener(receta.id)
    assert encontrada == receta


def test_obtener_id_inexistente_lanza_error(repo):
    with pytest.raises(RecetaNoEncontradaError):
        repo.obtener("id-inexistente")


def test_actualizar_receta(repo):
    receta = repo.crear(_receta())
    actualizada = _receta(nombre="Ensalada César especial")
    resultado = repo.actualizar(receta.id, actualizada)
    assert resultado.id == receta.id
    assert resultado.fecha_creacion == receta.fecha_creacion
    assert repo.obtener(receta.id).nombre == "Ensalada César especial"


def test_actualizar_id_inexistente_lanza_error(repo):
    with pytest.raises(RecetaNoEncontradaError):
        repo.actualizar("id-inexistente", _receta())


def test_eliminar_receta(repo):
    receta = repo.crear(_receta())
    repo.eliminar(receta.id)
    assert repo.listar() == []


def test_eliminar_id_inexistente_lanza_error(repo):
    with pytest.raises(RecetaNoEncontradaError):
        repo.eliminar("id-inexistente")


def test_buscar_por_nombre(repo):
    repo.crear(_receta(nombre="Ensalada César"))
    repo.crear(_receta(nombre="Sopa de tomate"))
    resultados = repo.buscar_por_nombre("ensalada")
    assert len(resultados) == 1
    assert resultados[0].nombre == "Ensalada César"


def test_buscar_por_ingrediente(repo):
    repo.crear(_receta(ingredientes=["Lechuga", "Pollo"]))
    repo.crear(_receta(ingredientes=["Tomate", "Cebolla"]))
    resultados = repo.buscar_por_ingrediente("pollo")
    assert len(resultados) == 1


def test_buscar_por_categoria(repo):
    repo.crear(_receta(categoria="Entrada"))
    repo.crear(_receta(categoria="Postre"))
    resultados = repo.buscar_por_categoria("postre")
    assert len(resultados) == 1


def test_listar_favoritas(repo):
    favorita = repo.crear(_receta(nombre="Ensalada César", favorita=True))
    repo.crear(_receta(nombre="Sopa de tomate"))
    resultados = repo.listar_favoritas()
    assert resultados == [favorita]


def test_marcar_favorita(repo):
    receta = repo.crear(_receta())
    assert receta.favorita is False

    actualizada = repo.marcar_favorita(receta.id, True)
    assert actualizada.favorita is True
    assert repo.obtener(receta.id).favorita is True

    repo.marcar_favorita(receta.id, False)
    assert repo.obtener(receta.id).favorita is False


def test_marcar_favorita_id_inexistente_lanza_error(repo):
    with pytest.raises(RecetaNoEncontradaError):
        repo.marcar_favorita("id-inexistente", True)

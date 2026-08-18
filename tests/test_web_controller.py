import pytest

from recetas_app.models.receta import Receta
from recetas_app.models.receta_repository import RecetaRepository
from recetas_app.web import create_app


@pytest.fixture
def cliente(tmp_path):
    repo = RecetaRepository(tmp_path / "recetas.json")
    app = create_app(repository=repo)
    app.testing = True
    return app.test_client(), repo


def test_listar_recetas_vacio(cliente):
    client, _ = cliente
    resp = client.get("/recetas")
    assert resp.status_code == 200
    assert "No hay recetas" in resp.get_data(as_text=True)


def test_index_muestra_landing_page(cliente):
    client, _ = cliente
    resp = client.get("/")
    assert resp.status_code == 200
    cuerpo = resp.get_data(as_text=True)
    assert "Recipe Collection" in cuerpo
    assert 'href="/recetas"' in cuerpo


def test_pagina_crear_muestra_categorias(cliente):
    client, _ = cliente
    resp = client.get("/recetas/nueva")
    assert resp.status_code == 200
    cuerpo = resp.get_data(as_text=True)
    for categoria in Receta.CATEGORIAS:
        assert categoria in cuerpo


def test_crear_receta_valida_redirige_y_persiste(cliente):
    client, repo = cliente
    resp = client.post(
        "/recetas/nueva",
        data={
            "nombre": "Gazpacho",
            "categoria": "Entrada",
            "ingredientes": "Tomate\nPepino",
            "pasos": "Trocear\nTriturar",
            "tiempo_preparacion_min": "20",
            "porciones": "4",
        },
    )
    assert resp.status_code == 302
    recetas = repo.listar()
    assert len(recetas) == 1
    assert recetas[0].nombre == "Gazpacho"
    assert recetas[0].ingredientes == ["Tomate", "Pepino"]


def test_crear_receta_invalida_muestra_error_y_no_persiste(cliente):
    client, repo = cliente
    resp = client.post(
        "/recetas/nueva",
        data={
            "nombre": "",
            "categoria": "Entrada",
            "ingredientes": "",
            "pasos": "",
            "tiempo_preparacion_min": "0",
            "porciones": "0",
        },
    )
    assert resp.status_code == 400
    assert repo.listar() == []


def test_marcar_favorita_y_verla_en_favoritas(cliente):
    client, repo = cliente
    receta = repo.crear(
        Receta(
            nombre="Sopa",
            categoria="Entrada",
            ingredientes=["Agua"],
            pasos=["Cocer"],
            tiempo_preparacion_min=10,
            porciones=2,
        )
    )

    resp = client.post(f"/recetas/{receta.id}/favorita")
    assert resp.status_code == 302
    assert repo.obtener(receta.id).favorita is True

    resp = client.get("/favoritas")
    assert "Sopa" in resp.get_data(as_text=True)


def test_desmarcar_favorita(cliente):
    client, repo = cliente
    receta = repo.crear(
        Receta(
            nombre="Sopa",
            categoria="Entrada",
            ingredientes=["Agua"],
            pasos=["Cocer"],
            tiempo_preparacion_min=10,
            porciones=2,
            favorita=True,
        )
    )

    client.post(f"/recetas/{receta.id}/favorita")
    assert repo.obtener(receta.id).favorita is False


def test_marcar_favorita_id_inexistente_no_falla(cliente):
    client, _ = cliente
    resp = client.post("/recetas/id-inexistente/favorita")
    assert resp.status_code == 302


def test_ver_receta_muestra_detalle_y_nutricion(cliente):
    client, repo = cliente
    receta = repo.crear(
        Receta(
            nombre="Tostada de aguacate",
            categoria="Entrada",
            ingredientes=["1 pan", "1 aguacate"],
            pasos=["Tostar el pan", "Aplastar el aguacate"],
            tiempo_preparacion_min=5,
            porciones=1,
        )
    )

    resp = client.get(f"/recetas/{receta.id}")
    assert resp.status_code == 200
    cuerpo = resp.get_data(as_text=True)
    assert "Tostada de aguacate" in cuerpo
    assert "Información nutricional" in cuerpo
    assert "kcal" in cuerpo


def test_ver_receta_inexistente_devuelve_404(cliente):
    client, _ = cliente
    resp = client.get("/recetas/id-inexistente")
    assert resp.status_code == 404
    assert "no encontrada" in resp.get_data(as_text=True).lower()


def test_listado_enlaza_a_detalle_de_receta(cliente):
    client, repo = cliente
    receta = repo.crear(
        Receta(
            nombre="Sopa",
            categoria="Entrada",
            ingredientes=["Agua"],
            pasos=["Cocer"],
            tiempo_preparacion_min=10,
            porciones=2,
        )
    )

    resp = client.get("/recetas")
    assert f'href="/recetas/{receta.id}"' in resp.get_data(as_text=True)

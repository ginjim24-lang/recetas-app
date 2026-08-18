from recetas_app.controllers.receta_controller import RecetaController
from recetas_app.models.receta_repository import RecetaRepository


class MenuViewStub:
    def __init__(self, opciones, ids=None, textos=None, busquedas=None):
        self._opciones = list(opciones)
        self._ids = list(ids or [])
        self._textos = list(textos or [])
        self._busquedas = list(busquedas or [])

    def mostrar_menu_principal(self):
        return self._opciones.pop(0)

    def mostrar_menu_busqueda(self):
        return self._busquedas.pop(0)

    def leer_texto(self, etiqueta):
        return self._textos.pop(0)

    def leer_id(self):
        return self._ids.pop(0)


class RecetaViewStub:
    def __init__(self, datos_formulario=None, confirmaciones=None):
        self._datos_formulario = list(datos_formulario or [])
        self._confirmaciones = list(confirmaciones or [])
        self.mensajes = []
        self.errores = []
        self.listados = []
        self.detalles = []

    def mostrar_listado(self, recetas):
        self.listados.append(recetas)

    def mostrar_detalle(self, receta):
        self.detalles.append(receta)

    def pedir_lista(self, etiqueta):
        campo = "ingredientes" if "ingrediente" in etiqueta.lower() else "pasos"
        return self._datos_formulario[0][campo]

    def pedir_entero(self, etiqueta):
        campo = "tiempo" if "tiempo" in etiqueta.lower() else "porciones"
        return self._datos_formulario[0][campo]

    def pedir_texto(self, etiqueta):
        campo = "nombre" if "nombre" in etiqueta.lower() else "categoria"
        return self._datos_formulario[0][campo]

    def confirmar(self, mensaje):
        return self._confirmaciones.pop(0)

    def mostrar_mensaje(self, texto):
        self.mensajes.append(texto)

    def mostrar_error(self, texto):
        self.errores.append(texto)


FORMULARIO_VALIDO = {
    "nombre": "Gazpacho",
    "categoria": "Entrada",
    "ingredientes": ["Tomate", "Pepino", "Pimiento"],
    "pasos": ["Trocear las verduras", "Triturar todo"],
    "tiempo": 20,
    "porciones": 4,
}


def _controller(tmp_path, menu_view, receta_view):
    repo = RecetaRepository(tmp_path / "recetas.json")
    return RecetaController(repo, menu_view, receta_view), repo


def test_crear_receta_flujo_completo(tmp_path):
    menu_view = MenuViewStub(opciones=["3", "7"])
    receta_view = RecetaViewStub(datos_formulario=[FORMULARIO_VALIDO])
    controller, repo = _controller(tmp_path, menu_view, receta_view)

    controller.ejecutar()

    recetas = repo.listar()
    assert len(recetas) == 1
    assert recetas[0].nombre == "Gazpacho"
    assert any("creada" in m.lower() for m in receta_view.mensajes)


def test_listar_recetas_vacio(tmp_path):
    menu_view = MenuViewStub(opciones=["1", "7"])
    receta_view = RecetaViewStub()
    controller, _ = _controller(tmp_path, menu_view, receta_view)

    controller.ejecutar()

    assert receta_view.listados == [[]]


def test_eliminar_receta_con_confirmacion(tmp_path):
    repo = RecetaRepository(tmp_path / "recetas.json")
    from recetas_app.models.receta import Receta

    receta = repo.crear(
        Receta(
            nombre="Sopa",
            categoria="Entrada",
            ingredientes=["Agua", "Verduras"],
            pasos=["Cocer"],
            tiempo_preparacion_min=10,
            porciones=2,
        )
    )

    menu_view = MenuViewStub(opciones=["5", "7"], ids=[receta.id])
    receta_view = RecetaViewStub(confirmaciones=[True])
    controller = RecetaController(repo, menu_view, receta_view)

    controller.ejecutar()

    assert repo.listar() == []
    assert any("eliminada" in m.lower() for m in receta_view.mensajes)


def test_ver_receta_inexistente_muestra_error(tmp_path):
    menu_view = MenuViewStub(opciones=["2", "7"], ids=["id-inexistente"])
    receta_view = RecetaViewStub()
    controller, _ = _controller(tmp_path, menu_view, receta_view)

    controller.ejecutar()

    assert any("no existe" in e.lower() for e in receta_view.errores)

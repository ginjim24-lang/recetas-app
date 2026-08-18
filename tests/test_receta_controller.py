from recetas_app.controllers.receta_controller import RecetaController
from recetas_app.models.receta import Receta
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
    def __init__(self, datos_formulario=None, confirmaciones=None, ids_lista_compra=None):
        self._datos_formulario = list(datos_formulario or [])
        self._confirmaciones = list(confirmaciones or [])
        self._ids_lista_compra = list(ids_lista_compra or [])
        self.mensajes = []
        self.errores = []
        self.listados = []
        self.detalles = []
        self.listas_compra = []

    def mostrar_listado(self, recetas):
        self.listados.append(recetas)

    def mostrar_detalle(self, receta):
        self.detalles.append(receta)

    def mostrar_lista_compra(self, recetas, ingredientes):
        self.listas_compra.append((recetas, ingredientes))

    def pedir_lista(self, etiqueta):
        if "recetas para la lista de la compra" in etiqueta.lower():
            return self._ids_lista_compra
        campo = "ingredientes" if "ingrediente" in etiqueta.lower() else "pasos"
        return self._datos_formulario[0][campo]

    def pedir_entero(self, etiqueta):
        campo = "tiempo" if "tiempo" in etiqueta.lower() else "porciones"
        return self._datos_formulario[0][campo]

    def pedir_texto(self, etiqueta):
        return self._datos_formulario[0]["nombre"]

    def pedir_categoria(self, categorias):
        return self._datos_formulario[0]["categoria"]

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
    menu_view = MenuViewStub(opciones=["4", "10"])
    receta_view = RecetaViewStub(datos_formulario=[FORMULARIO_VALIDO])
    controller, repo = _controller(tmp_path, menu_view, receta_view)

    controller.ejecutar()

    recetas = repo.listar()
    assert len(recetas) == 1
    assert recetas[0].nombre == "Gazpacho"
    assert recetas[0].categoria == "Entrada"
    assert recetas[0].favorita is False
    assert any("creada" in m.lower() for m in receta_view.mensajes)


def test_listar_recetas_vacio(tmp_path):
    menu_view = MenuViewStub(opciones=["1", "10"])
    receta_view = RecetaViewStub()
    controller, _ = _controller(tmp_path, menu_view, receta_view)

    controller.ejecutar()

    assert receta_view.listados == [[]]


def test_eliminar_receta_con_confirmacion(tmp_path):
    repo = RecetaRepository(tmp_path / "recetas.json")

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

    menu_view = MenuViewStub(opciones=["6", "10"], ids=[receta.id])
    receta_view = RecetaViewStub(confirmaciones=[True])
    controller = RecetaController(repo, menu_view, receta_view)

    controller.ejecutar()

    assert repo.listar() == []
    assert any("eliminada" in m.lower() for m in receta_view.mensajes)


def test_ver_receta_inexistente_muestra_error(tmp_path):
    menu_view = MenuViewStub(opciones=["3", "10"], ids=["id-inexistente"])
    receta_view = RecetaViewStub()
    controller, _ = _controller(tmp_path, menu_view, receta_view)

    controller.ejecutar()

    assert any("no existe" in e.lower() for e in receta_view.errores)


def test_marcar_y_desmarcar_favorita(tmp_path):
    repo = RecetaRepository(tmp_path / "recetas.json")
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

    menu_view = MenuViewStub(opciones=["7", "7", "10"], ids=[receta.id, receta.id])
    receta_view = RecetaViewStub()
    controller = RecetaController(repo, menu_view, receta_view)

    controller.ejecutar()

    assert repo.obtener(receta.id).favorita is False
    assert any("marcada" in m.lower() for m in receta_view.mensajes)
    assert any("desmarcada" in m.lower() for m in receta_view.mensajes)


def test_listar_favoritas_solo_muestra_marcadas(tmp_path):
    repo = RecetaRepository(tmp_path / "recetas.json")
    favorita = repo.crear(
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
    repo.crear(
        Receta(
            nombre="Ensalada",
            categoria="Entrada",
            ingredientes=["Lechuga"],
            pasos=["Mezclar"],
            tiempo_preparacion_min=5,
            porciones=1,
        )
    )

    menu_view = MenuViewStub(opciones=["2", "10"])
    receta_view = RecetaViewStub()
    controller = RecetaController(repo, menu_view, receta_view)

    controller.ejecutar()

    assert receta_view.listados == [[favorita]]


def test_editar_receta_conserva_estado_favorita(tmp_path):
    repo = RecetaRepository(tmp_path / "recetas.json")
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

    menu_view = MenuViewStub(opciones=["5", "10"], ids=[receta.id])
    receta_view = RecetaViewStub(datos_formulario=[FORMULARIO_VALIDO])
    controller = RecetaController(repo, menu_view, receta_view)

    controller.ejecutar()

    assert repo.obtener(receta.id).favorita is True


def test_generar_lista_compra_con_recetas_validas(tmp_path):
    repo = RecetaRepository(tmp_path / "recetas.json")
    receta1 = repo.crear(
        Receta(
            nombre="Sopa",
            categoria="Entrada",
            ingredientes=["Agua", "Sal"],
            pasos=["Cocer"],
            tiempo_preparacion_min=10,
            porciones=2,
        )
    )
    receta2 = repo.crear(
        Receta(
            nombre="Ensalada",
            categoria="Entrada",
            ingredientes=["Lechuga", "sal"],
            pasos=["Mezclar"],
            tiempo_preparacion_min=5,
            porciones=1,
        )
    )

    menu_view = MenuViewStub(opciones=["9", "10"])
    receta_view = RecetaViewStub(ids_lista_compra=[receta1.id, receta2.id])
    controller = RecetaController(repo, menu_view, receta_view)

    controller.ejecutar()

    assert len(receta_view.listas_compra) == 1
    recetas_incluidas, ingredientes = receta_view.listas_compra[0]
    assert {r.id for r in recetas_incluidas} == {receta1.id, receta2.id}
    assert ingredientes == ["Agua", "Lechuga", "Sal"]


def test_generar_lista_compra_sin_ids_muestra_error(tmp_path):
    menu_view = MenuViewStub(opciones=["9", "10"])
    receta_view = RecetaViewStub(ids_lista_compra=[])
    controller, _ = _controller(tmp_path, menu_view, receta_view)

    controller.ejecutar()

    assert any("al menos un id" in e.lower() for e in receta_view.errores)


def test_generar_lista_compra_con_id_inexistente_avisa_pero_continua(tmp_path):
    repo = RecetaRepository(tmp_path / "recetas.json")
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

    menu_view = MenuViewStub(opciones=["9", "10"])
    receta_view = RecetaViewStub(ids_lista_compra=[receta.id, "id-inexistente"])
    controller = RecetaController(repo, menu_view, receta_view)

    controller.ejecutar()

    assert any("no existe" in e.lower() for e in receta_view.errores)
    assert len(receta_view.listas_compra) == 1

from recetas_app.models.receta import Receta, RecetaInvalidaError
from recetas_app.models.receta_repository import RecetaNoEncontradaError, RecetaRepository
from recetas_app.views.menu_view import MenuView
from recetas_app.views.receta_view import RecetaView


class RecetaController:
    def __init__(
        self,
        repository: RecetaRepository,
        menu_view: MenuView,
        receta_view: RecetaView,
    ):
        self._repo = repository
        self._menu_view = menu_view
        self._receta_view = receta_view

    def ejecutar(self) -> None:
        acciones = {
            "1": self._listar,
            "2": self._listar_favoritas,
            "3": self._ver,
            "4": self._crear,
            "5": self._editar,
            "6": self._eliminar,
            "7": self._marcar_favorita,
            "8": self._buscar,
        }
        while True:
            opcion = self._menu_view.mostrar_menu_principal()
            if opcion == "9":
                self._receta_view.mostrar_mensaje("¡Hasta luego!")
                break
            accion = acciones.get(opcion)
            if accion is None:
                self._receta_view.mostrar_error("Opción no válida.")
                continue
            accion()

    def _listar(self) -> None:
        recetas = self._repo.listar()
        self._receta_view.mostrar_listado(recetas)

    def _listar_favoritas(self) -> None:
        recetas = self._repo.listar_favoritas()
        self._receta_view.mostrar_listado(recetas)

    def _ver(self) -> None:
        receta_id = self._menu_view.leer_id()
        try:
            receta = self._repo.obtener(receta_id)
        except RecetaNoEncontradaError:
            self._receta_view.mostrar_error("No existe una receta con ese id.")
            return
        self._receta_view.mostrar_detalle(receta)

    def _pedir_datos_receta(self) -> Receta:
        nombre = self._receta_view.pedir_texto("Nombre")
        categoria = self._receta_view.pedir_categoria(Receta.CATEGORIAS)
        ingredientes = self._receta_view.pedir_lista("Ingredientes")
        pasos = self._receta_view.pedir_lista("Pasos")
        tiempo = self._receta_view.pedir_entero("Tiempo de preparación (min)")
        porciones = self._receta_view.pedir_entero("Porciones")
        return Receta(
            nombre=nombre,
            categoria=categoria,
            ingredientes=ingredientes,
            pasos=pasos,
            tiempo_preparacion_min=tiempo,
            porciones=porciones,
        )

    def _crear(self) -> None:
        receta = self._pedir_datos_receta()
        try:
            self._repo.crear(receta)
        except RecetaInvalidaError as error:
            self._receta_view.mostrar_error(str(error))
            return
        self._receta_view.mostrar_mensaje(f"Receta creada con id {receta.id}.")

    def _editar(self) -> None:
        receta_id = self._menu_view.leer_id()
        try:
            receta_existente = self._repo.obtener(receta_id)
        except RecetaNoEncontradaError:
            self._receta_view.mostrar_error("No existe una receta con ese id.")
            return

        self._receta_view.mostrar_mensaje("Introduce los nuevos datos de la receta:")
        receta_actualizada = self._pedir_datos_receta()
        receta_actualizada.favorita = receta_existente.favorita
        try:
            self._repo.actualizar(receta_id, receta_actualizada)
        except RecetaInvalidaError as error:
            self._receta_view.mostrar_error(str(error))
            return
        self._receta_view.mostrar_mensaje("Receta actualizada correctamente.")

    def _eliminar(self) -> None:
        receta_id = self._menu_view.leer_id()
        try:
            receta = self._repo.obtener(receta_id)
        except RecetaNoEncontradaError:
            self._receta_view.mostrar_error("No existe una receta con ese id.")
            return

        if not self._receta_view.confirmar(f"¿Eliminar la receta '{receta.nombre}'?"):
            self._receta_view.mostrar_mensaje("Operación cancelada.")
            return

        self._repo.eliminar(receta_id)
        self._receta_view.mostrar_mensaje("Receta eliminada correctamente.")

    def _marcar_favorita(self) -> None:
        receta_id = self._menu_view.leer_id()
        try:
            receta = self._repo.obtener(receta_id)
        except RecetaNoEncontradaError:
            self._receta_view.mostrar_error("No existe una receta con ese id.")
            return

        nuevo_valor = not receta.favorita
        self._repo.marcar_favorita(receta_id, nuevo_valor)
        if nuevo_valor:
            self._receta_view.mostrar_mensaje(f"'{receta.nombre}' marcada como favorita.")
        else:
            self._receta_view.mostrar_mensaje(f"'{receta.nombre}' desmarcada como favorita.")

    def _buscar(self) -> None:
        criterio = self._menu_view.mostrar_menu_busqueda()
        if criterio == "1":
            texto = self._menu_view.leer_texto("Nombre a buscar")
            resultados = self._repo.buscar_por_nombre(texto)
        elif criterio == "2":
            texto = self._menu_view.leer_texto("Ingrediente a buscar")
            resultados = self._repo.buscar_por_ingrediente(texto)
        elif criterio == "3":
            texto = self._menu_view.leer_texto("Categoría a buscar")
            resultados = self._repo.buscar_por_categoria(texto)
        else:
            self._receta_view.mostrar_error("Criterio de búsqueda no válido.")
            return
        self._receta_view.mostrar_listado(resultados)

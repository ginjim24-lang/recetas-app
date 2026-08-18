from pathlib import Path

from recetas_app.controllers.receta_controller import RecetaController
from recetas_app.models.receta_repository import RecetaRepository
from recetas_app.views.menu_view import MenuView
from recetas_app.views.receta_view import RecetaView

RUTA_DATOS = Path(__file__).resolve().parent.parent.parent / "data" / "recetas.json"


def main() -> None:
    repository = RecetaRepository(RUTA_DATOS)
    controller = RecetaController(repository, MenuView(), RecetaView())
    controller.ejecutar()


if __name__ == "__main__":
    main()

import os
from pathlib import Path

from flask import Flask

from recetas_app.controllers.web_controller import crear_blueprint
from recetas_app.models.receta_repository import RecetaRepository
from recetas_app.paths import RUTA_DATOS

BASE_DIR = Path(__file__).resolve().parent


def create_app(repository: RecetaRepository | None = None) -> Flask:
    app = Flask(
        __name__,
        template_folder=str(BASE_DIR / "views" / "templates"),
        static_folder=str(BASE_DIR / "views" / "static"),
    )
    app.register_blueprint(crear_blueprint(repository or RecetaRepository(RUTA_DATOS)))
    return app


def main() -> None:
    app = create_app()
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True, use_reloader=False)


if __name__ == "__main__":
    main()

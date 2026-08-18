from flask import Blueprint, redirect, render_template, request, url_for

from recetas_app.models.receta import Receta, RecetaInvalidaError
from recetas_app.models.receta_repository import RecetaNoEncontradaError, RecetaRepository


def crear_blueprint(repository: RecetaRepository) -> Blueprint:
    bp = Blueprint("recetas", __name__)

    @bp.route("/")
    def index():
        return render_template("landing.html")

    @bp.route("/recetas")
    def listar():
        return render_template("recetas_listar.html", recetas=repository.listar())

    @bp.route("/favoritas")
    def favoritas():
        return render_template("favoritas.html", recetas=repository.listar_favoritas())

    @bp.route("/recetas/nueva", methods=["GET", "POST"])
    def crear():
        if request.method == "GET":
            return render_template(
                "recetas_crear.html", categorias=Receta.CATEGORIAS, error=None, valores={}
            )

        receta = Receta(
            nombre=request.form.get("nombre", "").strip(),
            categoria=request.form.get("categoria", ""),
            ingredientes=_lineas(request.form.get("ingredientes", "")),
            pasos=_lineas(request.form.get("pasos", "")),
            tiempo_preparacion_min=_entero(request.form.get("tiempo_preparacion_min")),
            porciones=_entero(request.form.get("porciones")),
        )
        try:
            repository.crear(receta)
        except RecetaInvalidaError as error:
            return (
                render_template(
                    "recetas_crear.html",
                    categorias=Receta.CATEGORIAS,
                    error=str(error),
                    valores=request.form,
                ),
                400,
            )
        return redirect(url_for("recetas.listar"))

    @bp.route("/recetas/<receta_id>/favorita", methods=["POST"])
    def marcar_favorita(receta_id):
        try:
            receta = repository.obtener(receta_id)
        except RecetaNoEncontradaError:
            return redirect(request.referrer or url_for("recetas.listar"))
        repository.marcar_favorita(receta_id, not receta.favorita)
        return redirect(request.referrer or url_for("recetas.listar"))

    return bp


def _lineas(texto: str) -> list[str]:
    return [linea.strip() for linea in texto.splitlines() if linea.strip()]


def _entero(valor: str | None) -> int:
    try:
        return int(valor)
    except (TypeError, ValueError):
        return 0

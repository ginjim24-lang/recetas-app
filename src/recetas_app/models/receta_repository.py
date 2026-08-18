from __future__ import annotations

import json
from pathlib import Path

from recetas_app.models.receta import Receta


class RecetaNoEncontradaError(KeyError):
    """Se lanza cuando no existe una receta con el id solicitado."""


class RecetaRepository:
    def __init__(self, ruta_json: Path | str):
        self._ruta = Path(ruta_json)
        self._asegurar_archivo()

    def _asegurar_archivo(self) -> None:
        if not self._ruta.exists():
            self._ruta.parent.mkdir(parents=True, exist_ok=True)
            self._ruta.write_text("[]", encoding="utf-8")

    def _cargar(self) -> list[Receta]:
        contenido = self._ruta.read_text(encoding="utf-8").strip()
        if not contenido:
            return []
        datos = json.loads(contenido)
        return [Receta.from_dict(item) for item in datos]

    def _guardar(self, recetas: list[Receta]) -> None:
        datos = [receta.to_dict() for receta in recetas]
        self._ruta.write_text(
            json.dumps(datos, ensure_ascii=False, indent=2), encoding="utf-8"
        )

    def listar(self) -> list[Receta]:
        return self._cargar()

    def obtener(self, receta_id: str) -> Receta:
        for receta in self._cargar():
            if receta.id == receta_id:
                return receta
        raise RecetaNoEncontradaError(receta_id)

    def crear(self, receta: Receta) -> Receta:
        receta.validate()
        recetas = self._cargar()
        recetas.append(receta)
        self._guardar(recetas)
        return receta

    def actualizar(self, receta_id: str, receta_actualizada: Receta) -> Receta:
        receta_actualizada.validate()
        recetas = self._cargar()
        for indice, receta in enumerate(recetas):
            if receta.id == receta_id:
                receta_actualizada.id = receta_id
                receta_actualizada.fecha_creacion = receta.fecha_creacion
                recetas[indice] = receta_actualizada
                self._guardar(recetas)
                return receta_actualizada
        raise RecetaNoEncontradaError(receta_id)

    def eliminar(self, receta_id: str) -> None:
        recetas = self._cargar()
        recetas_restantes = [r for r in recetas if r.id != receta_id]
        if len(recetas_restantes) == len(recetas):
            raise RecetaNoEncontradaError(receta_id)
        self._guardar(recetas_restantes)

    def buscar_por_nombre(self, texto: str) -> list[Receta]:
        texto = texto.lower()
        return [r for r in self._cargar() if texto in r.nombre.lower()]

    def buscar_por_ingrediente(self, texto: str) -> list[Receta]:
        texto = texto.lower()
        return [
            r
            for r in self._cargar()
            if any(texto in ingrediente.lower() for ingrediente in r.ingredientes)
        ]

    def buscar_por_categoria(self, texto: str) -> list[Receta]:
        texto = texto.lower()
        return [r for r in self._cargar() if texto in r.categoria.lower()]

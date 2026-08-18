from __future__ import annotations

import uuid
from dataclasses import dataclass, field
from datetime import datetime, timezone


class RecetaInvalidaError(ValueError):
    """Se lanza cuando los datos de una receta no cumplen las reglas de validación."""


@dataclass
class Receta:
    CATEGORIAS = [
        "Entrada",
        "Plato principal",
        "Postre",
        "Bebida",
        "Snack",
        "Vegano",
        "Vegetariano",
    ]

    nombre: str
    categoria: str
    ingredientes: list[str]
    pasos: list[str]
    tiempo_preparacion_min: int
    porciones: int
    favorita: bool = False
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    fecha_creacion: str = field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat()
    )

    def validate(self) -> None:
        errores = []

        if not self.nombre or not self.nombre.strip():
            errores.append("El nombre es obligatorio.")
        if self.categoria not in self.CATEGORIAS:
            errores.append(
                f"La categoría debe ser una de: {', '.join(self.CATEGORIAS)}."
            )
        if not self.ingredientes:
            errores.append("Debe indicar al menos un ingrediente.")
        if not self.pasos:
            errores.append("Debe indicar al menos un paso de preparación.")
        if not isinstance(self.tiempo_preparacion_min, int) or self.tiempo_preparacion_min <= 0:
            errores.append("El tiempo de preparación debe ser un entero positivo.")
        if not isinstance(self.porciones, int) or self.porciones <= 0:
            errores.append("Las porciones deben ser un entero positivo.")

        if errores:
            raise RecetaInvalidaError(" ".join(errores))

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "nombre": self.nombre,
            "categoria": self.categoria,
            "ingredientes": self.ingredientes,
            "pasos": self.pasos,
            "tiempo_preparacion_min": self.tiempo_preparacion_min,
            "porciones": self.porciones,
            "favorita": self.favorita,
            "fecha_creacion": self.fecha_creacion,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Receta":
        return cls(
            id=data["id"],
            nombre=data["nombre"],
            categoria=data["categoria"],
            ingredientes=list(data["ingredientes"]),
            pasos=list(data["pasos"]),
            tiempo_preparacion_min=data["tiempo_preparacion_min"],
            porciones=data["porciones"],
            favorita=data.get("favorita", False),
            fecha_creacion=data["fecha_creacion"],
        )

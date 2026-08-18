from recetas_app.models.receta import Receta


def generar_lista_compra(recetas: list[Receta]) -> list[str]:
    ingredientes_vistos: dict[str, str] = {}
    for receta in recetas:
        for ingrediente in receta.ingredientes:
            clave = ingrediente.strip().lower()
            if clave not in ingredientes_vistos:
                ingredientes_vistos[clave] = ingrediente.strip()
    return sorted(ingredientes_vistos.values(), key=str.lower)

# recetas-app

Aplicación de línea de comandos para gestionar recetas de cocina, construida con
arquitectura **MVC** (Modelo, Vista, Controlador) en carpetas separadas y gestionada
con [uv](https://docs.astral.sh/uv/).

## Estructura del proyecto

```
recetas-app/
├── data/
│   └── recetas.json            # almacenamiento persistente (generado automáticamente)
├── src/recetas_app/
│   ├── main.py                 # punto de entrada
│   ├── models/                 # entidad Receta + persistencia (RecetaRepository)
│   ├── views/                  # entrada/salida por consola (menús, formularios)
│   └── controllers/            # orquestación entre vistas y modelo
└── tests/                      # tests unitarios (pytest)
```

## Instalación

Requiere [uv](https://docs.astral.sh/uv/getting-started/installation/) instalado.

```bash
uv sync
```

## Uso

```bash
uv run recetas-app
```

Muestra un menú interactivo para listar, ver, crear, editar, eliminar y buscar recetas,
además de marcar/desmarcar recetas como favoritas, listar solo las favoritas y generar
una lista de la compra combinando los ingredientes de varias recetas (indicando sus
ids). La categoría de cada receta se elige de una lista predefinida (`Receta.CATEGORIAS`).
Las recetas se guardan en `data/recetas.json`.

## Tests

```bash
uv run pytest
```

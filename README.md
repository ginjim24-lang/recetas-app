# recetas-app

Aplicación de recetas de cocina construida con arquitectura **MVC** (Modelo, Vista,
Controlador) en carpetas separadas y gestionada con [uv](https://docs.astral.sh/uv/).
Tiene dos interfaces que comparten el mismo Modelo: una **CLI** interactiva y una
**app web** (Flask) con un diseño visual tipo SaaS.

## Estructura del proyecto

```
recetas-app/
├── data/
│   └── recetas.json                # almacenamiento persistente (generado automáticamente)
├── src/recetas_app/
│   ├── main.py                     # punto de entrada de la CLI
│   ├── web.py                      # fábrica de la app Flask (punto de entrada web)
│   ├── paths.py                    # ruta compartida a data/recetas.json
│   ├── models/                     # entidad Receta, persistencia, lista de la compra y nutrición
│   ├── views/
│   │   ├── menu_view.py            # vista de consola (menús)
│   │   ├── receta_view.py          # vista de consola (formularios, listados)
│   │   ├── templates/              # vistas web (Jinja2): landing, listado, crear, favoritas
│   │   └── static/style.css        # estilos de la app web
│   └── controllers/
│       ├── receta_controller.py    # controlador de la CLI
│       └── web_controller.py       # controlador web (Blueprint de Flask)
└── tests/                          # tests unitarios (pytest)
```

## Instalación

Requiere [uv](https://docs.astral.sh/uv/getting-started/installation/) instalado.

```bash
uv sync
```

## Uso — CLI

```bash
uv run recetas-app
```

Menú interactivo para listar, ver, crear, editar, eliminar y buscar recetas, marcar/
desmarcar favoritas, listar solo las favoritas y generar una lista de la compra
combinando los ingredientes de varias recetas. Al ver una receta se muestra también
su información nutricional estimada.

## Uso — app web

```bash
uv run recetas-app-web
```

Levanta un servidor Flask en `http://0.0.0.0:5000` (puerto configurable con la
variable de entorno `PORT`). Páginas disponibles:

- `/` — landing page con hero, categorías destacadas y llamadas a la acción.
- `/recetas` — listado de todas las recetas.
- `/recetas/<id>` — detalle de una receta, con su información nutricional estimada.
- `/recetas/nueva` — formulario para crear una receta.
- `/favoritas` — listado de recetas marcadas como favoritas.

La categoría de cada receta se elige de una lista predefinida (`Receta.CATEGORIAS`).
Ambas interfaces leen y escriben el mismo `data/recetas.json`.

### Información nutricional

Cada receta muestra una estimación de kcal, proteínas, grasas y carbohidratos
(totales y por porción), calculada a partir de sus ingredientes:

1. Cada línea de ingrediente (p. ej. `"200 g harina"`, `"3 huevos"`) se interpreta
   para extraer cantidad, unidad y alimento (`models/nutricion.py`).
2. El alimento se busca en una tabla local de composición nutricional por cada
   100 g, con valores de referencia de bases de datos públicas tipo USDA/BEDCA
   (`models/composicion_alimentos.py`).
3. Las cantidades se convierten a gramos (unidades de medida habituales, o un
   peso aproximado por unidad para ingredientes que se cuentan por piezas).

Es una **estimación aproximada**: los ingredientes que no se reconocen en la
tabla se muestran aparte y no se contabilizan.

## Tests

```bash
uv run pytest
```

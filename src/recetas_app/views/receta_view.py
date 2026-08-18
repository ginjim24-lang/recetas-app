from recetas_app.models.receta import Receta


class RecetaView:
    def mostrar_listado(self, recetas: list[Receta]) -> None:
        if not recetas:
            print("No hay recetas guardadas.")
            return
        print(f"\n{'':<2}{'ID':<36} {'Nombre':<25} {'Categoría':<15} Tiempo (min)")
        print("-" * 92)
        for receta in recetas:
            marca = "★ " if receta.favorita else "  "
            print(
                f"{marca}{receta.id:<36} {receta.nombre:<25} "
                f"{receta.categoria:<15} {receta.tiempo_preparacion_min}"
            )

    def mostrar_detalle(self, receta: Receta) -> None:
        print(f"\n=== {receta.nombre} {'★' if receta.favorita else ''} ===")
        print(f"Id: {receta.id}")
        print(f"Categoría: {receta.categoria}")
        print(f"Favorita: {'Sí' if receta.favorita else 'No'}")
        print(f"Tiempo de preparación: {receta.tiempo_preparacion_min} min")
        print(f"Porciones: {receta.porciones}")
        print(f"Creada: {receta.fecha_creacion}")
        print("\nIngredientes:")
        for ingrediente in receta.ingredientes:
            print(f"  - {ingrediente}")
        print("\nPasos:")
        for indice, paso in enumerate(receta.pasos, start=1):
            print(f"  {indice}. {paso}")

    def mostrar_lista_compra(self, recetas: list[Receta], ingredientes: list[str]) -> None:
        print("\n=== Lista de la compra ===")
        print("Recetas incluidas:")
        for receta in recetas:
            print(f"  - {receta.nombre}")
        print("\nIngredientes necesarios:")
        for ingrediente in ingredientes:
            print(f"  [ ] {ingrediente}")

    def pedir_lista(self, etiqueta: str) -> list[str]:
        print(f"{etiqueta} (una por línea, línea vacía para terminar):")
        items = []
        while True:
            valor = input("  - ").strip()
            if not valor:
                break
            items.append(valor)
        return items

    def pedir_entero(self, etiqueta: str) -> int:
        while True:
            valor = input(f"{etiqueta}: ").strip()
            try:
                return int(valor)
            except ValueError:
                print("Debe introducir un número entero. Inténtalo de nuevo.")

    def pedir_texto(self, etiqueta: str) -> str:
        return input(f"{etiqueta}: ").strip()

    def pedir_categoria(self, categorias: list[str]) -> str:
        print("Categorías disponibles:")
        for indice, categoria in enumerate(categorias, start=1):
            print(f"  {indice}) {categoria}")
        while True:
            valor = input("Elige una categoría (número): ").strip()
            if valor.isdigit() and 1 <= int(valor) <= len(categorias):
                return categorias[int(valor) - 1]
            print("Opción no válida. Inténtalo de nuevo.")

    def confirmar(self, mensaje: str) -> bool:
        respuesta = input(f"{mensaje} (s/n): ").strip().lower()
        return respuesta == "s"

    def mostrar_mensaje(self, texto: str) -> None:
        print(texto)

    def mostrar_error(self, texto: str) -> None:
        print(f"Error: {texto}")

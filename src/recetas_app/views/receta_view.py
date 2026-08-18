from recetas_app.models.receta import Receta


class RecetaView:
    def mostrar_listado(self, recetas: list[Receta]) -> None:
        if not recetas:
            print("No hay recetas guardadas.")
            return
        print(f"\n{'ID':<36} {'Nombre':<25} {'Categoría':<15} Tiempo (min)")
        print("-" * 90)
        for receta in recetas:
            print(
                f"{receta.id:<36} {receta.nombre:<25} "
                f"{receta.categoria:<15} {receta.tiempo_preparacion_min}"
            )

    def mostrar_detalle(self, receta: Receta) -> None:
        print(f"\n=== {receta.nombre} ===")
        print(f"Id: {receta.id}")
        print(f"Categoría: {receta.categoria}")
        print(f"Tiempo de preparación: {receta.tiempo_preparacion_min} min")
        print(f"Porciones: {receta.porciones}")
        print(f"Creada: {receta.fecha_creacion}")
        print("\nIngredientes:")
        for ingrediente in receta.ingredientes:
            print(f"  - {ingrediente}")
        print("\nPasos:")
        for indice, paso in enumerate(receta.pasos, start=1):
            print(f"  {indice}. {paso}")

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

    def confirmar(self, mensaje: str) -> bool:
        respuesta = input(f"{mensaje} (s/n): ").strip().lower()
        return respuesta == "s"

    def mostrar_mensaje(self, texto: str) -> None:
        print(texto)

    def mostrar_error(self, texto: str) -> None:
        print(f"Error: {texto}")

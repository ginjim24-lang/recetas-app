class MenuView:
    OPCIONES_PRINCIPAL = {
        "1": "Listar recetas",
        "2": "Ver receta",
        "3": "Crear receta",
        "4": "Editar receta",
        "5": "Eliminar receta",
        "6": "Buscar recetas",
        "7": "Salir",
    }

    OPCIONES_BUSQUEDA = {
        "1": "Por nombre",
        "2": "Por ingrediente",
        "3": "Por categoría",
    }

    def mostrar_menu_principal(self) -> str:
        print("\n=== App de Recetas ===")
        for clave, texto in self.OPCIONES_PRINCIPAL.items():
            print(f"{clave}) {texto}")
        return input("Elige una opción: ").strip()

    def mostrar_menu_busqueda(self) -> str:
        print("\n--- Buscar recetas ---")
        for clave, texto in self.OPCIONES_BUSQUEDA.items():
            print(f"{clave}) {texto}")
        return input("Elige un criterio: ").strip()

    def leer_texto(self, etiqueta: str) -> str:
        return input(f"{etiqueta}: ").strip()

    def leer_id(self) -> str:
        return input("Id de la receta: ").strip()

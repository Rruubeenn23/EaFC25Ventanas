import customtkinter as ctk

def center_window(window, width, height):
    # Obtener el tamaño de la pantalla
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()

    # Calcular las coordenadas (x, y) para centrar la ventana
    x = (screen_width // 2) - (width // 2)
    y = (screen_height // 2) - (height // 2)

    # Establecer el tamaño de la ventana y su ubicación
    window.geometry(f'{width}x{height}+{x}+{y}')


class VerPlantillaApp(ctk.CTk):
    def __init__(self, jugadores_seleccionados, main_app):
        super().__init__()
        self.jugadores_seleccionados = jugadores_seleccionados  # Recibir la plantilla creada
        self.main_app = main_app  # Referencia a la ventana principal
        self.title("Ver Plantilla")
        self.geometry("800x600")
        
        center_window(self, 800, 600)

        # Crear interfaz gráfica
        self.frame = ctk.CTkFrame(self)
        self.frame.pack(pady=20, padx=20, fill="both", expand=True)

        self.label_title = ctk.CTkLabel(self.frame, text="Plantilla Actual", font=("Arial", 24))
        self.label_title.pack(pady=10)

        # Mostrar la plantilla
        # Si 'jugadores_seleccionados' es una lista, no utilizamos `.items()`
        for i, jugador in enumerate(self.jugadores_seleccionados):
            ctk.CTkLabel(self.frame, text=f"{i + 1}: {jugador}", font=("Arial", 14)).pack(pady=5)

        # Botón de volver al menú
        self.button_volver = ctk.CTkButton(self.frame, text="Volver al Menú", command=self.volver_menu)
        self.button_volver.pack(pady=20)

    def volver_menu(self):
        """Cerrar la ventana actual y volver a la ventana principal."""
        self.main_app.deiconify()  # Mostrar la ventana principal
        self.destroy()  # Cerrar la ventana actual


if __name__ == "__main__":
    # Simulando una lista de jugadores seleccionados
    jugadores_seleccionados = ["Jugador A", "Jugador B", "Jugador C"]

    # Simulamos la ventana principal
    class MainApp(ctk.CTk):
        def __init__(self):
            super().__init__()
            self.title("Menú Principal")
            self.geometry("600x400")
            self.withdraw()  # Ocultamos la ventana principal al inicio

    main_app = MainApp()

    # Crear la ventana para ver la plantilla, pasando la ventana principal como referencia
    app = VerPlantillaApp(jugadores_seleccionados, main_app)
    app.mainloop()

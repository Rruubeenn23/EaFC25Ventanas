import customtkinter as ctk
import pandas as pd
from formaciones import Formacion, Equipo, crear_formaciones

def center_window(window, width, height):
    # Obtener el tamaño de la pantalla
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()

    # Calcular las coordenadas (x, y) para centrar la ventana
    x = (screen_width // 2) - (width // 2)
    y = (screen_height // 2) - (height // 2)

    # Establecer el tamaño de la ventana y su ubicación
    window.geometry(f'{width}x{height}+{x}+{y}')
    

class CrearPlantillaApp(ctk.CTk):
    def __init__(self, csv_path, main_app):
        super().__init__()
        self.main_app = main_app  # Referencia a la ventana principal
        self.title("Seleccionar Jugadores")
        self.geometry("800x600")
        center_window(self, 800, 600)

        # Cargar datos y configurar atributos
        self.jugadores_df = pd.read_csv(csv_path)
        self.equipo = Equipo("Mi Equipo")
        self.formacion_actual = None
        self.jugadores_seleccionados = []  # Usamos una lista para almacenar los jugadores seleccionados

        # Lista de posiciones en el orden correcto, ahora con repeticiones numeradas
        self.posiciones = [
            "GK", "LD", "DEF 1", "DEF 2", "LI", "MID 1", "MID 2", "MID 3", "EI", "FWD", "ED"
        ]
        self.posicion_actual_idx = 0  # Índice de la posición actual

        # Crear la interfaz
        self.frame = ctk.CTkFrame(self)
        self.frame.pack(pady=20, padx=20, fill="both", expand=True)

        self.label_title = ctk.CTkLabel(self.frame, text="Gestión de Jugadores", font=("Arial", 24))
        self.label_title.pack(pady=10)

        self.label_formacion = ctk.CTkLabel(self.frame, text="Formación: Ninguna", font=("Arial", 16))
        self.label_formacion.pack(pady=10)

        self.button_elegir_formacion = ctk.CTkButton(self.frame, text="Elegir Formación", command=self.elegir_formacion)
        self.button_elegir_formacion.pack(pady=10)

        self.posicion_var = ctk.StringVar(value=self.posiciones[self.posicion_actual_idx])
        self.dropdown_posicion = ctk.CTkOptionMenu(self.frame, variable=self.posicion_var, values=self.posiciones)
        self.dropdown_posicion.pack(pady=10)

        self.button_mostrar_jugadores = ctk.CTkButton(self.frame, text="Mostrar Jugadores", command=self.mostrar_jugadores_por_posicion)
        self.button_mostrar_jugadores.pack(pady=10)

        self.jugadores_frame = ctk.CTkFrame(self.frame)
        self.jugadores_frame.pack(pady=10, fill="both", expand=True)

        self.label_status = ctk.CTkLabel(self.frame, text="", font=("Arial", 14))
        self.label_status.pack(pady=10)

    def elegir_formacion(self):
        formaciones_creadas = crear_formaciones()
        for formacion in formaciones_creadas:
            self.equipo.agregar_formacion(formacion)

        self.formacion_actual = formaciones_creadas[0]
        self.label_formacion.configure(text=f"Formación: {self.formacion_actual.nombre} ({self.formacion_actual.formacion})")

    def mostrar_jugadores_por_posicion(self):
        posicion = self.posiciones[self.posicion_actual_idx]
        posicion_filtrada = self.obtener_posicion_filtrada(posicion)

        jugadores = self.jugadores_df[(
            self.jugadores_df['Position'] == posicion_filtrada) &
            (~self.jugadores_df['Name'].isin(self.jugadores_seleccionados))
        ].sort_values(by='OVR', ascending=False)

        for widget in self.jugadores_frame.winfo_children():
            widget.destroy()

        if jugadores.empty:
            ctk.CTkLabel(self.jugadores_frame, text=f"No hay jugadores disponibles en la posición {posicion}.").pack()
            return

        for idx, jugador in jugadores.iterrows():
            jugador_text = f"{jugador['Name']} - OVR: {jugador['OVR']} - Equipo: {jugador['Team']}"
            button = ctk.CTkButton(self.jugadores_frame, text=jugador_text,
                                   command=lambda j=jugador: self.seleccionar_jugador(posicion, j))
            button.pack(pady=5)

    def seleccionar_jugador(self, posicion, jugador):
        if posicion not in self.jugadores_seleccionados:
            self.jugadores_seleccionados.append(jugador['Name'])

        # Validar que el jugador seleccionado tiene datos completos
        if jugador['OVR'] is None or pd.isna(jugador['OVR']):
            self.label_status.configure(text=f"Error: El jugador {jugador['Name']} no tiene una media válida.")
            return

        self.label_status.configure(text=f"Seleccionado: {jugador['Name']} para la posición {posicion}.")
        self.posicion_actual_idx += 1  # Avanzar al siguiente índice de posición

        if self.posicion_actual_idx >= len(self.posiciones):
            # Cuando se completa la selección, pasamos los jugadores seleccionados a la ventana principal
            self.main_app.jugadores_seleccionados = self.jugadores_seleccionados
            self.label_status.configure(text="¡Selección completa!")
            self.regresar_al_menu()  # Regresar al menú principal
        else:
            self.posicion_var.set(self.posiciones[self.posicion_actual_idx])  # Actualizar la posición seleccionada
            self.mostrar_jugadores_por_posicion()

    def obtener_posicion_filtrada(self, posicion):
        """Ajusta las posiciones para que coincidan con los valores del CSV de jugadores."""
        # Aquí asignamos las posiciones a los valores en el CSV
        return {
            "GK": "GK", "DEF 1": "CB", "DEF 2": "CB", "LI": "LB", "LD": "RB",
            "MID 1": "CM", "MID 2": "CM", "MID 3": "CM", "FWD": "ST", "EI": "LW", "ED": "RW"
        }.get(posicion, None)

    def regresar_al_menu(self):
        self.main_app.deiconify()  # Volver a mostrar la ventana principal
        self.destroy()  # Cerrar la ventana de selección de jugadores


if __name__ == "__main__":
    class MainApp(ctk.CTk):
        def __init__(self):
            super().__init__()
            self.title("Ventana Principal")
            self.geometry("800x600")

    main_app = MainApp()
    main_app.withdraw()  # Ocultar la ventana principal
    app = CrearPlantillaApp("ruta/a/tu/csv.csv", main_app)  # Cambiar ruta del archivo CSV
    app.mainloop() 

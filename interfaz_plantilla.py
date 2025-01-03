import customtkinter as ctk
import tkinter as tk
from tkinter import ttk  # Importar ttk para Notebook
import pandas as pd
from formaciones import Formacion, Equipo, crear_formaciones


class SeleccionarJugadoresApp(ctk.CTk):
    def __init__(self, csv_path, main_app):
        super().__init__()
        self.main_app = main_app  # Referencia a la ventana principal
        self.title("Seleccionar Jugadores")
        self.geometry("800x600")

        # Cargar datos y configurar atributos
        self.jugadores_df = pd.read_csv(csv_path)
        self.equipo = Equipo("Mi Equipo")
        self.formacion_actual = None
        self.jugadores_seleccionados = {}  # Guardar jugadores seleccionados por posición

        # Lista de posiciones
        self.posiciones = ["GK", "DEF", "MID", "FWD", "LI", "LD", "EI", "ED"]
        self.posicion_actual_idx = 0  # Índice de la posición actual

        # Crear el Notebook (pestañas)
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(pady=20, padx=20, fill="both", expand=True)

        # Configurar pestañas
        self.tab_seleccionar = ctk.CTkFrame(self.notebook)
        self.notebook.add(self.tab_seleccionar, text="Seleccionar Jugadores")

        self.tab_plantilla = ctk.CTkFrame(self.notebook)
        self.notebook.add(self.tab_plantilla, text="Ver Plantilla")

        # Pestaña "Seleccionar Jugadores"
        self.frame = ctk.CTkFrame(self.tab_seleccionar)
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

        # Evento para actualizar la pestaña de plantilla
        self.notebook.bind("<<NotebookTabChanged>>", self.cambiar_pestana)

    def elegir_formacion(self):
        formaciones_creadas = crear_formaciones()
        for formacion in formaciones_creadas:
            self.equipo.agregar_formacion(formacion)

        self.formacion_actual = formaciones_creadas[0]
        self.label_formacion.configure(text=f"Formación: {self.formacion_actual.nombre} ({self.formacion_actual.formacion})")

    def mostrar_jugadores_por_posicion(self):
        posicion = self.posiciones[self.posicion_actual_idx]
        posicion_filtrada = self.obtener_posicion_filtrada(posicion)

        jugadores = self.jugadores_df[
            (self.jugadores_df['Position'] == posicion_filtrada) &
            (~self.jugadores_df['Name'].isin(self.jugadores_seleccionados.values()))
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
        self.jugadores_seleccionados[posicion] = jugador['Name']
        self.label_status.configure(text=f"Seleccionado: {jugador['Name']} para la posición {posicion}.")
        self.posicion_actual_idx += 1

        if self.posicion_actual_idx >= len(self.posiciones):
            self.main_app.jugadores_seleccionados = self.jugadores_seleccionados
            self.label_status.configure(text="¡Selección completa!")
            self.regresar_al_menu()
        else:
            self.posicion_var.set(self.posiciones[self.posicion_actual_idx])
            self.mostrar_jugadores_por_posicion()

    def obtener_posicion_filtrada(self, posicion):
        return {
            "GK": "GK", "DEF": "CB", "LI": "LB", "LD": "RB",
            "MID": "CM", "FWD": "ST", "EI": "LW", "ED": "RW"
        }.get(posicion, None)

    def cambiar_pestana(self, event):
        if self.notebook.index("current") == 1:
            self.ver_plantilla()

    def ver_plantilla(self):
        for widget in self.tab_plantilla.winfo_children():
            widget.destroy()

        ctk.CTkLabel(self.tab_plantilla, text="Plantilla Actual:", font=("Arial", 16)).pack(pady=10)
        for posicion, jugador in self.jugadores_seleccionados.items():
            ctk.CTkLabel(self.tab_plantilla, text=f"{posicion}: {jugador}", font=("Arial", 12)).pack(pady=5)

    def regresar_al_menu(self):
        self.main_app.deiconify()
        self.destroy()


if __name__ == "__main__":
    class MainApp(tk.Tk):
        def __init__(self):
            super().__init__()
            self.jugadores_seleccionados = {}

    main_app = MainApp()
    main_app.withdraw()  # Ocultar la ventana principal
    app = SeleccionarJugadoresApp('APIs/jugadores_obtenidos.csv', main_app)
    app.mainloop()

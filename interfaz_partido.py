import customtkinter as ctk
from tkinter import messagebox
import pandas as pd
import random
import itertools  # Para aplanar la lista de jugadores

def center_window(window, width, height):
    # Obtener el tamaño de la pantalla
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()

    # Calcular las coordenadas (x, y) para centrar la ventana
    x = (screen_width // 2) - (width // 2)
    y = (screen_height // 2) - (height // 2)

    # Establecer el tamaño de la ventana y su ubicación
    window.geometry(f'{width}x{height}+{x}+{y}')
    
    
class PartidoApp(ctk.CTk):
    def __init__(self, jugadores_seleccionados, parent=None):
        super().__init__()
        self.title("Partido")
        self.geometry("800x500")
        center_window(self, 800, 500)
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        # Asegurarnos de que jugadores_seleccionados es una lista plana
        if isinstance(jugadores_seleccionados[0], list):
            self.jugadores_seleccionados = [item for sublist in jugadores_seleccionados for item in sublist]  # Aplanar la lista
        else:
            self.jugadores_seleccionados = jugadores_seleccionados  # Ya es una lista plana
        self.jugadores_df = pd.read_csv('APIs/all_players.csv')  # Cargar todos los jugadores desde el CSV
        self.formacion_rival = None
        self.parent = parent

        self.create_widgets()

    def create_widgets(self):
        title_label = ctk.CTkLabel(self, text="Partido", font=ctk.CTkFont(size=20, weight="bold"))
        title_label.pack(pady=20)

        difficulty_label = ctk.CTkLabel(self, text="Seleccione la dificultad:", font=ctk.CTkFont(size=16))
        difficulty_label.pack(pady=10)

        difficulty_frame = ctk.CTkFrame(self)
        difficulty_frame.pack(pady=10, padx=10, fill="x")

        btn_facil = ctk.CTkButton(difficulty_frame, text="Fácil", command=lambda: self.iniciar_partido("Facil"))
        btn_facil.pack(pady=5, fill="x")

        btn_normal = ctk.CTkButton(difficulty_frame, text="Normal", command=lambda: self.iniciar_partido("Normal"))
        btn_normal.pack(pady=5, fill="x")

        btn_dificil = ctk.CTkButton(difficulty_frame, text="Difícil", command=lambda: self.iniciar_partido("Dificil"))
        btn_dificil.pack(pady=5, fill="x")

        btn_leyenda = ctk.CTkButton(difficulty_frame, text="Leyenda", command=lambda: self.iniciar_partido("Leyenda"))
        btn_leyenda.pack(pady=5, fill="x")

        btn_volver = ctk.CTkButton(self, text="Volver", command=self.volver_al_menu)
        btn_volver.pack(pady=10)

        # Área para mostrar el resultado del partido
        self.resultados_text = ctk.CTkTextbox(self, height=150, width=500)
        self.resultados_text.pack(pady=20)
        
    def iniciar_partido(self, dificultad):
        if not self.jugadores_seleccionados:
            messagebox.showerror("Error", "No se ha definido ninguna plantilla de usuario.")
            return

        plantilla_usuario = self.obtener_plantilla_usuario()
        self.formacion_rival = self.generar_plantilla_rival(dificultad)
        if self.formacion_rival is None:
            messagebox.showerror("Error", "No se pudo generar la plantilla rival.")
            return

        comparacion = self.calcular_media_equipo(plantilla_usuario, self.formacion_rival)
        media_usuario = comparacion['Media Usuario'].mean()
        media_rival = comparacion['Media Rival'].mean()

        prob_victoria = self.calcular_probabilidad_victoria(media_usuario, media_rival, dificultad) 
        resultado = random.random() < prob_victoria

        if resultado:
            resultado_texto = "¡Victoria! Has ganado el partido."
        else:
            resultado_texto = "Derrota. Has perdido el partido."

        # Mostrar el resultado en la interfaz
        self.resultados_text.delete(1.0, ctk.END)  # Limpiar el área de resultados antes de mostrar el nuevo
        self.resultados_text.insert(ctk.END, f"Resultado del partido:\n{resultado_texto}\n\n")
        self.resultados_text.insert(ctk.END, f"Media Usuario: {media_usuario:.2f}\nMedia Rival: {media_rival:.2f}")
        
    def obtener_plantilla_usuario(self):
        """Convierte la lista de jugadores seleccionados en un DataFrame."""
        print(f"Jugadores seleccionados: {self.jugadores_seleccionados}")  # Depuración
        
        jugadores_df = self.jugadores_df[self.jugadores_df['Name'].isin(self.jugadores_seleccionados)]
        if jugadores_df.empty:
            print("No se encontraron jugadores en la plantilla del usuario.")
        else:
            print(f"Plantilla del usuario obtenida:\n{jugadores_df[['Name', 'OVR']].to_string(index=False)}")
        return jugadores_df

    def generar_plantilla_rival(self, dificultad):
        """Genera una plantilla rival basada en la dificultad y las posiciones requeridas."""
        # Definir rangos de media según dificultad
        if dificultad == "Facil":
            media_min, media_max = 60, 70
        elif dificultad == "Normal":
            media_min, media_max = 70, 80
        elif dificultad == "Dificil":
            media_min, media_max = 80, 85
        elif dificultad == "Leyenda":
            media_min, media_max = 85, 90
        else:
            print("Dificultad no reconocida.")
            return None
    
        # Filtrar jugadores por media
        jugadores_filtrados = self.jugadores_df[
            (self.jugadores_df['OVR'] >= media_min) & (self.jugadores_df['OVR'] <= media_max)
        ]

        if len(jugadores_filtrados) < 11:
            print(f"No hay suficientes jugadores para la dificultad {dificultad}.")
            return None

        # Lista de posiciones requeridas
        posiciones_requeridas = ["GK", "DEF", "DEF", "DEF", "DEF", "MID", "MID", "MID", "FWD", "EI", "ED"]
        plantilla_rival = pd.DataFrame(columns=jugadores_filtrados.columns)

        for posicion in posiciones_requeridas:
            if posicion == "GK":
                jugadores_posicion = jugadores_filtrados[jugadores_filtrados['Position'] == "GK"]
            elif posicion == "DEF":
                jugadores_posicion = jugadores_filtrados[jugadores_filtrados['Position'].isin(["CB", "LB", "RB"])]
            elif posicion == "MID":
                jugadores_posicion = jugadores_filtrados[jugadores_filtrados['Position'] == "CM"]
            elif posicion == "FWD":
                jugadores_posicion = jugadores_filtrados[jugadores_filtrados['Position'] == "ST"]
            elif posicion == "EI":
                jugadores_posicion = jugadores_filtrados[jugadores_filtrados['Position'] == "LW"]
            elif posicion == "ED":
                jugadores_posicion = jugadores_filtrados[jugadores_filtrados['Position'] == "RW"]
            else:
                print(f"Posición {posicion} no reconocida.")
                continue

            if not jugadores_posicion.empty:
                jugador_seleccionado = jugadores_posicion.sample(n=1)
                plantilla_rival = pd.concat([plantilla_rival, jugador_seleccionado], ignore_index=True)
                jugadores_filtrados = jugadores_filtrados.drop(jugador_seleccionado.index)

        if len(plantilla_rival) < 11:
            print("No se pudo completar la plantilla rival con las posiciones necesarias.")
            return None

        return plantilla_rival

    def calcular_media_equipo(self, plantilla_usuario, plantilla_rival):
        jugadores_usuario = plantilla_usuario['Name'].tolist()
        medias_usuario = plantilla_usuario['OVR'].tolist()
        jugadores_rival = plantilla_rival['Name'].tolist()
        medias_rival = plantilla_rival['OVR'].tolist()

        max_length = max(len(jugadores_usuario), len(medias_usuario), len(jugadores_rival), len(medias_rival))
        jugadores_usuario += [""] * (max_length - len(jugadores_usuario))
        medias_usuario += [0] * (max_length - len(medias_usuario))
        jugadores_rival += [""] * (max_length - len(jugadores_rival))
        medias_rival += [0] * (max_length - len(medias_rival))

        comparacion = pd.DataFrame({
            'Jugador Usuario': jugadores_usuario,
            'Media Usuario': medias_usuario,
            'Jugador Rival': jugadores_rival,
            'Media Rival': medias_rival
        })
        comparacion['Diferencia'] = comparacion['Media Usuario'] - comparacion['Media Rival']

        print("\nComparación de medias jugador por jugador:")
        print(comparacion.to_string(index=False))

        return comparacion

    def calcular_probabilidad_victoria(self, media_usuario, media_rival, dificultad):
        """Calcula la probabilidad de victoria basada en las medias y la dificultad."""
        prob_base = {"Facil": 0.8, "Normal": 0.6, "Dificil": 0.4, "Leyenda": 0.2}.get(dificultad, 0.5)
        diferencia = media_usuario - media_rival
        prob_victoria = prob_base + (diferencia * 0.01)
        prob_victoria = max(0, min(1, prob_victoria))  # Limitar entre 0 y 1
        return prob_victoria

    def volver_al_menu(self):
        if self.parent:
            self.destroy()
            self.parent.deiconify()

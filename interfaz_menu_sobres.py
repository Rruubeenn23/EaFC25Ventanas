# gui_sobres.py
# -*- coding: utf-8 -*-
"""
Created on Mon Oct 28 17:09:04 2024

@author: ruben
"""

import customtkinter as ctk
from interfaz_sobres import SobreBronce, SobrePlata, SobreOroNormal, SobreOroPromocional  # Importamos las clases necesarias

def center_window(window, width, height):
    # Obtener el tamaño de la pantalla
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()

    # Calcular las coordenadas (x, y) para centrar la ventana
    x = (screen_width // 2) - (width // 2)
    y = (screen_height // 2) - (height // 2)

    # Establecer el tamaño de la ventana y su ubicación
    window.geometry(f'{width}x{height}+{x}+{y}')
    
class SobresApp(ctk.CTk):
    def __init__(self, parent=None):
        super().__init__()
        self.parent = parent  # Guarda una referencia a la ventana principal (si se proporciona)
        self.title("Apertura de Sobres")
        self.geometry("500x400")
        center_window(self, 500, 400)
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        # Crear interfaz
        self.create_widgets()

        # Instancia las clases de sobres
        self.sobre_bronce = SobreBronce(self)
        self.sobre_plata = SobrePlata(self)
        self.sobre_oro_normal = SobreOroNormal(self)
        self.sobre_oro_promocional = SobreOroPromocional(self)

    def create_widgets(self):
        title_label = ctk.CTkLabel(self, text="Seleccione un tipo de sobre", font=ctk.CTkFont(size=20, weight="bold"))
        title_label.pack(pady=20)

        buttons_frame = ctk.CTkFrame(self)
        buttons_frame.pack(pady=10, padx=10, fill="both", expand=True)

        btn_bronce = ctk.CTkButton(buttons_frame, text="Sobre Bronce", command=self.abrir_sobre_bronce)
        btn_bronce.pack(pady=10, fill="x")

        btn_plata = ctk.CTkButton(buttons_frame, text="Sobre Plata", command=self.abrir_sobre_plata)
        btn_plata.pack(pady=10, fill="x")

        btn_oro_normal = ctk.CTkButton(buttons_frame, text="Sobre Oro Normal", command=self.abrir_sobre_oro_normal)
        btn_oro_normal.pack(pady=10, fill="x")

        btn_oro_promo = ctk.CTkButton(buttons_frame, text="Sobre Oro Promocional", command=self.abrir_sobre_oro_promocional)
        btn_oro_promo.pack(pady=10, fill="x")

        btn_volver = ctk.CTkButton(buttons_frame, text="Volver", command=self.volver_al_menu)
        btn_volver.pack(pady=10, fill="x")

    def abrir_sobre_bronce(self):
        # Llama al método open_pack del sobre de bronce
        self.sobre_bronce.open_pack()

    def abrir_sobre_plata(self):
        # Llama al método open_pack del sobre de plata
        self.sobre_plata.open_pack()

    def abrir_sobre_oro_normal(self):
        # Llama al método open_pack del sobre de oro normal
        self.sobre_oro_normal.open_pack()

    def abrir_sobre_oro_promocional(self):
        # Llama al método open_pack del sobre de oro promocional
        self.sobre_oro_promocional.open_pack()

    def volver_al_menu(self):
        if self.parent:
            self.destroy()
            self.parent.deiconify()  # Muestra la ventana principal si estaba oculta

    def mostrar_mensaje(self, mensaje):
        msg_box = ctk.CTkLabel(self, text=mensaje, font=ctk.CTkFont(size=16))
        msg_box.pack(pady=10)

    def show_pack_opening_animation(self, best_player, players):
        # Cierra la ventana de sobres antes de abrir la ventana de animación
        self.withdraw()
    
        # Abre una nueva ventana (Toplevel) para mostrar la animación del jugador
        animation_window = ctk.CTkToplevel(self)
        animation_window.title("Animación de Apertura de Sobre")
        animation_window.geometry("500x400")
        
        center_window(animation_window, 500, 400)
    
        # Asegurarse de que la ventana secundaria esté al frente
        animation_window.lift()  # O usar: animation_window.grab_set() para bloquear la ventana principal
    
        label_info = ctk.CTkLabel(animation_window, text="¡Sobre abierto!", font=("Arial", 24))
        label_info.pack(pady=50)
    
        self.animate_best_player(label_info, best_player, players, animation_window)


    def animate_best_player(self, label_info, best_player, players, animation_window):
        # Mostrar solo la media (OVR) del mejor jugador
        label_info.configure(text=f"Media: {best_player['OVR']}")
        animation_window.update()  # Actualizar la ventana para mostrar el cambio
    
        # Mostrar la posición después de un retraso
        self.after(2000, lambda: self.show_player_position(label_info, best_player, animation_window))
    
        # Mostrar el país después de otro retraso
        self.after(4000, lambda: self.show_player_nation(label_info, best_player, animation_window))
    
        # Mostrar el equipo después de otro retraso
        self.after(6000, lambda: self.show_player_team(label_info, best_player, animation_window))
    
        # Finalmente, mostrar todos los detalles del jugador
        self.after(8000, lambda: self.show_player_details(label_info, best_player, animation_window))
    
        # Mostrar los detalles de los otros jugadores con un retraso de 2 segundos entre ellos
        for i, player in enumerate(players):
            self.after(10000 + i * 2000, lambda p=player: self.show_player_details(label_info, p, animation_window))
    
        # Después de mostrar todos los jugadores, mostrar la lista de nombres y medias
        self.after(10000 + len(players) * 2000, lambda: self.show_player_list(players, animation_window))
    
    def show_player_position(self, label_info, player, animation_window):
        details = f"Posición: {player['Position']}"
        label_info.configure(text=details, font=("Arial", 14))
        animation_window.update()  # Actualizar la ventana para mostrar los cambios
    
    def show_player_nation(self, label_info, player, animation_window):
        details = f"Nación: {player['Nation']}"
        label_info.configure(text=details, font=("Arial", 14))
        animation_window.update()  # Actualizar la ventana para mostrar los cambios
    
    def show_player_team(self, label_info, player, animation_window):
        details = f"Equipo: {player['Team']}"
        label_info.configure(text=details, font=("Arial", 14))
        animation_window.update()  # Actualizar la ventana para mostrar los cambios
    
    def show_player_details(self, label_info, player, animation_window):
        # Muestra todos los detalles del jugador
        details = f"Nombre: {player['Name']}\n"
        details += f"OVR: {player['OVR']}\n"
        details += f"Posición: {player['Position']}\n"
        details += f"Nación: {player['Nation']}\n"
        details += f"Equipo: {player['Team']}\n"
        details += f"Liga: {player['League']}\n"
        details += f"PAC: {player['PAC']} SHO: {player['SHO']} PAS: {player['PAS']}\n"
        details += f"DRI: {player['DRI']} DEF: {player['DEF']} PHY: {player['PHY']}"
    
        label_info.configure(text=details, font=("Arial", 14))
        animation_window.update()  # Actualiza la ventana para mostrar los cambios
    
    def show_player_list(self, players, animation_window):
        # Crear una nueva lista con los nombres y medias
        player_list_text = "Lista de Jugadores:\n"
        for player in players:
            player_list_text += f"{player['Name']} - Media: {player['OVR']}\n"
    
        # Mostrar la lista en una etiqueta
        label_player_list = ctk.CTkLabel(animation_window, text=player_list_text, font=("Arial", 14))
        label_player_list.pack(pady=20)
    
        # Crear un botón "Volver"
        btn_volver = ctk.CTkButton(animation_window, text="Volver", command=animation_window.destroy)
        btn_volver.pack(pady=20)
    
        # Asegurarse de que la ventana esté al frente
        animation_window.lift()

        

if __name__ == "__main__":
    app = SobresApp()
    app.mainloop()

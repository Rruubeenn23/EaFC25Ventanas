import customtkinter as ctk
import pandas as pd
import random
import time
from abc import ABC, abstractmethod
from guardarJugadores import guardar_jugadores

# Cargar datos desde el archivo CSV
players_data = pd.read_csv('APIs/all_players.csv')

def center_window(window, width, height):
    # Obtener el tamaño de la pantalla
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()

    # Calcular las coordenadas (x, y) para centrar la ventana
    x = (screen_width // 2) - (width // 2)
    y = (screen_height // 2) - (height // 2)

    # Establecer el tamaño de la ventana y su ubicación
    window.geometry(f'{width}x{height}+{x}+{y}')
    


class Sobre(ABC):
    def __init__(self, probabilities, OVR_ranges, main_app):
        self.probabilities = probabilities
        self.OVR_ranges = OVR_ranges
        self.main_app = main_app  # Asegúrate de pasar el main_app
        self.categories = self._categorize_players()

    def _categorize_players(self):
        categories = {}
        for category, (min_OVR, max_OVR) in self.OVR_ranges.items():
            categories[category] = players_data[(players_data['OVR'] >= min_OVR) & (players_data['OVR'] <= max_OVR)]
        return categories

    @abstractmethod
    def open_pack(self):
        pass

class SobreBronce(Sobre):
    def __init__(self, main_app):
        probabilities = {
            '50-58': 0.7,
            '59-62': 0.25,
            '63-64': 0.05
        }
        OVR_ranges = {
            '50-58': (50, 58),
            '59-62': (59, 62),
            '63-64': (63, 64)
        }
        super().__init__(probabilities, OVR_ranges, main_app)

    def open_pack(self):
        players = []
        for _ in range(12):
            category = random.choices(
                list(self.probabilities.keys()),
                list(self.probabilities.values())
            )[0]
            
            if not self.categories[category].empty:
                player = self.categories[category].sample(1).iloc[0]
                players.append(player)

        if players:
            guardar_jugadores(pd.DataFrame(players))

        players = sorted(players, key=lambda x: x['OVR'], reverse=True)
        best_player = players[0]

        # Llama a la animación correctamente
        self.main_app.show_pack_opening_animation(best_player, players)


class SobrePlata(Sobre):
    def __init__(self, main_app):
        probabilities = {
            '65-68': 0.7,
            '69-72': 0.25,
            '73-74': 0.05
        }
        OVR_ranges = {
            '65-68': (65, 68),
            '69-72': (69, 72),
            '73-74': (73, 74)
        }
        super().__init__(probabilities, OVR_ranges, main_app)

    def open_pack(self):
        players = []
        for _ in range(12):
            category = random.choices(
                list(self.probabilities.keys()),
                list(self.probabilities.values())
            )[0]
            
            if not self.categories[category].empty:
                player = self.categories[category].sample(1).iloc[0]
                players.append(player)

        if players:
            guardar_jugadores(pd.DataFrame(players))

        players = sorted(players, key=lambda x: x['OVR'], reverse=True)
        best_player = players[0]

        # Llama a la animación correctamente
        self.main_app.show_pack_opening_animation(best_player, players)


class SobreOroNormal(Sobre):
    def __init__(self, main_app):
        probabilities = {
            '75-79': 0.7,
            '80-84': 0.25,
            '85+': 0.05
        }
        OVR_ranges = {
            '75-79': (75, 79),
            '80-84': (80, 84),
            '85+': (85, 99)
        }
        super().__init__(probabilities, OVR_ranges, main_app)

    def open_pack(self):
        players = []
        for _ in range(12):
            category = random.choices(
                list(self.probabilities.keys()),
                list(self.probabilities.values())
            )[0]
            
            if not self.categories[category].empty:
                player = self.categories[category].sample(1).iloc[0]
                players.append(player)

        if players:
            guardar_jugadores(pd.DataFrame(players))

        players = sorted(players, key=lambda x: x['OVR'], reverse=True)
        best_player = players[0]

        # Llama a la animación correctamente
        self.main_app.show_pack_opening_animation(best_player, players)


class SobreOroPromocional(Sobre):
    def __init__(self, main_app):
        probabilities = {
            '86-88': 0.7,
            '89-90': 0.25,
            '90+': 0.05
        }
        OVR_ranges = {
            '86-88': (86, 88),
            '89-90': (89, 90),
            '90+': (90, 99)
        }
        super().__init__(probabilities, OVR_ranges, main_app)

    def open_pack(self):
        players = []
        for _ in range(5):
            category = random.choices(
                list(self.probabilities.keys()),
                list(self.probabilities.values())
            )[0]
            
            if not self.categories[category].empty:
                player = self.categories[category].sample(1).iloc[0]
                players.append(player)

        if players:
            guardar_jugadores(pd.DataFrame(players))

        players = sorted(players, key=lambda x: x['OVR'], reverse=True)
        best_player = players[0]

        # Llama a la animación correctamente
        self.main_app.show_pack_opening_animation(best_player, players)


class MainApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Apertura de Sobres")
        self.geometry("800x600")
        
        center_window(self, 800, 600)

        # Instancia los sobres
        self.sobre_bronce = SobreBronce(self)
        self.sobre_plata = SobrePlata(self)
        self.sobre_oro_normal = SobreOroNormal(self)
        self.sobre_oro_promocional = SobreOroPromocional(self)

        # Añadir botones y otras configuraciones de UI
        self.label_info = ctk.CTkLabel(self, text="Haz clic para abrir un sobre", font=("Arial", 20))
        self.label_info.pack(pady=50)

        self.button_open_bronce = ctk.CTkButton(self, text="Abrir Sobre Bronce", command=self.abir_sobre_bronce)
        self.button_open_bronce.pack(pady=20)

        self.button_open_plata = ctk.CTkButton(self, text="Abrir Sobre Plata", command=self.abir_sobre_plata)
        self.button_open_plata.pack(pady=20)

        self.button_open_oro_normal = ctk.CTkButton(self, text="Abrir Sobre Oro Normal", command=self.abir_sobre_oro_normal)
        self.button_open_oro_normal.pack(pady=20)

        self.button_open_oro_promocional = ctk.CTkButton(self, text="Abrir Sobre Oro Promocional", command=self.abir_sobre_oro_promocional)
        self.button_open_oro_promocional.pack(pady=20)

    def abir_sobre_bronce(self):
        # Llama correctamente al método de apertura de sobres
        self.label_info.configure(text="Abriendo sobre...", font=("Arial", 18))
        self.button_open_bronce.configure(state="disabled")  # Deshabilita el botón
        self.after(500, lambda: self.sobre_bronce.open_pack())  # Abre el sobre después de medio segundo

    def abir_sobre_plata(self):
        # Llama correctamente al método de apertura de sobres
        self.label_info.configure(text="Abriendo sobre...", font=("Arial", 18))
        self.button_open_plata.configure(state="disabled")  # Deshabilita el botón
        self.after(500, lambda: self.sobre_plata.open_pack())  # Abre el sobre después de medio segundo

    def abir_sobre_oro_normal(self):
        # Llama correctamente al método de apertura de sobres
        self.label_info.configure(text="Abriendo sobre...", font=("Arial", 18))
        self.button_open_oro_normal.configure(state="disabled")  # Deshabilita el botón
        self.after(500, lambda: self.sobre_oro_normal.open_pack())  # Abre el sobre después de medio segundo

    def abir_sobre_oro_promocional(self):
        # Llama correctamente al método de apertura de sobres
        self.label_info.configure(text="Abriendo sobre...", font=("Arial", 18))
        self.button_open_oro_promocional.configure(state="disabled")  # Deshabilita el botón
        self.after(500, lambda: self.sobre_oro_promocional.open_pack())  # Abre el sobre después de medio segundo

    def show_pack_opening_animation(self, best_player, players):
        # Iniciar la animación de apertura del sobre
        self.label_info.configure(text="¡Sobre abierto!", font=("Arial", 24))

        # Mostrar al mejor jugador
        self.after(1000, lambda: self.animate_best_player(best_player))

        # Mostrar otros jugadores con retraso
        for i, player in enumerate(players):
            self.after(3000 + i * 2000, lambda p=player: self.show_player_details(p))

    def animate_best_player(self, best_player):
        self.label_info.configure(text=f"Jugador de portada: {best_player['Name']}", font=("Arial", 18))
        self.after(2000, lambda: self.show_player_details(best_player))

    def show_player_details(self, player):
        details = f"Nombre: {player['Name']}\nOVR: {player['OVR']}\n"
        details += f"Posición: {player['Position']}\nNación: {player['Nation']}\n"
        details += f"Equipo: {player['Team']}\nLiga: {player['League']}\n"
        details += f"PAC: {player['PAC']} SHO: {player['SHO']} PAS: {player['PAS']}\n"
        details += f"DRI: {player['DRI']} DEF: {player['DEF']} PHY: {player['PHY']}"
        
        self.label_info.configure(text=details, font=("Arial", 14))
        

# Ejecutar la aplicación
if __name__ == "__main__":
    app = MainApp()
    app.mainloop()

import customtkinter as ctk
import pandas as pd
from interfaz_menu_sobres import SobresApp  # Importar la interfaz de sobres
from interfaz_partido import PartidoApp
from interfaz_crear_plantilla import CrearPlantillaApp  # Importamos la clase SeleccionarJugadoresApp
from interfaz_ver_plantilla import VerPlantillaApp  # Importamos la clase VerPlantillaApp

def center_window(window, width, height):
    # Obtener el tamaño de la pantalla
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()

    # Calcular las coordenadas (x, y) para centrar la ventana
    x = (screen_width // 2) - (width // 2)
    y = (screen_height // 2) - (height // 2)

    # Establecer el tamaño de la ventana y su ubicación
    window.geometry(f'{width}x{height}+{x}+{y}')
    
    
class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Menú Principal")
        self.geometry("600x400")
        
        center_window(self, 600, 400)
        
        ctk.set_appearance_mode("dark")  # Modo oscuro
        ctk.set_default_color_theme("blue")  # Tema azul

        # Inicializar datos
        self.jugadores_seleccionados = []  # Usamos una lista vacía en lugar de un DataFrame
        self.jugadores_df = pd.read_csv('APIs/all_players.csv')

        # Crear la interfaz
        self.create_widgets()

    def create_widgets(self):
        title_label = ctk.CTkLabel(self, text="Menú Principal", font=ctk.CTkFont(size=24, weight="bold"))
        title_label.pack(pady=20)

        buttons_frame = ctk.CTkFrame(self)
        buttons_frame.pack(pady=10, padx=10, fill="both", expand=True)

        btn_abrir_sobres = ctk.CTkButton(buttons_frame, text="Abrir Sobres", command=self.abrir_sobres)
        btn_abrir_sobres.pack(pady=10, fill="x")

        btn_hacer_plantilla = ctk.CTkButton(buttons_frame, text="Hacer Plantilla", command=self.hacer_plantilla)
        btn_hacer_plantilla.pack(pady=10, fill="x")

        btn_ver_plantilla = ctk.CTkButton(buttons_frame, text="Ver Plantilla", command=self.ver_plantilla)
        btn_ver_plantilla.pack(pady=10, fill="x")

        btn_jugar_partido = ctk.CTkButton(buttons_frame, text="Jugar Partido", command=self.jugar_partido)
        btn_jugar_partido.pack(pady=10, fill="x")

        btn_salir = ctk.CTkButton(buttons_frame, text="Salir", command=self.salir)
        btn_salir.pack(pady=10, fill="x")

    def abrir_sobres(self):
        self.withdraw()  # Oculta la ventana principal
        sobres_app = SobresApp(self)  # Crea la ventana de sobres, pasando la ventana principal como referencia
        sobres_app.mainloop()

    def hacer_plantilla(self):
        # Llama al método de la clase SeleccionarJugadores para hacer la plantilla
        self.withdraw()  # Oculta la ventana principal
        crearplantilla = CrearPlantillaApp('APIs/jugadores_obtenidos.csv', self)
        crearplantilla.mainloop()

    def ver_plantilla(self):
        """Este método ahora redirige a la interfaz para mostrar la plantilla gráficamente."""
        self.withdraw()  # Oculta la ventana principal
        # Pasa los jugadores seleccionados y la referencia a la ventana principal
        verplantilla = VerPlantillaApp(self.jugadores_seleccionados, self)
        verplantilla.mainloop()

    def jugar_partido(self):
        print("Redirigiendo a la interfaz de partido...")  # Para depuración
        
        # Verificar si la lista de jugadores seleccionados está vacía
        if not self.jugadores_seleccionados:
            print("Error", "No se han seleccionado jugadores para jugar.")
            return
    
        self.withdraw()  # Oculta la ventana principal
        partido_app = PartidoApp(self.jugadores_seleccionados, self)  # Pasa la lista de jugadores seleccionados
        partido_app.mainloop()
        

    def salir(self):
        self.destroy()

    def agregar_jugador_a_plantilla(self, jugador_seleccionado):
        """Esta función agrega un jugador a la plantilla rival."""
        self.jugadores_seleccionados.append(jugador_seleccionado)  # Añadimos el jugador a la lista de seleccionados


if __name__ == "__main__":
    app = App()
    app.mainloop()

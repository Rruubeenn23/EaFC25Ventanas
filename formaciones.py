class Formacion:
    def __init__(self, nombre, formacion, jugadores):
        self.nombre = nombre
        self.formacion = formacion  # Ejemplo: "4-3-3"
        self.jugadores = jugadores  # Lista de nombres de jugadores en orden
        self.jugadores_seleccionados = [None] * len(jugadores)  # Lista para almacenar jugadores seleccionados

    def mostrar_display(self):
        print(f"Formación: {self.nombre} ({self.formacion})")
        print("                      " + (self.jugadores_seleccionados[0] if self.jugadores_seleccionados[0] else "Portero"))  # Portero
        print("      " + "  ".join([jugador if jugador else "Defensa" for jugador in self.jugadores_seleccionados[1:5]]))  # Defensores
        print("             " + "  ".join([jugador if jugador else "Centro" for jugador in self.jugadores_seleccionados[5:8]]))  # Mediocampistas
        print("         " + "  ".join([jugador if jugador else "Delantero" for jugador in self.jugadores_seleccionados[8:]]))  # Delanteros
        print()


    def seleccionar_jugador(self, posicion, jugador):
        posiciones = ["GK", "LI", "DEF", "DEF", "LD", "MID", "EI", "FWD", "ED"]
        
        if posicion == "GK":
            self.jugadores_seleccionados[0] = jugador  # Portero
        elif posicion == "LI":
            if self.jugadores_seleccionados[1] is None:
                self.jugadores_seleccionados[1] = jugador
        elif posicion == "DEF":
            for i in range(2, 4):  # Comprobamos ambos defensores
                if self.jugadores_seleccionados[i] is None:
                    self.jugadores_seleccionados[i] = jugador
                    break
        elif posicion == "LD":
            if self.jugadores_seleccionados[4] is None:
                self.jugadores_seleccionados[4] = jugador
        elif posicion == "MID":
            for i in range(5, 8):  # Mediocampistas
                if self.jugadores_seleccionados[i] is None:
                    self.jugadores_seleccionados[i] = jugador
                    break     
        elif posicion == "EI":
            if self.jugadores_seleccionados[8] is None:
                self.jugadores_seleccionados[8] = jugador
                
        elif posicion == "FWD":
            if self.jugadores_seleccionados[9] is None:
                self.jugadores_seleccionados[9] = jugador

        elif posicion == "ED":
            if self.jugadores_seleccionados[10] is None:
                self.jugadores_seleccionados[10] = jugador
                
    def obtener_plantilla(self):
        """Devuelve la lista de jugadores en la formación actual."""
        return self.jugadores_seleccionados  # Devolver solo los nombres de los jugadores
    
    def get_jugadores(self):
        """Devuelve la lista de jugadores seleccionados."""
        return self.jugadores_seleccionados

class Equipo:
    def __init__(self, nombre):
        self.nombre = nombre
        self.formaciones = []

    def agregar_formacion(self, formacion):
        self.formaciones.append(formacion)

    def mostrar_formaciones(self):
        print(f"Equipo: {self.nombre}\nFormaciones:")
        for formacion in self.formaciones:
            formacion.mostrar_display()

def crear_formaciones():
    formacion_433 = Formacion("433", "4-3-3", [
        "Portero",
        "Defensa 1", "Defensa 2", "Defensa 3", "Defensa 4",
        "Centro 1", "Centro 2", "Centro 3",
        "Delantero 1", "Delantero 2", "Delantero 3"
    ])
    

    return [formacion_433]

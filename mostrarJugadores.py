import pandas as pd

# Definir la ruta del archivo CSV donde se guardan los jugadores
csv_file_path = 'APIs/jugadores_obtenidos.csv'

def mostrar_jugadores():
    """
    Función para leer el archivo CSV y mostrar los jugadores.
    """
    try:
        # Cargar los datos del archivo CSV
        jugadores = pd.read_csv(csv_file_path)
        
        # Verificar si el DataFrame está vacío
        if jugadores.empty:
            print("No hay ningun jugador en el club. Prueba a abrir algún sobre.")
            return

        # Crear un DataFrame con los encabezados en español
        jugadores_en_espanol = jugadores[['Name', 'OVR', 'Nation', 'Team', 'Position']]
        jugadores_en_espanol.columns = ['Nombre', 'OVR', 'Nacionalidad', 'Equipo', 'Posición']

        # Mostrar los jugadores
        print(f"\nSe han encontrado {len(jugadores)} jugadores:\n")
        print(jugadores_en_espanol)  # Mostrar con encabezados en español
    except FileNotFoundError:
        print(f"\nNo hay ningún jugador en el club. Abre algún sobre")
    except Exception as e:
        print(f"\nOcurrió un error al intentar leer el archivo: {e}")

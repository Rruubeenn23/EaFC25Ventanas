# -*- coding: utf-8 -*-
"""
Created on Mon Oct 28 17:49:30 2024

@author: ruben
"""

import pandas as pd
import os

# Definir la ruta del archivo CSV donde se guardarán los jugadores obtenidos
csv_file_path = 'APIs/jugadores_obtenidos.csv'
players_club = pd.read_csv('APIs/jugadores_obtenidos.csv')

def guardar_jugadores(players):
    """
    Función para guardar los jugadores en un archivo CSV.
    :param players: Lista de jugadores (DataFrame) que se añadirán al archivo CSV.
    """
    # Comprobar si el archivo ya existe
    if os.path.exists(csv_file_path):
        # Si existe, cargar los datos actuales
        jugadores_guardados = pd.read_csv(csv_file_path)
    else:
        # Si no existe, crear un DataFrame vacío con las mismas columnas que el CSV original
        jugadores_guardados = pd.DataFrame(columns=[
            'Unnamed: 0', 'Rank', 'Name', 'OVR', 'PAC', 'SHO', 'PAS', 'DRI', 'DEF', 'PHY', 'Acceleration', 'Sprint Speed', 
            'Positioning', 'Finishing', 'Shot Power', 'Long Shots', 'Volleys', 'Penalties', 'Vision', 'Crossing', 
            'Free Kick Accuracy', 'Short Passing', 'Long Passing', 'Curve', 'Dribbling', 'Agility', 'Balance', 'Reactions', 
            'Ball Control', 'Composure', 'Interceptions', 'Heading Accuracy', 'Def Awareness', 'Standing Tackle', 'Sliding Tackle', 
            'Jumping', 'Stamina', 'Strength', 'Aggression', 'Position', 'Weak foot', 'Skill moves', 'Preferred foot', 
            'Height', 'Weight', 'Alternative positions', 'Age', 'Nation', 'League', 'Team', 'play style', 'url', 
            'GK Diving', 'GK Handling', 'GK Kicking', 'GK Positioning', 'GK Reflexes'
        ])

    # Añadir los nuevos jugadores obtenidos al DataFrame existente
    jugadores_guardados = pd.concat([jugadores_guardados, players], ignore_index=True)

    # Ordenar el DataFrame por OVR de mayor a menor
    jugadores_guardados = jugadores_guardados.sort_values(by=['OVR', 'Name'], ascending=False)

    # Guardar los datos actualizados en el archivo CSV
    jugadores_guardados.to_csv(csv_file_path, index=False)
    print(f"{len(players)} jugadores han sido guardados en el club.")

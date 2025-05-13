import json
import os
import pygame
from constantes import SCREEN_SIZE
from Screens.save_screen import mostrar_save_screen

def save_score(score, main_screen):
    nombre_jugador = mostrar_save_screen(score, main_screen)

    if nombre_jugador is None:
        return False

    if not nombre_jugador.strip():
        nombre_jugador = "Anónimo"

    datos = {"nombre": nombre_jugador.strip(), "puntaje": score}

    if not os.path.exists('Saves'):
        os.makedirs('Saves')

    try:
        archivo = 'Saves/puntajes.json'
        puntajes = []

        if os.path.exists(archivo):
            with open(archivo, 'r') as f:
                puntajes = json.load(f)

        # Actualizar puntajes
        existe = False
        for i, p in enumerate(puntajes):
            if p['nombre'].lower() == datos['nombre'].lower():
                if score > p['puntaje']:
                    puntajes[i] = datos
                existe = True
                break

        if not existe:
            puntajes.append(datos)

        puntajes.sort(key=lambda x: x['puntaje'], reverse=True)

        with open(archivo, 'w') as f:
            json.dump(puntajes[:10], f, indent=4)

        return True

    except Exception as e:
        print(f"Error al guardar: {e}")
        return False

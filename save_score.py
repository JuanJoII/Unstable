import json
import os
import pygame
from constantes import SCREEN_SIZE

def save_score(score, main_screen):
    # Configuración temporal de la ventana de entrada
    input_screen = pygame.display.set_mode((400, 300))
    pygame.display.set_caption("Guardar Puntaje")
    
    font = pygame.font.Font(None, 36)
    input_text = ""
    active = True
    
    clock = pygame.time.Clock()
    
    while active:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return None
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    active = False
                elif event.key == pygame.K_BACKSPACE:
                    input_text = input_text[:-1]
                else:
                    if event.unicode.isalnum() or event.unicode == ' ':
                        input_text += event.unicode
        
        input_screen.fill((0, 28, 42))
        
        prompt_text = font.render("Ingresa tu nombre:", True, (255, 255, 255))
        input_screen.blit(prompt_text, (50, 100))
        
        input_surface = font.render(input_text, True, (255, 255, 255))
        pygame.draw.rect(input_screen, (255, 255, 255), (50, 150, 300, 40), 2)
        input_screen.blit(input_surface, (60, 155))
        
        help_text = font.render("Presiona ENTER para guardar", True, (200, 200, 200))
        input_screen.blit(help_text, (50, 220))
        
        pygame.display.flip()
        clock.tick(30)
    
    pygame.display.set_mode((SCREEN_SIZE, SCREEN_SIZE))
    
    if not input_text.strip():
        input_text = "Anónimo"
    
    nombre_jugador = input_text.strip()
    datos = {
        "nombre": nombre_jugador,
        "puntaje": score
    }
    
    if not os.path.exists('Saves'):
        os.makedirs('Saves')
    
    archivo = 'Saves/puntajes.json'
    
    try:
        if os.path.exists(archivo):
            with open(archivo, 'r') as f:
                puntajes = json.load(f)
        else:
            puntajes = []
        
        # Buscar si ya existe un puntaje con el mismo nombre
        existe = False
        for i, puntaje in enumerate(puntajes):
            if puntaje['nombre'].lower() == nombre_jugador.lower():  # Comparación sin distinción de mayúsculas
                if score > puntaje['puntaje']:
                    # Reemplazar si el nuevo puntaje es mayor
                    puntajes[i] = datos
                    print(f"Puntaje actualizado para {nombre_jugador}")
                else:
                    print(f"El puntaje existente es mayor para {nombre_jugador}")
                existe = True
                break
        
        if not existe:
            puntajes.append(datos)
            print(f"Nuevo puntaje guardado para {nombre_jugador}")
        
        puntajes.sort(key=lambda x: x['puntaje'], reverse=True)
        
        puntajes = puntajes[:10]
        
        with open(archivo, 'w') as f:
            json.dump(puntajes, f, indent=4)
            
        return True
    
    except Exception as e:
        print(f"Error al guardar el puntaje: {e}")
        return False
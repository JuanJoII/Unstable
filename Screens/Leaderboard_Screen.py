import pygame
import json
import os
import math
from constantes import SCREEN_SIZE

pygame.init()
screen = pygame.display.set_mode((SCREEN_SIZE, SCREEN_SIZE))

# Fondo
background_image = pygame.image.load("Assets/UI/FondoUI.png").convert()
background_image = pygame.transform.scale(background_image, (SCREEN_SIZE, SCREEN_SIZE))

# Cargar imagen del botón de volver
boton_volver_img = pygame.image.load("Assets/UI/ButtonRed.png").convert_alpha()
button_size = (160, 48)
boton_volver_img = pygame.transform.scale(boton_volver_img, button_size)

# Colores
GOLD = (255, 215, 0)
SILVER = (192, 192, 192)
BRONZE = (205, 127, 50)
WHITE = (255, 255, 255)
GREEN = (100, 255, 100)
BLACK = (0, 0, 0)
LIGHT_BLUE = (100, 100, 255)

def cargar_puntajes():
    """Carga los puntajes desde el archivo JSON"""
    try:
        if os.path.exists('Saves/puntajes.json'):
            with open('Saves/puntajes.json', 'r') as f:
                puntajes = json.load(f)
                # Ordenar puntajes de mayor a menor
                puntajes.sort(key=lambda x: x['puntaje'], reverse=True)
                return puntajes
        else:
            return []
    except Exception as e:
        print(f"Error al cargar puntajes: {e}")
        return []

def draw_text_with_shadow(surface, text, font, color, shadow_color, pos):
    """Dibuja texto con sombra para mejor legibilidad"""
    shadow_pos = (pos[0] + 2, pos[1] + 2)
    shadow = font.render(text, True, shadow_color)
    surface.blit(shadow, shadow_pos)
    rendered_text = font.render(text, True, color)
    surface.blit(rendered_text, pos)

def draw_medal(surface, position, rank):
    """Dibuja una medalla según la posición en el ranking"""
    radius = 15
    if rank == 0:  # Oro
        color = GOLD
        text = "1"
    elif rank == 1:  # Plata
        color = SILVER
        text = "2"
    elif rank == 2:  # Bronce
        color = BRONZE
        text = "3"
    else:
        return  # No dibujamos medalla para posiciones fuera del podio
    
    pygame.draw.circle(surface, color, position, radius)
    pygame.draw.circle(surface, BLACK, position, radius, 2)
    
    small_font = pygame.font.Font("Assets/UI/PressStart2P.ttf", 12)
    text_surf = small_font.render(text, True, BLACK)
    text_rect = text_surf.get_rect(center=position)
    surface.blit(text_surf, text_rect)

def draw_leaderboard_screen(screen):
    screen.blit(background_image, (0, 0))
    
    # Fuentes
    title_font = pygame.font.Font("Assets/UI/PressStart2P.ttf", 24)
    header_font = pygame.font.Font("Assets/UI/PressStart2P.ttf", 16)
    score_font = pygame.font.Font("Assets/UI/PressStart2P.ttf", 18)
    score_font_small = pygame.font.Font("Assets/UI/PressStart2P.ttf", 14)
    button_font = pygame.font.Font("Assets/UI/PressStart2P.ttf", 16)
    
    # Título
    title_text = "MEJORES PUNTAJES"
    title_x = SCREEN_SIZE // 2 - title_font.size(title_text)[0] // 2
    draw_text_with_shadow(screen, title_text, title_font, GOLD, BLACK, (title_x, 50))
    
    # Cabecera de la tabla - diseño simplificado
    header_y = 100
    
    # Fondo para la cabecera
    header_bg = pygame.Rect(100, header_y - 5, SCREEN_SIZE - 200, 30)
    pygame.draw.rect(screen, (40, 40, 60), header_bg)
    pygame.draw.rect(screen, GOLD, header_bg, 2)
    
    # Textos de cabecera - simplificado a solo POS y JUGADOR
    draw_text_with_shadow(screen, "POS", header_font, WHITE, BLACK, (130, header_y))
    draw_text_with_shadow(screen, "JUGADOR", header_font, WHITE, BLACK, (220, header_y))
    
    # Cargar puntajes
    puntajes = cargar_puntajes()
    
    # Mostrar puntajes
    if not puntajes:
        no_scores_text = "No hay puntajes guardados"
        no_scores_x = SCREEN_SIZE // 2 - score_font.size(no_scores_text)[0] // 2
        draw_text_with_shadow(screen, no_scores_text, score_font, WHITE, BLACK, (no_scores_x, 150))
    else:
        for i, puntaje in enumerate(puntajes[:10]):  # Mostrar solo top 10
            # Calcular la posición vertical para cada entrada, con más espacio para nombre y puntaje
            pos_y = 150 + i * 50  # Más espacio entre filas
            
            # Fondo para cada fila, alternando colores
            row_bg_color = (30, 30, 45) if i % 2 == 0 else (40, 40, 60)
            row_bg = pygame.Rect(100, pos_y - 5, SCREEN_SIZE - 200, 40)  # Mayor altura para acomodar dos líneas
            pygame.draw.rect(screen, row_bg_color, row_bg)
            
            # Medallas para los 3 primeros lugares
            if i < 3:
                draw_medal(screen, (130, pos_y + 15), i)
            else:
                # Número de posición para el resto
                pos_text = f"{i+1}."
                draw_text_with_shadow(screen, pos_text, score_font, WHITE, BLACK, (130, pos_y + 5))
            
            # Nombre del jugador (en la línea superior)
            nombre = puntaje.get('nombre', 'Sin nombre')
            name_text = nombre[:15]  # Limitar longitud del nombre
            draw_text_with_shadow(screen, name_text, score_font, WHITE, BLACK, (220, pos_y))
            
            # Puntaje (en la línea inferior)
            try:
                puntos = puntaje.get('puntaje', 0)
                score_text = f"{puntos} pts"
                
                # Color según posición
                if i == 0:
                    score_color = GOLD
                elif i == 1:
                    score_color = SILVER
                elif i == 2:
                    score_color = BRONZE
                else:
                    score_color = GREEN
                    
                # Mostrar puntaje debajo del nombre, con fuente ligeramente más pequeña
                draw_text_with_shadow(screen, score_text, score_font_small, score_color, BLACK, (220, pos_y + 22))
            except:
                draw_text_with_shadow(screen, "Error", score_font_small, (255, 0, 0), BLACK, (220, pos_y + 22))
    
    # Botón de volver
    back_button_pos = (SCREEN_SIZE // 2 - button_size[0] // 2, SCREEN_SIZE - 100)
    back_button_rect = pygame.Rect(back_button_pos, button_size)
    screen.blit(boton_volver_img, back_button_pos)
    
    # Efecto hover para el botón
    mouse_pos = pygame.mouse.get_pos()
    hover_back = back_button_rect.collidepoint(mouse_pos)
    back_color = LIGHT_BLUE if hover_back else WHITE
    back_text = button_font.render("VOLVER", True, back_color)
    
    # Centrar texto en el botón
    screen.blit(back_text, (
        back_button_rect.centerx - back_text.get_width() // 2,
        back_button_rect.centery - back_text.get_height() // 2
    ))
    
    pygame.display.flip()
    return back_button_rect
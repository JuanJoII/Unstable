import pygame
import json
import os
from constantes import SCREEN_SIZE

# Inicialización de pygame
pygame.init()

# Fondo
background_image = pygame.image.load("Assets/UI/FondoUI.png").convert()
background_image = pygame.transform.scale(background_image, (SCREEN_SIZE, SCREEN_SIZE))

# Botón de volver (configuración inicial)
boton_volver_img_original = pygame.image.load("Assets/UI/ButtonRed.png").convert_alpha()
button_size = (160, 48)
boton_volver_img = pygame.transform.scale(boton_volver_img_original, button_size)

# Colores
GOLD = (255, 215, 0)
SILVER = (192, 192, 192)
BRONZE = (205, 127, 50)
WHITE = (255, 255, 255)
GREEN = (100, 255, 100)
BLACK = (0, 0, 0)
LIGHT_BLUE = (100, 100, 255)
DARK_BLUE = (20, 20, 40)
LIGHT_GRAY = (70, 70, 90)

def cargar_puntajes():
    """Carga los puntajes desde el archivo JSON"""
    try:
        if os.path.exists('Saves/puntajes.json'):
            with open('Saves/puntajes.json', 'r') as f:
                puntajes = json.load(f)
                puntajes.sort(key=lambda x: x['puntaje'], reverse=True)
                return puntajes
        return []
    except Exception as e:
        print(f"Error al cargar puntajes: {e}")
        return []

def draw_text_with_shadow(surface, text, font, color, shadow_color, pos):
    """Dibuja texto con sombra"""
    shadow_pos = (pos[0] + 2, pos[1] + 2)
    shadow = font.render(text, True, shadow_color)
    surface.blit(shadow, shadow_pos)
    surface.blit(font.render(text, True, color), pos)

def draw_medal(surface, position, rank):
    """Dibuja una medalla según la posición"""
    radius = 12
    colors = [GOLD, SILVER, BRONZE]
    if rank < 3:
        pygame.draw.circle(surface, colors[rank], position, radius)
        pygame.draw.circle(surface, BLACK, position, radius, 2)
        small_font = pygame.font.Font("Assets/UI/PressStart2P.ttf", 10)
        text_surf = small_font.render(str(rank+1), True, BLACK)
        surface.blit(text_surf, (position[0]-4, position[1]-6))

def draw_leaderboard_screen(screen, scroll_y=0, max_scroll=0):
    global boton_volver_img
    
    # Configuración del grid ajustada
    COL_POS = 60       # Ancho columna posición
    COL_NAME = 150     # Ancho columna nombre
    COL_SCORE = 100    # Ancho columna puntaje
    ROW_HEIGHT = 35    # Altura de fila
    TABLE_MARGIN = 40  # Margen lateral
    
    screen.blit(background_image, (0, 0))
    
    # Fuentes (ligeramente más pequeñas)
    title_font = pygame.font.Font("Assets/UI/PressStart2P.ttf", 20) 
    header_font = pygame.font.Font("Assets/UI/PressStart2P.ttf", 12)  
    score_font = pygame.font.Font("Assets/UI/PressStart2P.ttf", 12)  
    button_font = pygame.font.Font("Assets/UI/PressStart2P.ttf", 14)
    
    # Título más compacto
    title_text = "MEJORES PUNTAJES"
    title_x = SCREEN_SIZE // 2 - title_font.size(title_text)[0] // 2
    draw_text_with_shadow(screen, title_text, title_font, GREEN, BLACK, (title_x, 25)) 
    
    # Área de la tabla más estrecha
    table_width = COL_POS + COL_NAME + COL_SCORE + 20  
    table_rect = pygame.Rect(
        (SCREEN_SIZE - table_width)//2, 
        70, 
        table_width, 
        SCREEN_SIZE - 160 
    )
    
    # Fondo de la tabla con bordes más delgados
    pygame.draw.rect(screen, DARK_BLUE, table_rect)
    pygame.draw.rect(screen, GOLD, table_rect, 2) 
    
    # Superficie de contenido
    content_height = max(400, len(cargar_puntajes()) * ROW_HEIGHT + 40)
    content_surface = pygame.Surface((table_rect.width - 10, content_height)) 
    content_surface.fill(DARK_BLUE)
    
    # Cabecera más compacta
    header_bg = pygame.Rect(5, 5, table_rect.width - 10, 22)  # Más estrecha y baja
    pygame.draw.rect(content_surface, (50, 50, 80), header_bg)
    pygame.draw.rect(content_surface, GOLD, header_bg, 1)
    
    # Textos de cabecera ajustados
    draw_text_with_shadow(content_surface, "POS", header_font, WHITE, BLACK, (15, 8))
    draw_text_with_shadow(content_surface, "JUGADOR", header_font, WHITE, BLACK, (COL_POS + 5, 8))
    draw_text_with_shadow(content_surface, "PUNTOS", header_font, WHITE, BLACK, (COL_POS + COL_NAME + 5, 8))
    
    # Mostrar puntajes con mejor espaciado
    puntajes = cargar_puntajes()
    if puntajes:
        for i, puntaje in enumerate(puntajes[:10]):  # Mostrar solo top 10
            pos_y = 40 + i * ROW_HEIGHT  # Comenzar más arriba
            
            # Fondo de fila
            row_bg = pygame.Rect(5, pos_y - 3, table_rect.width - 10, ROW_HEIGHT - 5)
            pygame.draw.rect(content_surface, (40, 40, 60) if i % 2 == 0 else (50, 50, 70), row_bg)
            pygame.draw.rect(content_surface, (80, 80, 100), row_bg, 1)
            
            # Posición (sin punto si es menor a 10 para ahorrar espacio)
            pos_text = f"{i+1:02d}"  # Formato 01, 02, etc.
            draw_text_with_shadow(content_surface, pos_text, score_font, WHITE, BLACK, (15, pos_y + 8))
            
            # Medallas solo para top 3, mejor posicionadas
            if i < 3:
                medal_pos = (COL_POS - 25, pos_y + ROW_HEIGHT//2)  # Más a la izquierda
                draw_medal(content_surface, medal_pos, i)
            
            # Nombre del jugador (10 caracteres máximo)
            nombre = puntaje.get('nombre', 'Sin nombre')[:10]
            draw_text_with_shadow(content_surface, nombre, score_font, WHITE, BLACK, (COL_POS + 5, pos_y + 8))
            
            # Puntaje compacto
            try:
                puntos = puntaje.get('puntaje', 0)
                score_text = f"{puntos}p" 
                score_color = GOLD if i == 0 else SILVER if i == 1 else BRONZE if i == 2 else GREEN
                draw_text_with_shadow(content_surface, score_text, score_font, score_color, BLACK,
                                    (COL_POS + COL_NAME + 5, pos_y + 8))
            except:
                draw_text_with_shadow(content_surface, "Error", score_font, (255, 0, 0), BLACK,
                                    (COL_POS + COL_NAME + 5, pos_y + 8))
    
    # Scroll y dibujado del contenido
    max_scroll = max(0, content_height - table_rect.height + 10)
    scroll_y = max(0, min(scroll_y, max_scroll))
    screen.blit(content_surface, (table_rect.x + 5, table_rect.y + 5),
               (0, scroll_y, table_rect.width - 10, table_rect.height - 10))
    
    # Botón 
    boton_volver_img = pygame.transform.scale(boton_volver_img_original, button_size)
    back_button_pos = (SCREEN_SIZE//2 - button_size[0]//2, SCREEN_SIZE - 80) 
    back_button_rect = pygame.Rect(back_button_pos, button_size)
    screen.blit(boton_volver_img, back_button_pos)
    
    # Texto del botón
    mouse_pos = pygame.mouse.get_pos()
    hover_back = back_button_rect.collidepoint(mouse_pos)
    back_text = button_font.render("VOLVER", True, LIGHT_BLUE if hover_back else WHITE)
    screen.blit(back_text, (
        back_button_rect.centerx - back_text.get_width()//2,
        back_button_rect.centery - back_text.get_height()//2
    ))
    
    pygame.display.flip()
    return back_button_rect, table_rect
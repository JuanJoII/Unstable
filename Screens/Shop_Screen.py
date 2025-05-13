import pygame
from constantes import SCREEN_SIZE

pygame.font.init()

# Cargar fondo
background_img = pygame.image.load("Assets/UI/FondoUI.png").convert_alpha()
background_img = pygame.transform.scale(background_img, (SCREEN_SIZE, SCREEN_SIZE))

# Cargar botones
button_img = pygame.image.load("Assets/UI/ButtonRed.png").convert_alpha()
button_img = pygame.transform.scale(button_img, (150, 50))

# Ajustar tamaño para botones de la tienda
button_size = (160, 48)
boton_iniciar_img = pygame.image.load("Assets/UI/ButtonGreen.png").convert_alpha()
boton_iniciar_img = pygame.transform.scale(boton_iniciar_img, button_size)

# Botón de volver
boton_volver_img_original = pygame.image.load("Assets/UI/ButtonRed.png").convert_alpha()
button_size = (160, 48)
boton_volver_img = pygame.transform.scale(boton_volver_img_original, button_size)

# Fuentes
button_font = pygame.font.Font("Assets/UI/PressStart2P.ttf", 12)
title_font = pygame.font.Font("Assets/UI/PressStart2P.ttf", 20)

GOLD = (255, 215, 0)
SILVER = (192, 192, 192)
BRONZE = (205, 127, 50)
WHITE = (255, 255, 255)
GREEN = (100, 255, 100)
BLACK = (0, 0, 0)
LIGHT_BLUE = (100, 100, 255)
DARK_BLUE = (20, 20, 40)
LIGHT_GRAY = (70, 70, 90)

# Sombreros disponibles
hats = [
    {"nombre": "Sombrero Azul", "imagen": "Assets/Hats/hat_blue.png", "precio": 5},
    {"nombre": "Sombrero Rojo", "imagen": "Assets/Hats/hat_red.png", "precio": 8},
    {"nombre": "Sombrero Dorado", "imagen": "Assets/Hats/hat_purple.png", "precio": 15},
    {"nombre": "Sombrero Azul", "imagen": "Assets/Hats/hat_green.png", "precio": 20},
    {"nombre": "Sombrero Rojo", "imagen": "Assets/Hats/hat_onepi.png", "precio": 28},
    {"nombre": "Sombrero Dorado", "imagen": "Assets/Hats/hat_crown.png", "precio": 36},
]

for hat in hats:
    img = pygame.image.load(hat["imagen"]).convert_alpha()
    hat["img_obj"] = pygame.transform.scale(img, (64, 64))


def get_current_hat(sombrero_actual, sombreros_comprados, hats_list=None):
    if not sombrero_actual or sombrero_actual not in sombreros_comprados:
        return None
    
    if hats_list is None:
        hats_list = hats
    
    for hat in hats_list:
        if hat["nombre"] == sombrero_actual:
            return hat
    
    return None


def draw_text_with_shadow(surface, text, font, color, shadow_color, pos):
    shadow_pos = (pos[0] + 2, pos[1] + 2)
    shadow = font.render(text, True, shadow_color)
    surface.blit(shadow, shadow_pos)
    rendered_text = font.render(text, True, color)
    surface.blit(rendered_text, pos)


def draw_button(screen, x, y, text):
    screen.blit(button_img, (x, y))
    label = button_font.render(text, True, (0, 0, 0))
    label_rect = label.get_rect(center=(x + 75, y + 25))
    screen.blit(label, label_rect)
    return pygame.Rect(x, y, 150, 50)


def draw_shop_screen(screen, monedas, sombrero_actual, sombreros_comprados, scroll_offset, error_message=None):
    # Configuración de diseño
    COL_WIDTH = 340
    ITEM_HEIGHT = 70
    MARGIN_X = 30
    MARGIN_Y = 80
    INFO_AREA_HEIGHT = 40  # Espacio para mensajes
    
    # Fuentes
    title_font = pygame.font.Font("Assets/UI/PressStart2P.ttf", 18)
    item_font = pygame.font.Font("Assets/UI/PressStart2P.ttf", 12)
    button_font = pygame.font.Font("Assets/UI/PressStart2P.ttf", 14)
    info_font = pygame.font.Font("Assets/UI/PressStart2P.ttf", 12)
    
    # Colores
    COLOR_TITULO = (0, 200, 0)
    COLOR_TEXTO = WHITE
    COLOR_SOMBRA = BLACK
    COLOR_MONEDAS = GOLD
    COLOR_EQUIPADO = (0, 255, 100)
    COLOR_COMPRADO = LIGHT_BLUE
    COLOR_NO_COMPRADO = (255, 100, 100)
    COLOR_ERROR = (255, 50, 50)
    COLOR_INFO = (100, 255, 100)
    
    screen.blit(background_img, (0, 0))
    mouse_pos = pygame.mouse.get_pos()
    
    # Título
    title_text = "TIENDA DE SOMBREROS"
    title_x = SCREEN_SIZE // 2 - title_font.size(title_text)[0] // 2
    draw_text_with_shadow(screen, title_text, title_font, COLOR_TITULO, COLOR_SOMBRA, (title_x, 30))
    
    # Monedas
    monedas_text = f"MONEDAS: {monedas}"
    draw_text_with_shadow(screen, monedas_text, item_font, COLOR_MONEDAS, COLOR_SOMBRA, (MARGIN_X, 60))
    
    # Área de items con scroll 
    table_height = SCREEN_SIZE - MARGIN_Y - 100 - INFO_AREA_HEIGHT
    table_rect = pygame.Rect(MARGIN_X, MARGIN_Y, COL_WIDTH, table_height)
    pygame.draw.rect(screen, DARK_BLUE, table_rect)
    pygame.draw.rect(screen, GOLD, table_rect, 2)
    
    # Superficie de contenido
    content_height = len(hats) * (ITEM_HEIGHT + 10)
    content_surface = pygame.Surface((table_rect.width - 20, content_height))
    content_surface.fill(DARK_BLUE)
    
    button_rects = []
    
    for i, hat in enumerate(hats):
        item_y = 10 + i * (ITEM_HEIGHT + 10)
        item_rect = pygame.Rect(10, item_y, table_rect.width - 40, ITEM_HEIGHT)
        
        # Fondo del ítem
        pygame.draw.rect(content_surface, (40, 40, 60) if i % 2 == 0 else (50, 50, 70), item_rect)
        pygame.draw.rect(content_surface, (80, 80, 100), item_rect, 1)
        
        # Imagen del sombrero
        hat_img = pygame.transform.scale(hat["img_obj"], (50, 50))
        content_surface.blit(hat_img, (20, item_y + 10))
        
        # Estado del sombrero
        comprado = hat["nombre"] in sombreros_comprados
        if sombrero_actual == hat["nombre"]:
            estado = "EQUIPADO"
            color_estado = COLOR_EQUIPADO
        elif comprado:
            estado = "COMPRADO"
            color_estado = COLOR_COMPRADO
        else:
            estado = f"PRECIO: {hat['precio']} MONEDAS"
            color_estado = COLOR_NO_COMPRADO
        
        # Textos del ítem
        draw_text_with_shadow(content_surface, hat["nombre"], item_font, COLOR_TEXTO, COLOR_SOMBRA, (80, item_y + 15))
        draw_text_with_shadow(content_surface, estado, item_font, color_estado, COLOR_SOMBRA, (80, item_y + 40))
        
        # Rectángulo clickeable
        click_rect = pygame.Rect(
            table_rect.x + 10,
            table_rect.y + 10 + item_y - scroll_offset,
            table_rect.width - 40,
            ITEM_HEIGHT
        )
        button_rects.append((click_rect, hat))
    
    # Manejo del scroll
    max_scroll = max(0, content_height - table_rect.height)
    scroll_offset = max(0, min(scroll_offset, max_scroll))
    
    # Dibujar contenido con scroll
    screen.blit(content_surface, (table_rect.x + 10, table_rect.y + 10), 
               (0, scroll_offset, table_rect.width - 20, table_rect.height - 20))
    
    # Barra de scroll
    if content_height > table_rect.height:
        scroll_bar_height = table_rect.height * (table_rect.height / content_height)
        scroll_bar_pos = table_rect.y + 10 + (table_rect.height - scroll_bar_height - 20) * (scroll_offset / max_scroll if max_scroll > 0 else 0)
        pygame.draw.rect(screen, LIGHT_GRAY, (table_rect.right-8, scroll_bar_pos, 6, scroll_bar_height))
    
    # Área de información
    info_area_y = table_rect.bottom + 10
    info_bg = pygame.Rect(MARGIN_X, info_area_y, COL_WIDTH, INFO_AREA_HEIGHT)
    pygame.draw.rect(screen, GOLD, info_bg, 1)
    
    # Mostrar información
    current_hat = get_current_hat(sombrero_actual, sombreros_comprados)
    if error_message:
        error_text = f"ERROR: {error_message}"
        draw_text_with_shadow(screen, error_text, info_font, COLOR_ERROR, COLOR_SOMBRA, 
                            (SCREEN_SIZE//2 - info_font.size(error_text)[0]//2, info_area_y + 15))
    elif current_hat:
        equipado_text = f"EQUIPADO: {current_hat['nombre']}"
        draw_text_with_shadow(screen, equipado_text, info_font, COLOR_INFO, COLOR_SOMBRA, 
                            (SCREEN_SIZE//2 - info_font.size(equipado_text)[0]//2, info_area_y + 15))
    
    # Botones inferiores
    button_size = (160, 48)
    spacing = 20
    
    # Botón MENÚ
    menu_rect = pygame.Rect(
        SCREEN_SIZE//2 - button_size[0] - spacing//2, 
        SCREEN_SIZE - 70, 
        button_size[0], button_size[1]
    )
    screen.blit(boton_volver_img, menu_rect.topleft)
    hover_menu = menu_rect.collidepoint(mouse_pos)
    menu_text = button_font.render("MENÚ", True, LIGHT_BLUE if hover_menu else WHITE)
    screen.blit(menu_text, (
        menu_rect.centerx - menu_text.get_width()//2,
        menu_rect.centery - menu_text.get_height()//2
    ))
    
    # Botón JUGAR
    jugar_rect = pygame.Rect(
        SCREEN_SIZE//2 + spacing//2, 
        SCREEN_SIZE - 70, 
        button_size[0], button_size[1]
    )
    screen.blit(boton_iniciar_img, jugar_rect.topleft)
    hover_jugar = jugar_rect.collidepoint(mouse_pos)
    jugar_text = button_font.render("JUGAR", True, LIGHT_BLUE if hover_jugar else WHITE)
    screen.blit(jugar_text, (
        jugar_rect.centerx - jugar_text.get_width()//2,
        jugar_rect.centery - jugar_text.get_height()//2
    ))

    
    pygame.display.flip()
    return button_rects, menu_rect, jugar_rect
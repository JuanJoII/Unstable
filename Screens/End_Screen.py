import pygame
from constantes import SCREEN_SIZE

pygame.init()

# Cargar recursos
background_image = pygame.image.load("Assets/UI/FondoUI.png").convert()
background_image = pygame.transform.scale(background_image, (SCREEN_SIZE, SCREEN_SIZE))

# Botones
boton_reintentar_img = pygame.image.load("Assets/UI/ButtonGreen.png").convert_alpha()
boton_menu_img = pygame.image.load("Assets/UI/ButtonRed.png").convert_alpha()
boton_store_img = pygame.image.load("Assets/UI/ButtonStore2.png").convert_alpha()

button_size = (160, 48)
boton_reintentar_img = pygame.transform.scale(boton_reintentar_img, button_size)
boton_menu_img = pygame.transform.scale(boton_menu_img, button_size)
boton_store_img = pygame.transform.scale(boton_store_img, button_size)

# Fuente
title_font = pygame.font.Font("Assets/UI/PressStart2P.ttf", 28)
button_font = pygame.font.Font("Assets/UI/PressStart2P.ttf", 12)

def draw_text_with_shadow(surface, text, font, color, shadow_color, pos):
    shadow = font.render(text, True, shadow_color)
    surface.blit(shadow, (pos[0] + 2, pos[1] + 2))
    rendered = font.render(text, True, color)
    surface.blit(rendered, pos)

def draw_end_screen(screen, result):
    screen.blit(background_image, (0, 0))

    # Texto de resultado
    text = "¡GANASTE!" if result == "player" else "PERDISTE..."
    text_color = (0, 255, 0) if result == "player" else (255, 80, 80)
    shadow_color = (0, 0, 0)

    title_surface = title_font.render(text, True, text_color)
    title_x = SCREEN_SIZE // 2 - title_surface.get_width() // 2
    title_y = 80
    draw_text_with_shadow(screen, text, title_font, text_color, shadow_color, (title_x, title_y))

    # Botones en columna centrados
    button_spacing = 25
    total_height = 5 * button_size[1] + 2 * button_spacing
    start_y = SCREEN_SIZE // 2 - total_height // 2 + 70 

    button_positions = [
        ("REINTENTAR", boton_reintentar_img, start_y),
        ("MENÚ", boton_menu_img, start_y + button_size[1] + button_spacing),
        ("TIENDA", boton_store_img, start_y + 2 * (button_size[1] + button_spacing))
    ]

    mouse_pos = pygame.mouse.get_pos()
    button_rects = []

    for label, image, y in button_positions:
        x = SCREEN_SIZE // 2 - button_size[0] // 2
        rect = pygame.Rect(x, y, *button_size)
        screen.blit(image, (x, y))

        is_hovered = rect.collidepoint(mouse_pos)
        text_color = (255, 255, 100) if is_hovered else (255, 255, 255)

        text_surface = button_font.render(label, True, text_color)
        text_x = rect.centerx - text_surface.get_width() // 2
        text_y = rect.centery - text_surface.get_height() // 2
        screen.blit(text_surface, (text_x, text_y))

        button_rects.append(rect)

    pygame.display.flip()
    return button_rects

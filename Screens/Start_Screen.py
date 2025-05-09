import pygame
from constantes import SCREEN_SIZE

pygame.init()
screen = pygame.display.set_mode((SCREEN_SIZE, SCREEN_SIZE))

# Fondo
background_image = pygame.image.load("Assets/UI/Unstable_Cover.jpg").convert()
background_image = pygame.transform.scale(background_image, (SCREEN_SIZE, SCREEN_SIZE))

# Cargar imágenes de los botones
boton_iniciar_img = pygame.image.load("Assets/UI/ButtonGreen.png").convert_alpha()
boton_salir_img = pygame.image.load("Assets/UI/ButtonRed.png").convert_alpha()

# Ajustar tamaño más pequeño
button_size = (160, 48)
boton_iniciar_img = pygame.transform.scale(boton_iniciar_img, button_size)
boton_salir_img = pygame.transform.scale(boton_salir_img, button_size)

def draw_text_with_shadow(surface, text, font, color, shadow_color, pos):
    shadow_pos = (pos[0] + 2, pos[1] + 2)
    shadow = font.render(text, True, shadow_color)
    surface.blit(shadow, shadow_pos)
    rendered_text = font.render(text, True, color)
    surface.blit(rendered_text, pos)

def draw_start_screen(screen):
    screen.blit(background_image, (0, 0))

    # Fuentes
    title_font = pygame.font.Font("Assets/UI/PressStart2P.ttf", 36)
    button_font = pygame.font.Font("Assets/UI/PressStart2P.ttf", 16)

    # Título centrado sobre los sapos
    title_text = "UNSTABLE"
    title_surface = title_font.render(title_text, True, (255, 255, 255))
    title_x = SCREEN_SIZE // 2 - title_surface.get_width() // 2
    title_y = SCREEN_SIZE // 2 - 100
    draw_text_with_shadow(screen, title_text, title_font, (0, 28, 42), (255, 255, 255), (title_x, title_y))

    # Coordenadas de botones
    spacing = 40
    button_y = SCREEN_SIZE - 80

    start_button_pos = (SCREEN_SIZE // 2 - button_size[0] - spacing // 2, button_y)
    exit_button_pos = (SCREEN_SIZE // 2 + spacing // 2, button_y)

    # Dibujar botones
    start_button_rect = pygame.Rect(start_button_pos, button_size)
    exit_button_rect = pygame.Rect(exit_button_pos, button_size)

    screen.blit(boton_iniciar_img, start_button_pos)
    screen.blit(boton_salir_img, exit_button_pos)

    # Detectar hover
    mouse_pos = pygame.mouse.get_pos()
    hover_start = start_button_rect.collidepoint(mouse_pos)
    hover_exit = exit_button_rect.collidepoint(mouse_pos)

    # Texto de botones con hover
    iniciar_color = (255, 255, 100) if hover_start else (255, 255, 255)
    salir_color = (255, 100, 100) if hover_exit else (255, 255, 255)

    iniciar_text = button_font.render("INICIAR", True, iniciar_color)
    salir_text = button_font.render("SALIR", True, salir_color)

    screen.blit(iniciar_text, (
        start_button_rect.centerx - iniciar_text.get_width() // 2,
        start_button_rect.centery - iniciar_text.get_height() // 2
    ))
    screen.blit(salir_text, (
        exit_button_rect.centerx - salir_text.get_width() // 2,
        exit_button_rect.centery - salir_text.get_height() // 2
    ))

    pygame.display.flip()

    # Devolver los rectángulos de los botones
    return start_button_rect, exit_button_rect


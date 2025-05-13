import pygame
from constantes import SCREEN_SIZE

pygame.init()
screen = pygame.display.set_mode((SCREEN_SIZE, SCREEN_SIZE))

def background(counter):
    # Fondo de la nueva pantalla
    if counter == 1:
        background_image = pygame.image.load("Assets/UI/GamePlay_Unstable1.png").convert_alpha()
    elif counter == 2:
        background_image = pygame.image.load("Assets/UI/GamePlay_Unstable2.png").convert_alpha()
    elif counter == 3:
        background_image = pygame.image.load("Assets/UI/GamePlay_Unstable3.png").convert_alpha()
    background_image = pygame.transform.scale(background_image, (SCREEN_SIZE, SCREEN_SIZE))
    return background_image

# Cargar imágenes de los botones
boton_saltar_img = pygame.image.load("Assets/UI/ButtonRed.png").convert_alpha()
boton_siguiente_img = pygame.image.load("Assets/UI/ButtonGreen.png").convert_alpha()

# Ajustar tamaño
button_size = (160, 48)
boton_saltar_img = pygame.transform.scale(boton_saltar_img, button_size)
boton_siguiente_img = pygame.transform.scale(boton_siguiente_img, button_size)


def draw_tuto_screen(screen, counter):
    screen.blit(background(counter), (0, 0))

    # Fuente
    button_font = pygame.font.Font("Assets/UI/PressStart2P.ttf", 16)

    # Posiciones de los botones abajo a los lados
    padding = 40
    y_pos = SCREEN_SIZE - button_size[1] - padding
    saltar_button_pos = (padding, y_pos)
    siguiente_button_pos = (SCREEN_SIZE - button_size[0] - padding, y_pos)

    # Crear rectángulos
    saltar_button_rect = pygame.Rect(saltar_button_pos, button_size)
    siguiente_button_rect = pygame.Rect(siguiente_button_pos, button_size)

    # Dibujar botones
    screen.blit(boton_saltar_img, saltar_button_pos)
    screen.blit(boton_siguiente_img, siguiente_button_pos)

    # Hover
    mouse_pos = pygame.mouse.get_pos()
    hover_saltar = saltar_button_rect.collidepoint(mouse_pos)
    hover_siguiente = siguiente_button_rect.collidepoint(mouse_pos)

    saltar_color = (255, 100, 100) if hover_saltar else (255, 255, 255)
    siguiente_color = (100, 255, 100) if hover_siguiente else (255, 255, 255)

    saltar_text = button_font.render("SALTAR", True, saltar_color)
    siguiente_text = button_font.render("SIGUIENTE", True, siguiente_color)

    # Centrar texto en botones
    screen.blit(saltar_text, (
        saltar_button_rect.centerx - saltar_text.get_width() // 2,
        saltar_button_rect.centery - saltar_text.get_height() // 2
    ))
    screen.blit(siguiente_text, (
        siguiente_button_rect.centerx - siguiente_text.get_width() // 2,
        siguiente_button_rect.centery - siguiente_text.get_height() // 2
    ))

    pygame.display.flip()
    return saltar_button_rect, siguiente_button_rect
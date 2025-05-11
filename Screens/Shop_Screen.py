import pygame
from constantes import SCREEN_SIZE

pygame.font.init()

# Cargar fondo
background_img = pygame.image.load("Assets/UI/FondoUI.png").convert_alpha()
background_img = pygame.transform.scale(background_img, (SCREEN_SIZE, SCREEN_SIZE))

# Cargar botones (Usando imágenes de la pantalla principal)
button_img = pygame.image.load("Assets/UI/ButtonRed.png").convert_alpha()
button_img = pygame.transform.scale(button_img, (150, 50))

# Ajustar tamaño más pequeño para botones de la tienda
button_size = (160, 48)
boton_iniciar_img = pygame.image.load("Assets/UI/ButtonGreen.png").convert_alpha()
boton_iniciar_img = pygame.transform.scale(boton_iniciar_img, button_size)

# Fuentes
button_font = pygame.font.Font("Assets/UI/PressStart2P.ttf", 12)
title_font = pygame.font.Font("Assets/UI/PressStart2P.ttf", 20)

# Sombreros disponibles
hats = [
    {"nombre": "Sombrero Azul", "imagen": "Assets/Hats/hat_blue.png", "precio": 5},
    {"nombre": "Sombrero Rojo", "imagen": "Assets/Hats/hat_red.png", "precio": 8},
    {"nombre": "Sombrero Dorado", "imagen": "Assets/Hats/hat_purple.png", "precio": 15},
]

for hat in hats:
    img = pygame.image.load(hat["imagen"]).convert_alpha()
    hat["img_obj"] = pygame.transform.scale(img, (64, 64))


def get_current_hat(sombrero_actual, sombreros_comprados, hats_list=None):
    """
    Retorna el sombrero actual equipado.
    
    Args:
        sombrero_actual (str): Nombre del sombrero actualmente equipado
        sombreros_comprados (list): Lista de nombres de sombreros que ha comprado el jugador
        hats_list (list, optional): Lista de sombreros disponibles. Si es None, usa la lista global.
    
    Returns:
        dict: Diccionario con la información del sombrero actual, o None si no hay ninguno equipado
    """
    # Si no hay un sombrero seleccionado o el sombrero no está en la lista de comprados
    if not sombrero_actual or sombrero_actual not in sombreros_comprados:
        return None
    
    # Usar la lista de sombreros proporcionada o la global
    if hats_list is None:
        hats_list = hats
    
    # Buscar el sombrero en la lista de sombreros disponibles
    for hat in hats_list:
        if hat["nombre"] == sombrero_actual:
            return hat
    
    # Si no se encuentra el sombrero (no debería ocurrir si los datos son consistentes)
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


def draw_shop_screen(screen, monedas, sombrero_actual, sombreros_comprados, scroll_offset):
    screen.blit(background_img, (0, 0))
    mouse_pos = pygame.mouse.get_pos()

    # === COLORES INTERNOS ===
    texto_victoria = (61, 171, 85)
    texto_hover = (255, 255, 100)
    texto_normal = (255, 255, 255)
    texto_sombra = (0, 0, 0)
    texto_monedas = (255, 215, 0)
    borde_hover = (255, 215, 0)
    borde_default = (200, 200, 200)

    # === TÍTULO ===
    draw_text_with_shadow(screen, "TIENDA DE SOMBREROS", button_font, texto_victoria, texto_sombra,
                          (SCREEN_SIZE // 2 - 100, 30))

    # === MONEDAS ===
    draw_text_with_shadow(screen, f"MONEDAS: {monedas}", button_font, texto_monedas, texto_sombra, (30, 60))
    
    # === SOMBRERO ACTUAL ===
    current_hat = get_current_hat(sombrero_actual, sombreros_comprados)
    if current_hat:
        draw_text_with_shadow(screen, f"EQUIPADO: {current_hat['nombre']}", button_font, 
                             (0, 255, 100), texto_sombra, (SCREEN_SIZE // 2 + 30, 60))
        screen.blit(current_hat["img_obj"], (SCREEN_SIZE // 2 + 220, 45))

    # === ÁREA SCROLL PARA SOMBREROS ===
    sombrero_area_rect = pygame.Rect(30, 100, SCREEN_SIZE - 60, SCREEN_SIZE - 180)
    pygame.draw.rect(screen, (255, 255, 255, 30), sombrero_area_rect, border_radius=10)

    sombrero_surface = pygame.Surface((sombrero_area_rect.width, 1000), pygame.SRCALPHA)

    button_rects = []
    start_y = -scroll_offset
    spacing_y = 95

    for i, hat in enumerate(hats):
        x = 20
        y = start_y + i * spacing_y

        rect = pygame.Rect(x, y, sombrero_area_rect.width - 40, 80)
        is_hovered = rect.move(sombrero_area_rect.topleft).collidepoint(mouse_pos)

        # Caja de sombrero
        pygame.draw.rect(sombrero_surface, texto_normal, rect, border_radius=10)
        pygame.draw.rect(sombrero_surface, borde_hover if is_hovered else borde_default, rect, 3, border_radius=10)

        # Imagen del sombrero
        sombrero_surface.blit(hat["img_obj"], (x + 10, y + 8))

        # Estado
        comprado = hat["nombre"] in sombreros_comprados
        if sombrero_actual == hat["nombre"]:
            estado = "¡Equipado!"
            color_estado = (0, 255, 100)
        elif comprado:
            estado = "Clic para Equipar"
            color_estado = (100, 200, 255)
        else:
            estado = f"Precio: {hat['precio']} M"
            color_estado = (255, 80, 80)

        # Textos con sombra y hover
        draw_text_with_shadow(sombrero_surface, hat["nombre"], button_font,
                              texto_hover if is_hovered else texto_normal, texto_sombra, (x + 90, y + 15))
        draw_text_with_shadow(sombrero_surface, estado, button_font, color_estado, texto_sombra, (x + 90, y + 40))

        button_rects.append((rect.move(sombrero_area_rect.topleft), hat))

    # Mostrar el área visible del scroll
    screen.blit(sombrero_surface, sombrero_area_rect.topleft,
                area=pygame.Rect(0, 0, sombrero_area_rect.width, sombrero_area_rect.height))

    # === BOTONES INFERIORES ===
    y_botones = SCREEN_SIZE - 65
    button_size = (150, 50)

    menu_rect = jugar_rect = None
    botones = [("MENÚ", SCREEN_SIZE // 2 - 160), ("JUGAR", SCREEN_SIZE // 2 + 10)]

    for texto, x in botones:
        rect = pygame.Rect(x, y_botones, *button_size)
        hovered = rect.collidepoint(mouse_pos)
        screen.blit(button_img, (x, y_botones))

        text_color = texto_hover if hovered else (0, 0, 0)
        text_surface = button_font.render(texto, True, text_color)
        text_rect = text_surface.get_rect(center=(x + button_size[0] // 2, y_botones + button_size[1] // 2))
        screen.blit(text_surface, text_rect)

        if texto == "MENÚ":
            menu_rect = rect
        else:
            jugar_rect = rect

    pygame.display.flip()
    return button_rects, menu_rect, jugar_rect


def handle_shop_click(mouse_pos, button_rects, sombreros_comprados, monedas, sombrero_actual):
    for rect, hat in button_rects:
        if rect.collidepoint(mouse_pos):
            if hat["nombre"] not in sombreros_comprados and monedas >= hat["precio"]:
                # Comprar sombrero nuevo
                sombreros_comprados.append(hat["nombre"])
                monedas -= hat["precio"]
                sombrero_actual = hat["nombre"]
                print(f"Comprando y equipando: {sombrero_actual}")
            elif hat["nombre"] in sombreros_comprados:
                sombrero_actual = hat["nombre"]
                print(f"Equipando sombrero: {sombrero_actual}")
            return sombrero_actual, sombreros_comprados, monedas
    return sombrero_actual, sombreros_comprados, monedas
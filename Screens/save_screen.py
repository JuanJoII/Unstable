import pygame
from constantes import SCREEN_SIZE

def mostrar_save_screen(score, screen):  # Ahora recibe la pantalla como parámetro
    # Fuentes
    title_font = pygame.font.Font("Assets/UI/PressStart2P.ttf", 20)
    input_font = pygame.font.Font("Assets/UI/PressStart2P.ttf", 18)
    help_font = pygame.font.Font("Assets/UI/PressStart2P.ttf", 12)

    BACKGROUND_COLOR = (0, 28, 42)
    TEXT_COLOR = (255, 255, 255)
    ACCENT_COLOR = (0, 255, 255)
    INPUT_BOX_COLOR = (50, 50, 80)

    try:
        background = pygame.image.load("Assets/UI/Unstable_Cover.jpg").convert()
        background = pygame.transform.scale(background, (SCREEN_SIZE, SCREEN_SIZE))
    except:
        background = None

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
                    if len(input_text) < 12 and (event.unicode.isalnum() or event.unicode == ' '):
                        input_text += event.unicode

        if background:
            screen.blit(background, (0, 0))
            overlay = pygame.Surface((SCREEN_SIZE, SCREEN_SIZE), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 180))
            screen.blit(overlay, (0, 0))
        else:
            screen.fill(BACKGROUND_COLOR)

        panel_rect = pygame.Rect(SCREEN_SIZE//2 - 180, SCREEN_SIZE//2 - 120, 360, 200)
        pygame.draw.rect(screen, (0, 28, 42, 220), panel_rect, border_radius=10)
        pygame.draw.rect(screen, ACCENT_COLOR, panel_rect, 2, border_radius=10)

        title_text = title_font.render("GUARDAR", True, ACCENT_COLOR)
        title_rect = title_text.get_rect(center=(SCREEN_SIZE//2, panel_rect.y + 30))
        screen.blit(title_text, title_rect)

        score_text = input_font.render(f"Puntos: {score}", True, TEXT_COLOR)
        score_rect = score_text.get_rect(center=(SCREEN_SIZE//2, panel_rect.y + 70))
        screen.blit(score_text, score_rect)

        input_box = pygame.Rect(SCREEN_SIZE//2 - 120, panel_rect.y + 100, 240, 30)
        pygame.draw.rect(screen, INPUT_BOX_COLOR, input_box, border_radius=5)  # Corregido: añadido input_box
        pygame.draw.rect(screen, ACCENT_COLOR, input_box, 2, border_radius=5)

        input_surface = input_font.render(input_text, True, TEXT_COLOR)
        screen.blit(input_surface, (input_box.x + 10, input_box.y + 5))

        if pygame.time.get_ticks() % 1000 < 500:
            cursor_pos = input_font.size(input_text)[0] + 12
            pygame.draw.line(screen, TEXT_COLOR,
                            (input_box.x + cursor_pos, input_box.y + 5),
                            (input_box.x + cursor_pos, input_box.y + 25), 2)

        help_text = help_font.render("ENTER para guardar", True, ACCENT_COLOR)
        help_rect = help_text.get_rect(center=(SCREEN_SIZE//2, panel_rect.y + 160))
        screen.blit(help_text, help_rect)

        pygame.display.flip()
        clock.tick(30)

    return input_text.strip()
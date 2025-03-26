import pygame
from constantes import SCREEN_SIZE

def draw_start_screen(screen):
    screen.fill((30, 30, 30))

    title_font = pygame.font.SysFont(None, 72)
    button_font = pygame.font.SysFont(None, 36)

    title_text = title_font.render("Arcade - IA", True, (255, 255, 255))
    screen.blit(title_text, (SCREEN_SIZE // 2 - title_text.get_width() // 2, SCREEN_SIZE // 2 - 150))

    mouse_pos = pygame.mouse.get_pos()
    button_rect = pygame.Rect(SCREEN_SIZE // 2 - 100, SCREEN_SIZE // 2, 200, 60)
    is_hovered = button_rect.collidepoint(mouse_pos)

    shadow_rect = button_rect.copy()
    shadow_rect.x += 3
    shadow_rect.y += 3
    pygame.draw.rect(screen, (0, 0, 0), shadow_rect, border_radius=12)

    button_color = (70, 200, 100) if is_hovered else (50, 150, 80)
    pygame.draw.rect(screen, button_color, button_rect, border_radius=12)
    pygame.draw.rect(screen, (255, 255, 255), button_rect, 2, border_radius=12)

    button_text = button_font.render("Iniciar Juego", True, (255, 255, 255))
    screen.blit(button_text, (button_rect.x + button_rect.width // 2 - button_text.get_width() // 2, button_rect.y + 10))

    pygame.display.flip()
    return button_rect
import pygame
import random
import copy
from constantes import TILE_SIZE, GRID_WIDTH, GRID_HEIGHT, MARGIN

pygame.init()

SCREEN_SIZE = TILE_SIZE * max(GRID_WIDTH, GRID_HEIGHT) + 2 * MARGIN
screen = pygame.display.set_mode((SCREEN_SIZE, SCREEN_SIZE))
pygame.display.set_caption("Arcade - Turno por Turno VISUAL")

tile_image_grass = pygame.image.load("Assets/Fondo/tileGrass.png")
tile_image_grass = pygame.transform.scale(tile_image_grass, (TILE_SIZE, TILE_SIZE))
tile_image_dirt = pygame.image.load("Assets/Fondo/tileDirt.png")
tile_image_dirt = pygame.transform.scale(tile_image_dirt, (TILE_SIZE, TILE_SIZE))
tile_image_goo = pygame.image.load("Assets/Fondo/tileSand.png")
tile_image_goo = pygame.transform.scale(tile_image_goo, (TILE_SIZE, TILE_SIZE))

font = pygame.font.SysFont(None, 48)

def generate_random_grid(width, height):
    return [[random.randint(1, 3) for _ in range(width)] for _ in range(height)]

grid = generate_random_grid(GRID_WIDTH, GRID_HEIGHT)

player_pos = [0, 0]
ai_pos = [GRID_WIDTH - 1, GRID_HEIGHT - 1]
turno_jugador = True
esperando_ia = False
IA_DELAY = 500  # ms
last_move_time = 0
game_over = False
winner = None  # "player" o "ai"

show_start_screen = True  # Bandera para mostrar la pantalla de inicio

def draw_start_screen():
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

movs = [(-1, 0), (1, 0), (0, -1), (0, 1)]

def get_valid_moves(pos, grid, other_pos):
    moves = []
    for dx, dy in movs:
        nx, ny = pos[0] + dx, pos[1] + dy
        if (0 <= nx < GRID_WIDTH) and (0 <= ny < GRID_HEIGHT) and grid[ny][nx] > 0 and [nx, ny] != other_pos:
            moves.append((nx, ny))
    return moves


def evaluate(grid, player, ai):
    player_moves = len(get_valid_moves(player, grid, ai))
    ai_moves = len(get_valid_moves(ai, grid, player))
    return ai_moves - player_moves

def alpha_beta(grid, player, ai, depth, alpha, beta, maximizing):
    if depth == 0 or is_terminal(grid, player, ai):
        return evaluate(grid, player, ai)

    if maximizing:
        max_eval = -float('inf')
        for move in get_valid_moves(ai, grid, player):
            new_grid = [row[:] for row in grid]
            new_grid[move[1]][move[0]] -= 1
            eval = alpha_beta(new_grid, player, move, depth - 1, alpha, beta, False)
            max_eval = max(max_eval, eval)
            alpha = max(alpha, eval)
            if beta <= alpha:
                break
        return max_eval
    else:
        min_eval = float('inf')
        for move in get_valid_moves(player, grid, ai):
            new_grid = [row[:] for row in grid]
            new_grid[move[1]][move[0]] -= 1
            eval = alpha_beta(new_grid, move, ai, depth - 1, alpha, beta, True)
            min_eval = min(min_eval, eval)
            beta = min(beta, eval)
            if beta <= alpha:
                break
        return min_eval

def ai_move():
    global game_over, winner
    best_value = float('-inf')
    best_move = None
    for move in get_valid_moves(ai_pos, grid, player_pos):
        temp_grid = copy.deepcopy(grid)
        temp_grid[move[1]][move[0]] -= 1
        value = alpha_beta(temp_grid, player_pos, move, 3, -float('inf'), float('inf'), False)
        if value > best_value:
            best_value = value
            best_move = move

    if best_move:
        ai_pos[0], ai_pos[1] = best_move
        grid[best_move[1]][best_move[0]] -= 1
        if grid[best_move[1]][best_move[0]] < 0:
            winner = "player"
            game_over = True

def is_terminal(grid, player, ai):
    player_moves = get_valid_moves(player, grid, ai)
    ai_moves = get_valid_moves(ai, grid, player)
    return len(player_moves) == 0 or len(ai_moves) == 0

def draw_end_screen(result):
    screen.fill((20, 20, 20))

    title_font = pygame.font.SysFont(None, 72)
    button_font = pygame.font.SysFont(None, 36)

    if result == "player":
        text = title_font.render("¡Ganaste!", True, (0, 255, 0))
    else:
        text = title_font.render("Perdiste...", True, (255, 0, 0))

    screen.blit(text, (SCREEN_SIZE // 2 - text.get_width() // 2, SCREEN_SIZE // 2 - text.get_height() // 2 - 80))

    mouse_pos = pygame.mouse.get_pos()
    button_rect = pygame.Rect(SCREEN_SIZE // 2 - 100, SCREEN_SIZE // 2, 200, 60)
    is_hovered = button_rect.collidepoint(mouse_pos)

    shadow_rect = button_rect.copy()
    shadow_rect.x += 3
    shadow_rect.y += 3
    pygame.draw.rect(screen, (0, 0, 0), shadow_rect, border_radius=12)

    button_color = (70, 130, 255) if is_hovered else (50, 100, 200)
    pygame.draw.rect(screen, button_color, button_rect, border_radius=12)
    pygame.draw.rect(screen, (255, 255, 255), button_rect, 2, border_radius=12)

    button_text = button_font.render("Volver a jugar", True, (255, 255, 255))
    screen.blit(button_text, (button_rect.x + button_rect.width // 2 - button_text.get_width() // 2, button_rect.y + 10))

    pygame.display.flip()
    return button_rect

def draw():
    screen.fill((0, 0, 0))
    for row in range(GRID_HEIGHT):
        for col in range(GRID_WIDTH):
            if grid[row][col] > 0:
                x = col * TILE_SIZE + MARGIN
                y = row * TILE_SIZE + MARGIN
                if grid[row][col] == 1:
                    screen.blit(tile_image_dirt, (x, y))
                if grid[row][col] == 2:
                    screen.blit(tile_image_goo, (x, y))
                if grid[row][col] == 3:
                    screen.blit(tile_image_grass, (x, y))

    pygame.draw.rect(screen, (0, 0, 255), (player_pos[0] * TILE_SIZE + MARGIN, player_pos[1] * TILE_SIZE + MARGIN, TILE_SIZE, TILE_SIZE))
    pygame.draw.rect(screen, (255, 0, 0), (ai_pos[0] * TILE_SIZE + MARGIN, ai_pos[1] * TILE_SIZE + MARGIN, TILE_SIZE, TILE_SIZE))
    pygame.display.flip()

button_rect = None

# Loop principal
clock = pygame.time.Clock()
running = True
while running:
    current_time = pygame.time.get_ticks()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if show_start_screen:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if start_button and start_button.collidepoint(event.pos):
                    show_start_screen = False

        elif game_over and event.type == pygame.MOUSEBUTTONDOWN:
            if button_rect and button_rect.collidepoint(event.pos):
                grid = generate_random_grid(GRID_WIDTH, GRID_HEIGHT)
                player_pos = [0, 0]
                ai_pos = [GRID_WIDTH - 1, GRID_HEIGHT - 1]
                turno_jugador = True
                esperando_ia = False
                last_move_time = 0
                game_over = False
                winner = None
                show_start_screen = True  # Volver a la pantalla inicial después de perder o ganar

        elif not game_over and not show_start_screen and turno_jugador and event.type == pygame.KEYDOWN:
            new_x, new_y = player_pos[0], player_pos[1]
            if event.key == pygame.K_w:
                new_y -= 1
            if event.key == pygame.K_s:
                new_y += 1
            if event.key == pygame.K_a:
                new_x -= 1
            if event.key == pygame.K_d:
                new_x += 1

            if (0 <= new_x < GRID_WIDTH) and (0 <= new_y < GRID_HEIGHT) and [new_x, new_y] != ai_pos:
                player_pos = [new_x, new_y]
                grid[new_y][new_x] -= 1
                if grid[new_y][new_x] < 0:
                    winner = "ai"
                    game_over = True
                else:
                    turno_jugador = False
                    esperando_ia = True
                    last_move_time = current_time

    if show_start_screen:
        start_button = draw_start_screen()
    elif not game_over:
        if esperando_ia and current_time - last_move_time > IA_DELAY:
            if get_valid_moves(ai_pos, grid, player_pos):
                ai_move()
            else:
                winner = "player"
                game_over = True
            esperando_ia = False
            turno_jugador = True

        if is_terminal(grid, player_pos, ai_pos):
            player_moves = len(get_valid_moves(player_pos, grid, ai_pos))
            ai_moves = len(get_valid_moves(ai_pos, grid, player_pos))
            winner = "player" if player_moves > ai_moves else "ai"
            game_over = True

        draw()
        button_rect = None
    else:
        button_rect = draw_end_screen(winner)

    clock.tick(60)

pygame.quit()
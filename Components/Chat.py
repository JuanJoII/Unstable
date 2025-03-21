import pygame

# Definir constantes
TILE_SIZE = 40  # Tamaño del bloque
GRID_WIDTH = 6
GRID_HEIGHT = 6

# Crear la cuadrícula con valores de resistencia
grid = [
    [2, 2, 2, 2, 2, 2],
    [2, 1, 1, 2, 1, 2],
    [2, 1, 2, 2, 1, 2],
    [2, 2, 2, 1, 1, 2],
    [2, 1, 1, 2, 2, 2],
    [2, 2, 2, 2, 2, 2]
]

# Posición inicial del jugador
player_x = 0
player_y = 0

# Inicializar Pygame
pygame.init()
screen = pygame.display.set_mode((GRID_WIDTH * TILE_SIZE, GRID_HEIGHT * TILE_SIZE))
pygame.display.set_caption("Bloki Turn-Based Movement")

running = True

while running:
    screen.fill((0, 0, 0))  # Limpiar pantalla

    # Dibujar la cuadrícula
    for y in range(GRID_HEIGHT):
        for x in range(GRID_WIDTH):
            if grid[y][x] > 0:
                color = (0, 200, 0) if grid[y][x] == 2 else (200, 200, 0)
                pygame.draw.rect(screen, color, (x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE))
                font = pygame.font.Font(None, 30)
                text = font.render(str(grid[y][x]), True, (255, 0, 0))
                screen.blit(text, (x * TILE_SIZE + 15, y * TILE_SIZE + 10))

    # Dibujar al jugador
    pygame.draw.rect(screen, (0, 0, 255), (player_x * TILE_SIZE, player_y * TILE_SIZE, TILE_SIZE, TILE_SIZE))

    pygame.display.flip()  # Actualizar pantalla

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            new_x = player_x
            new_y = player_y

            # Movimiento por turnos
            if event.key == pygame.K_w and player_y > 0:
                new_y -= 1
            if event.key == pygame.K_s and player_y < GRID_HEIGHT - 1:
                new_y += 1
            if event.key == pygame.K_a and player_x > 0:
                new_x -= 1
            if event.key == pygame.K_d and player_x < GRID_WIDTH - 1:
                new_x += 1

            # Solo moverse si la casilla tiene un valor > 0
            if grid[new_y][new_x] > 0:
                player_x, player_y = new_x, new_y
                grid[new_y][new_x] -= 1  # Reducir resistencia de la casilla

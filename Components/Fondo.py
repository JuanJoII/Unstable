import pygame

# Inicializar pygame
pygame.init()

# Configuración de la pantalla
TILE_SIZE = 60  # Tamaño de cada tile en píxeles
GRID_SIZE = 8  # Tamaño de la cuadrícula (8x8)
MARGIN = 20  # Espacio alrededor del mapa

SCREEN_SIZE = TILE_SIZE * GRID_SIZE + 2 * MARGIN  # Ajuste por el margen
screen = pygame.display.set_mode((SCREEN_SIZE, SCREEN_SIZE))
pygame.display.set_caption("Arcade -IA Minimax")

# Cargar la imagen del tile
tile_image = pygame.image.load("Assets/Fondo/tileGrass.png") 
tile_image = pygame.transform.scale(tile_image, (TILE_SIZE, TILE_SIZE))  # Escalar

# Bucle principal
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:  # Permite cerrar la ventana con la X
            running = False

    # Dibujar el fondo con tiles
    screen.fill((0, 0, 0))  # Rellenar con negro antes de dibujar
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            x = col * TILE_SIZE + MARGIN
            y = row * TILE_SIZE + MARGIN
            screen.blit(tile_image, (x, y))

    pygame.display.flip()  # Actualizar la pantalla

pygame.quit()

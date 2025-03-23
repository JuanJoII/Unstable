import pygame
import random
from constantes import TILE_SIZE, GRID_WIDTH, GRID_HEIGHT, MARGIN


def generate_random_grid(width, height):
    return [[random.randint(1, 3) for _ in range(width)] for _ in range(height)]


pygame.init()


SCREEN_SIZE = TILE_SIZE * max(GRID_WIDTH, GRID_HEIGHT) + 2 * MARGIN
screen = pygame.display.set_mode((SCREEN_SIZE, SCREEN_SIZE))
pygame.display.set_caption("Arcade -IA Minimax")


tile_image_grass = pygame.image.load("Assets/Fondo/tileGrass.png")
tile_image_grass = pygame.transform.scale(tile_image_grass, (TILE_SIZE, TILE_SIZE))

tile_image_dirt = pygame.image.load("Assets/Fondo/tileDirt.png")
tile_image_dirt = pygame.transform.scale(tile_image_dirt, (TILE_SIZE, TILE_SIZE))

tile_image_goo = pygame.image.load("Assets/Fondo/tileGoo.png")
tile_image_goo = pygame.transform.scale(tile_image_goo, (TILE_SIZE, TILE_SIZE))

grid = generate_random_grid(GRID_WIDTH, GRID_HEIGHT)


player_x = 0
player_y = 0


running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            new_x = player_x
            new_y = player_y

           
            if event.key == pygame.K_w and player_y > 0:
                new_y -= 1
            if event.key == pygame.K_s and player_y < GRID_HEIGHT - 1:
                new_y += 1
            if event.key == pygame.K_a and player_x > 0:
                new_x -= 1
            if event.key == pygame.K_d and player_x < GRID_WIDTH - 1:
                new_x += 1

            
            if grid[new_y][new_x] > 0:
                player_x, player_y = new_x, new_y
                grid[new_y][new_x] -= 1 

    
    screen.fill((0, 0, 0))  
    for row in range(GRID_HEIGHT):
        for col in range(GRID_WIDTH):
           
            if grid[row][col] > 0:
                x = col * TILE_SIZE + MARGIN
                y = row * TILE_SIZE + MARGIN
               
                if grid[row][col] == 1:
                    screen.blit(tile_image_dirt, (x, y))
                if grid[row][col] == 2:
                    screen.blit(tile_image_grass, (x, y))
                if grid[row][col] == 3:
                    screen.blit(tile_image_goo, (x, y))

    
    pygame.draw.rect(screen, (0, 0, 255), (player_x * TILE_SIZE + MARGIN, player_y * TILE_SIZE + MARGIN, TILE_SIZE, TILE_SIZE))

    pygame.display.flip()  

pygame.quit()
import pygame
from constantes import TILE_SIZE, GRID_WIDTH, GRID_HEIGHT, MARGIN, SCREEN_SIZE

class GameScreen:
    def __init__(self):
        self.tile_images = {
            1: self._load_image("Assets/Fondo/tileDirt.png"),
            2: self._load_image("Assets/Fondo/tileSand.png"),
            3: self._load_image("Assets/Fondo/tileGrass.png")
        }
    
    def _load_image(self, path):
        image = pygame.image.load(path)
        return pygame.transform.scale(image, (TILE_SIZE, TILE_SIZE))
    
    def draw(self, screen, grid, player, ai, coins, coins_count, score):
        screen.fill((0, 0, 0))
        for row in range(GRID_HEIGHT):
            for col in range(GRID_WIDTH):
                if grid[row][col] > 0:
                    x = col * TILE_SIZE + MARGIN
                    y = row * TILE_SIZE + MARGIN
                    screen.blit(self.tile_images[grid[row][col]], (x, y))
        
        font = pygame.font.SysFont("Arial", 24)
        coins_text = font.render(f"Monedas: {coins_count}", True, (255, 255, 0))
        screen.blit(coins_text, (10, 10))
        
        score_text = font.render(f"Score: {score}", True, (255, 255, 0))
        score_text_width = score_text.get_width()
        screen_width = SCREEN_SIZE
        screen.blit(score_text, (screen_width - score_text_width - 10, 10)) 
        
        player.draw(screen, TILE_SIZE, MARGIN)
        ai.draw(screen, TILE_SIZE, MARGIN)
        for coin in coins:
            if not coin.collected:
                coin.draw(screen, TILE_SIZE, MARGIN)
        pygame.display.flip()
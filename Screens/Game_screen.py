import pygame
from constantes import TILE_SIZE, GRID_WIDTH, GRID_HEIGHT, MARGIN, SCREEN_SIZE

class GameScreen:
    def __init__(self):
        self.tile_images = {
            1: self._load_image("Assets/Fondo/tileDirt.png"),
            2: self._load_image("Assets/Fondo/tileSand.png"),
            3: self._load_image("Assets/Fondo/tileGrass.png")
        }
        # Cargar fuente personalizada
        self.font = pygame.font.Font("Assets/UI/PressStart2P.ttf", 16)
        # Cargar iconos
        self.coin_icon = pygame.image.load("Assets/UI/CoinBG.png").convert_alpha()
        self.coin_icon = pygame.transform.scale(self.coin_icon, (24, 24))
        self.score_icon = pygame.image.load("Assets/UI/Star.png").convert_alpha()
        self.score_icon = pygame.transform.scale(self.score_icon, (24, 24))

        #Cargar musica
        pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=512)
        
        # Cargar música
        self.music_loaded = False
        try:
            pygame.mixer.music.load('Assets/Sounds/bg_song.mp3')
            pygame.mixer.music.set_volume(0.2)  # Volumen
            self.music_loaded = True
        except Exception as e:
            print(f"Error cargando música: {e}")
            
        # Crear superficies semitransparentes para los contadores
        self.info_panel = pygame.Surface((SCREEN_SIZE, 40), pygame.SRCALPHA)
        self.info_panel.fill((0, 0, 0, 128))  # Fondo negro semitransparente

    def start_music(self):
        """Reproduce la música de fondo en loop"""
        if self.music_loaded and not pygame.mixer.music.get_busy():
            pygame.mixer.music.play(-1)  # -1 para loop infinito
            print("Música iniciada")  # Debug
    
    def stop_music(self):
        """Detiene la música"""
        pygame.mixer.music.stop()
    
    def _load_image(self, path):
        image = pygame.image.load(path)
        return pygame.transform.scale(image, (TILE_SIZE, TILE_SIZE))
    
    def draw(self, screen, grid, player, ai, coins, coins_count, score):
        screen.fill((0, 0, 0))
        
        # Dibujar el grid
        for row in range(GRID_HEIGHT):
            for col in range(GRID_WIDTH):
                if grid[row][col] > 0:
                    x = col * TILE_SIZE + MARGIN
                    y = row * TILE_SIZE + MARGIN
                    screen.blit(self.tile_images[grid[row][col]], (x, y))
        
        # Dibujar panel de información
        screen.blit(self.info_panel, (0, 0))
        
        # Dibujar monedas con icono
        coins_text = self.font.render(f"{coins_count}", True, (255, 255, 0))
        screen.blit(self.coin_icon, (15, 8))
        screen.blit(coins_text, (45, 10))
        
        # Dibujar score con icono
        score_text = self.font.render(f"{score}", True, (255, 215, 0)) 
        score_text_width = score_text.get_width()
        screen.blit(self.score_icon, (SCREEN_SIZE - score_text_width - 40, 8))
        screen.blit(score_text, (SCREEN_SIZE - score_text_width - 10, 10))
        
        # Dibujar elementos del juego
        player.draw(screen, TILE_SIZE, MARGIN)
        ai.draw(screen, TILE_SIZE, MARGIN)
        for coin in coins:
            if not coin.collected:
                coin.draw(screen, TILE_SIZE, MARGIN)
        
        pygame.display.flip()
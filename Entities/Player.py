import pygame

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()  # ¡Importante! Llama al constructor de la clase Sprite.
        self.x = x
        self.y = y
        self.color = (0, 0, 255)  
        
        # Carga de sprites con manejo de errores
        self.sprites = []
        try:
            self.sprites = [
                pygame.image.load('Assets/Base Character/Frog/frogidle_1.png').convert_alpha(),
                pygame.image.load('Assets/Base Character/Frog/frogidle_2.png').convert_alpha(),
                pygame.image.load('Assets/Base Character/Frog/frogidle_3.png').convert_alpha(),
                pygame.image.load('Assets/Base Character/Frog/frogidle_4.png').convert_alpha()
            ]
        except pygame.error as e:
            print(f"Error cargando sprites: {e}")
            # Si falla, crea un placeholder (opcional)
            self.sprites = [pygame.Surface((32, 32), pygame.SRCALPHA)]
        
        self.current_sprite = 0
        self.image = self.sprites[int(self.current_sprite)]
        self.rect = self.image.get_rect(center=(x, y))
        self.animation_speed = 0.15  # Ajustado para mejor visualización
    
    @property
    def pos(self):
        return [self.x, self.y]
    
    def move(self, dx, dy, grid, ai_pos, grid_width, grid_height):
        new_x, new_y = self.x + dx, self.y + dy
        if (0 <= new_x < grid_width) and (0 <= new_y < grid_height) and [new_x, new_y] != ai_pos:
            self.x, self.y = new_x, new_y
            grid[new_y][new_x] -= 1
            self.rect.center = (self.x * self.tile_size + self.margin + self.tile_size//2, 
                                self.y * self.tile_size + self.margin + self.tile_size//2)
            return True
        return False
    
    def update(self):
        # Actualiza la animación
        self.current_sprite += self.animation_speed
        if self.current_sprite >= len(self.sprites):
            self.current_sprite = 0
        self.image = self.sprites[int(self.current_sprite)]
        
        # Actualiza la posición del rect (opcional, si no usas draw)
        # self.rect.center = (self.x * self.tile_size + self.margin + self.tile_size//2, 
        #                     self.y * self.tile_size + self.margin + self.tile_size//2)
    
    def draw(self, screen, tile_size, margin):
        self.tile_size = tile_size
        self.margin = margin
        self.rect.center = (self.x * tile_size + margin + tile_size//2, 
                            self.y * tile_size + margin + tile_size//2)
        screen.blit(self.image, self.rect)
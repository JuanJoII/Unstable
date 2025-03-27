import pygame
from constantes import CHARACTER_SCALE

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):  # Añade parámetro de escala
        super().__init__()
        self.x = x
        self.y = y
        self.color = (0, 0, 255)
        self.sprite_scale = CHARACTER_SCALE   # Factor de escalado (1.0 = tamaño original)
        
        # Carga y escala los sprites
        self.original_sprites = self._load_sprites()
        self.sprites = self._scale_sprites(self.original_sprites)
        
        self.current_sprite = 0
        self.image = self.sprites[int(self.current_sprite)]
        self.rect = self.image.get_rect(center=(x, y))
        self.animation_speed = 0.15
        self.tile_size = 0  # Se establecerá en draw()
        self.margin = 0
    
    def _load_sprites(self):
        """Carga los sprites originales"""
        sprite_paths = [
            'Assets/Base Character/Frog/frogidle_1.png',
            'Assets/Base Character/Frog/frogidle_2.png',
            'Assets/Base Character/Frog/frogidle_3.png',
            'Assets/Base Character/Frog/frogidle_4.png'
        ]
        
        loaded = []
        for path in sprite_paths:
            try:
                loaded.append(pygame.image.load(path).convert_alpha())
            except pygame.error as e:
                print(f"Error cargando sprite {path}: {e}")
                # Crea un placeholder si falla
                placeholder = pygame.Surface((32, 32), pygame.SRCALPHA)
                placeholder.fill((0, 0, 255, 128))  # Azul semitransparente
                loaded.append(placeholder)
        
        return loaded
    
    def _scale_sprites(self, sprites):
        """Escala todos los sprites según el factor"""
        scaled = []
        for sprite in sprites:
            new_width = int(sprite.get_width() * self.sprite_scale)
            new_height = int(sprite.get_height() * self.sprite_scale)
            scaled.append(pygame.transform.smoothscale(sprite, (new_width, new_height)))
        return scaled
    
    def set_scale(self, new_scale):
        """Cambia el tamaño dinámicamente"""
        self.sprite_scale = new_scale
        self.sprites = self._scale_sprites(self.original_sprites)
        # Ajusta el rectángulo para mantener la posición
        self.image = self.sprites[int(self.current_sprite)]
        self.rect = self.image.get_rect(center=self.rect.center)
    
    @property
    def pos(self):
        return [self.x, self.y]
    
    def move(self, dx, dy, grid, ai_pos, grid_width, grid_height):
        new_x, new_y = self.x + dx, self.y + dy
        
        if not (0 <= new_x < grid_width and 0 <= new_y < grid_height):
            return False
        if [new_x, new_y] == ai_pos:
            return False
        
        grid[self.y][self.x] -= 1
        
        self.x, self.y = new_x, new_y
        

        self.rect.center = (
            self.x * self.tile_size + self.margin + self.tile_size//2, 
            self.y * self.tile_size + self.margin + self.tile_size//2
        )
        
        return True
    
    def update(self):
        self.current_sprite += self.animation_speed
        if self.current_sprite >= len(self.sprites):
            self.current_sprite = 0
        self.image = self.sprites[int(self.current_sprite)]
    
    def draw(self, screen, tile_size, margin):
        self.tile_size = tile_size
        self.margin = margin
        self.rect.center = (self.x * tile_size + margin + tile_size//2,
                           self.y * tile_size + margin + tile_size//2)
        screen.blit(self.image, self.rect)
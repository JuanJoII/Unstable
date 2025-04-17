import pygame
from constantes import CHARACTER_SCALE

class Coin(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.x = x
        self.y = y
        self.sprite_scale = CHARACTER_SCALE
        self.collected = False
        

        self.original_sprites = self._load_sprites()
        self.sprites = self._scale_sprites(self.original_sprites)
        

        self.current_sprite = 0
        self.image = self.sprites[int(self.current_sprite)]
        self.rect = self.image.get_rect(center=(x, y))
        self.animation_speed = 0.12
        self.tile_size = 0
        self.margin = 0
    
    def _load_sprites(self):
        sprite_paths = [
            'Assets\SpritesAnimacion\spinning_coin\coin1.png',
            'Assets\SpritesAnimacion\spinning_coin\coin2.png',
            'Assets\SpritesAnimacion\spinning_coin\coin3.png',
            'Assets\SpritesAnimacion\spinning_coin\coin4.png',
            'Assets\SpritesAnimacion\spinning_coin\coin5.png',
            'Assets\SpritesAnimacion\spinning_coin\coin6.png',
            'Assets\SpritesAnimacion\spinning_coin\coin7.png',
            'Assets\SpritesAnimacion\spinning_coin\coin8.png',
            'Assets\SpritesAnimacion\spinning_coin\coin9.png',
            'Assets\SpritesAnimacion\spinning_coin\coin10.png',
        ]
        
        loaded = []
        for path in sprite_paths:
            try:
                loaded.append(pygame.image.load(path).convert_alpha())
            except pygame.error as e:
                print(f"Error cargando sprite {path}: {e}")
                placeholder = pygame.Surface((16, 16), pygame.SRCALPHA)
                placeholder.fill((255, 255, 0, 128))  # Amarillo semitransparente como placeholder
                loaded.append(placeholder)
        
        return loaded
    
    def _scale_sprites(self, sprites):
        scaled = []
        for sprite in sprites:
            new_width = int(sprite.get_width() * self.sprite_scale)
            new_height = int(sprite.get_height() * self.sprite_scale)
            scaled.append(pygame.transform.smoothscale(sprite, (new_width, new_height)))
        return scaled
    
    def set_scale(self, new_scale):
        self.sprite_scale = new_scale
        self.sprites = self._scale_sprites(self.original_sprites)
        self.image = self.sprites[int(self.current_sprite)]
        self.rect = self.image.get_rect(center=self.rect.center)
    
    @property
    def pos(self):
        return [self.x, self.y]
    
    def update(self):
        if not self.collected:
            self.current_sprite += self.animation_speed
            if self.current_sprite >= len(self.sprites):
                self.current_sprite = 0
            self.image = self.sprites[int(self.current_sprite)]
    
    def draw(self, screen, tile_size, margin):
        if not self.collected:
            self.tile_size = tile_size
            self.margin = margin
            self.rect.center = (self.x * tile_size + margin + tile_size//2,
                               self.y * tile_size + margin + tile_size//2)
            screen.blit(self.image, self.rect)
    
    def check_collision(self, player_pos):
        if not self.collected and self.pos == player_pos:
            self.collected = True
            return True
        return False
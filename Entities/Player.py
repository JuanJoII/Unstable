import pygame
from constantes import CHARACTER_SCALE

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, sombrero_actual=None): 
        super().__init__()
        self.x = x
        self.y = y
        self.color = (0, 0, 255)
        self.sprite_scale = CHARACTER_SCALE 
        self.hat_scale = 0.15
        
        # Atributos para el sombrero
        self.sombrero_actual = sombrero_actual
        self.hat_img = None
        self.hat_offset = (0, -15)  # Ajuste de posición del sombrero
        
        self.original_sprites = self._load_sprites()
        self.sprites = self._scale_sprites(self.original_sprites)
        
        self.current_sprite = 0
        self.image = self.sprites[int(self.current_sprite)]
        self.rect = self.image.get_rect(center=(x, y))
        self.animation_speed = 0.15
        self.tile_size = 0 
        self.margin = 0
        
        # Cargar el sombrero si hay uno equipado
        if self.sombrero_actual:
            self.cargar_sombrero(self.sombrero_actual)
    
    def cargar_sombrero(self, nombre_sombrero):
        """Carga la imagen del sombrero basado en el nombre"""
        # Lista de sombreros disponibles (debería coincidir con la de la tienda)
        hats = [
        {"nombre": "Sombrero Azul", "imagen": "Assets/Hats/hat_blue.png", "precio": 5},
        {"nombre": "Sombrero Rojo", "imagen": "Assets/Hats/hat_red.png", "precio": 8},
        {"nombre": "Sombrero Dorado", "imagen": "Assets/Hats/hat_purple.png", "precio": 15},
        {"nombre": "Sombrero Green", "imagen": "Assets/Hats/hat_green.png", "precio": 20},
        {"nombre": "Sombrero One Pi", "imagen": "Assets/Hats/hat_onepi.png", "precio": 28},
        {"nombre": "Sombrero Crown", "imagen": "Assets/Hats/hat_crown.png", "precio": 36},
        ]
        
        # Buscar el sombrero en la lista
        for hat in hats:
            if hat["nombre"] == nombre_sombrero:
                try:
                    self.hat_img = pygame.image.load(hat["imagen"]).convert_alpha()
                    # Escalar el sombrero proporcionalmente al tamaño del personaje
                    new_width = int(self.hat_img.get_width() * self.hat_scale)
                    new_height = int(self.hat_img.get_height() * self.hat_scale)
                    self.hat_img = pygame.transform.smoothscale(self.hat_img, (new_width, new_height))
                    self.sombrero_actual = nombre_sombrero
                    return True
                except pygame.error as e:
                    print(f"Error cargando sombrero {hat['imagen']}: {e}")
                    self.hat_img = None
                    return False
        
        # Si no se encuentra el sombrero
        self.hat_img = None
        return False
    
    def equipar_sombrero(self, nombre_sombrero):
        """Equipa un nuevo sombrero"""
        self.sombrero_actual = nombre_sombrero
        self.cargar_sombrero(nombre_sombrero)
    
    def quitar_sombrero(self):
        """Quita el sombrero actual"""
        self.sombrero_actual = None
        self.hat_img = None
    
    def _load_sprites(self):
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
                placeholder = pygame.Surface((32, 32), pygame.SRCALPHA)
                placeholder.fill((0, 0, 255, 128)) 
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
        
        # Re-escalar el sombrero si hay uno equipado
        if self.sombrero_actual:
            self.cargar_sombrero(self.sombrero_actual)
    
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
        
        # Dibujar al personaje
        screen.blit(self.image, self.rect)
        
        # Dibujar el sombrero si hay uno equipado
        if self.hat_img:
            hat_pos = (
                self.rect.centerx + self.hat_offset[0] - self.hat_img.get_width() // 2,
                self.rect.centery + self.hat_offset[1] - self.hat_img.get_height() // 2
            )
            screen.blit(self.hat_img, hat_pos)
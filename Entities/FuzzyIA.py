import math
import pygame
from Entities.Grid import get_valid_moves
from Entities.AI_Diffuse_Controller import FuzzController
from constantes import CHARACTER_SCALE

class FuzzyAI(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.x = x
        self.y = y
        self.color = (0, 255, 0)  # Verde para distinguir de la otra IA
        self.sprite_scale = CHARACTER_SCALE  # Asume que CHARACTER_SCALE está definido
        self.coins_collected = 0
        
        # Inicialización de sprites (similar a tu clase AI)
        self.original_sprites = self._load_sprites()
        self.sprites = self._scale_sprites(self.original_sprites)
        
        self.current_sprite = 0
        self.image = self.sprites[self.current_sprite]
        self.rect = self.image.get_rect(center=(x, y))
        self.animation_speed = 0.1
        self.tile_size = 0  
        self.margin = 0
        
        # Controlador de lógica difusa
        self.fuzzy = FuzzController()
    
    def _load_sprites(self):
        # Implementación similar a tu clase AI
        sprite_paths = [
            'Assets/Base Character/Frog/Enemyfrogidle_1.png',
            'Assets/Base Character/Frog/Enemyfrogidle_2.png',
            'Assets/Base Character/Frog/Enemyfrogidle_3.png',
            'Assets/Base Character/Frog/Enemyfrogidle_4.png'
        ]
        
        loaded = []
        for path in sprite_paths:
            try:
                loaded.append(pygame.image.load(path).convert_alpha())
            except pygame.error as e:
                print(f"Error cargando sprite {path}: {e}")
                placeholder = pygame.Surface((32, 32), pygame.SRCALPHA)
                placeholder.fill((0, 255, 0, 128))  # Verde semitransparente
                loaded.append(placeholder)
        
        return loaded
    
    def _scale_sprites(self, sprites):
        # Implementación similar a tu clase AI
        scaled = []
        for sprite in sprites:
            new_width = int(sprite.get_width() * self.sprite_scale)
            new_height = int(sprite.get_height() * self.sprite_scale)
            scaled.append(pygame.transform.smoothscale(sprite, (new_width, new_height)))
        return scaled
    
    @property
    def pos(self):
        return [self.x, self.y]
    
    def move(self, dx, dy, grid, player_pos, grid_width, grid_height, coins_group=None):
        # Implementación similar a tu clase AI
        new_x, new_y = self.x + dx, self.y + dy
        
        if not (0 <= new_x < grid_width and 0 <= new_y < grid_height):
            return False
        if [new_x, new_y] == player_pos:
            return False
        
        grid[self.y][self.x] -= 1
        
        self.x, self.y = new_x, new_y
        
        self.rect.center = (
            self.x * self.tile_size + self.margin + self.tile_size//2, 
            self.y * self.tile_size + self.margin + self.tile_size//2
        )
        
        # Verificar colisión con monedas
        if coins_group:
            for coin in list(coins_group):
                if not coin.collected and (self.x, self.y) == (coin.x, coin.y):
                    coin.collected = True
                    self.coins_collected += 1
                    print(f"IA Difusa recogió moneda! Total: {self.coins_collected}")
        
        return True
    
    def _normalize_distance(self, distance, max_distance=10):
        """Normaliza la distancia a escala 0-10"""
        return min(10, max(0, (distance / max_distance) * 10))
    
    def _calculate_risk(self, move, player_pos, grid_width, grid_height):
        """Calcula el riesgo de un movimiento (0-10)"""
        # Ejemplo simple: riesgo aumenta cuanto más cerca está del jugador
        dist_to_player = math.sqrt((move[0]-player_pos[0])**2 + (move[1]-player_pos[1])**2)
        max_possible_dist = math.sqrt(grid_width**2 + grid_height**2)
        risk = 10 - self._normalize_distance(dist_to_player, max_possible_dist)
        return risk
    
    def _find_closest_coin(self, move, coins_group):
        """Encuentra la distancia a la moneda más cercana"""
        if not coins_group:
            return float('inf')
            
        min_dist = float('inf')
        for coin in coins_group:
            if not coin.collected:
                dist = math.sqrt((move[0]-coin.x)**2 + (move[1]-coin.y)**2)
                if dist < min_dist:
                    min_dist = dist
        return min_dist
    
    def evaluate_move(self, move, grid, player_pos, grid_width, grid_height, coins_group=None):
        """Evalúa un movimiento usando lógica difusa"""
        # Calcular métricas
        risk = self._calculate_risk(move, player_pos, grid_width, grid_height)
        
        dist_to_player = math.sqrt((move[0]-player_pos[0])**2 + (move[1]-player_pos[1])**2)
        norm_dist_player = self._normalize_distance(dist_to_player, grid_width + grid_height)
        
        dist_to_coin = self._find_closest_coin(move, coins_group)
        norm_dist_coin = self._normalize_distance(dist_to_coin, grid_width + grid_height) if dist_to_coin != float('inf') else 10
        
        # Obtener prioridad del sistema difuso
        priority = self.fuzzy.calcular_prioridad(
            riesgo_val=risk,
            distancia_jugador=norm_dist_player,
            distancia_moneda=norm_dist_coin
        )
        
        return priority
    
    def make_move(self, grid, player_pos, grid_width, grid_height, coins_group=None):
        """Toma una decisión de movimiento usando lógica difusa"""
        valid_moves = get_valid_moves(self.pos, grid, player_pos, grid_width, grid_height)
        if not valid_moves:
            return False
        
        # Evaluar cada movimiento posible
        best_move = None
        best_score = -1
        
        for move in valid_moves:
            # Evaluación con lógica difusa
            score = self.evaluate_move(move, grid, player_pos, grid_width, grid_height, coins_group)
            
            # Bonus adicional si este movimiento recoge una moneda
            if coins_group:
                for coin in coins_group:
                    if not coin.collected and (move[0], move[1]) == (coin.x, coin.y):
                        score += 3  # Bonus por recoger moneda
            
            if score > best_score:
                best_score = score
                best_move = move
        
        # Ejecutar el mejor movimiento encontrado
        if best_move:
            dx = best_move[0] - self.x
            dy = best_move[1] - self.y
            success = self.move(dx, dy, grid, player_pos, grid_width, grid_height, coins_group)
            return success
        return False
    
    def update(self):
        """Actualiza la animación"""
        self.current_sprite += self.animation_speed
        if self.current_sprite >= len(self.sprites):
            self.current_sprite = 0
        self.image = self.sprites[int(self.current_sprite)]
        
    def draw(self, screen, tile_size, margin):
        """Dibuja el sprite"""
        self.tile_size = tile_size
        self.margin = margin
        self.rect.center = (self.x * tile_size + margin + tile_size//2, 
                           self.y * tile_size + margin + tile_size//2)
        screen.blit(self.image, self.rect)
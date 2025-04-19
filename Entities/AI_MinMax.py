import copy
import pygame
from Entities.Grid import get_valid_moves
from constantes import CHARACTER_SCALE

class AI(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.x = x
        self.y = y
        self.color = (255, 0, 0) 
        self.sprite_scale = CHARACTER_SCALE
        self.coins_collected = 0
        
        self.original_sprites = self._load_sprites()
        self.sprites = self._scale_sprites(self.original_sprites)
        
        self.current_sprite = 0
        self.image = self.sprites[self.current_sprite]
        self.rect = self.image.get_rect(center=(x, y))
        self.animation_speed = 0.1
        self.tile_size = 0  
        self.margin = 0
    
    def _load_sprites(self):
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
                placeholder.fill((255, 0, 0, 128)) 
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
    

    def move(self, dx, dy, grid, player_pos, grid_width, grid_height, coins_group=None):
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
                    print(f"IA recogió moneda! Total: {self.coins_collected}")
        
        return True
    
    def _is_terminal(self, grid, player_pos, grid_width, grid_height):
        player_moves = get_valid_moves(player_pos, grid, self.pos, grid_width, grid_height)
        ai_moves = get_valid_moves(self.pos, grid, player_pos, grid_width, grid_height)
        return len(player_moves) == 0 or len(ai_moves) == 0
    
    def evaluate(self, grid, player_pos, grid_width, grid_height, coins_group=None):
        player_moves = len(get_valid_moves(player_pos, grid, self.pos, grid_width, grid_height))
        ai_moves = len(get_valid_moves(self.pos, grid, player_pos, grid_width, grid_height))
        
        # Valor base basado en movilidad
        score = ai_moves - player_moves
        
        # Si hay monedas, añadimos incentivo para recogerlas
        if coins_group:
            closest_coin_dist = float('inf')
            for coin in coins_group:
                if not coin.collected:
                    dist = abs(self.x - coin.x) + abs(self.y - coin.y)
                    if dist < closest_coin_dist:
                        closest_coin_dist = dist
            
            if closest_coin_dist != float('inf'):
                score += 10.0 / (closest_coin_dist + 1)
        
        return score

    def alpha_beta(self, grid, player_pos, depth, alpha, beta, maximizing, grid_width, grid_height, coins_group=None):
        if depth == 0 or self._is_terminal(grid, player_pos, grid_width, grid_height):
            return self.evaluate(grid, player_pos, grid_width, grid_height, coins_group)

        if maximizing:
            max_eval = -float('inf')
            for move in get_valid_moves(self.pos, grid, player_pos, grid_width, grid_height):
                new_grid = [row[:] for row in grid]
                new_grid[move[1]][move[0]] -= 1
                eval = self.alpha_beta(new_grid, player_pos, depth - 1, alpha, beta, False, grid_width, grid_height, coins_group)
                max_eval = max(max_eval, eval)
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break
            return max_eval
        else:
            min_eval = float('inf')
            for move in get_valid_moves(player_pos, grid, self.pos, grid_width, grid_height):
                new_grid = [row[:] for row in grid]
                new_grid[move[1]][move[0]] -= 1
                eval = self.alpha_beta(new_grid, move, depth - 1, alpha, beta, True, grid_width, grid_height, coins_group)
                min_eval = min(min_eval, eval)
                beta = min(beta, eval)
                if beta <= alpha:
                    break
            return min_eval

    def make_move(self, grid, player_pos, grid_width, grid_height, coins_group=None):
        best_value = float('-inf')
        best_move = None
        
        for move in get_valid_moves(self.pos, grid, player_pos, grid_width, grid_height):
            temp_grid = copy.deepcopy(grid)
            temp_grid[move[1]][move[0]] -= 1
            value = self.alpha_beta(temp_grid, player_pos, 3, -float('inf'), float('inf'), False, grid_width, grid_height, coins_group)
            
            if coins_group:
                for coin in coins_group:
                    if not coin.collected and (move[0], move[1]) == (coin.x, coin.y):
                        value += 5
            
            if value > best_value:
                best_value = value
                best_move = move

        if best_move:
            dx = best_move[0] - self.x
            dy = best_move[1] - self.y
            success = self.move(dx, dy, grid, player_pos, grid_width, grid_height, coins_group)
            return success and grid[best_move[1]][best_move[0]] < 0
        return False

    def make_move(self, grid, player_pos, grid_width, grid_height, coins_group=None):
        best_value = float('-inf')
        best_move = None
        
        for move in get_valid_moves(self.pos, grid, player_pos, grid_width, grid_height):
            temp_grid = copy.deepcopy(grid)
            temp_grid[move[1]][move[0]] -= 1
            value = self.alpha_beta(temp_grid, player_pos, 3, -float('inf'), float('inf'), False, grid_width, grid_height, coins_group)
            
            # Bonus adicional si este movimiento recoge una moneda
            if coins_group:
                for coin in coins_group:
                    if not coin.collected and (move[0], move[1]) == (coin.x, coin.y):
                        value += 5  # Bonus por recoger moneda
            
            if value > best_value:
                best_value = value
                best_move = move

        if best_move:
            dx = best_move[0] - self.x
            dy = best_move[1] - self.y
            success = self.move(dx, dy, grid, player_pos, grid_width, grid_height, coins_group)
            return success and grid[best_move[1]][best_move[0]] < 0
        return False
    
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
import copy
import pygame
import math
from Entities.Grid import get_valid_moves
from constantes import CHARACTER_SCALE, GRID_WIDTH, GRID_HEIGHT

class AI(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.x = x
        self.y = y
        self.color = (255, 0, 0) 
        self.sprite_scale = CHARACTER_SCALE
        self.coins_collected = 0
        
        # Estados del juego para comportamiento adaptativo
        self.game_phase = "early"  # early, mid, late
        self.turns_played = 0
        self.player_aggressive = False
        self.last_player_positions = []  # Para rastrear movimientos del jugador
        
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
    
    def _update_game_phase(self, grid):
        # Actualiza la fase del juego basado en el estado del tablero
        self.turns_played += 1
        
        # Contar casillas estables e inestables
        total_cells = GRID_WIDTH * GRID_HEIGHT
        unstable_cells = sum(1 for row in grid for cell in row if cell <= 0)
        stable_cells = total_cells - unstable_cells
        stability_ratio = stable_cells / total_cells if total_cells > 0 else 0
        
        # Determinar fase del juego
        if self.turns_played < 5 or stability_ratio > 0.8:
            self.game_phase = "early"
        elif stability_ratio > 0.4 or self.turns_played < 15:
            self.game_phase = "mid"
        else:
            self.game_phase = "late"
            
        # Detectar si el jugador está siendo agresivo (acercándose a la IA)
        if len(self.last_player_positions) >= 3:
            distances = [abs(pos[0] - self.x) + abs(pos[1] - self.y) for pos in self.last_player_positions[-3:]]
            if all(distances[i] < distances[i+1] for i in range(len(distances)-1)):
                self.player_aggressive = True
            else:
                self.player_aggressive = False

    def move(self, dx, dy, grid, player_pos, grid_width, grid_height, coins_group=None):
        new_x, new_y = self.x + dx, self.y + dy
        
        if not (0 <= new_x < grid_width and 0 <= new_y < grid_height):
            return False
        if [new_x, new_y] == player_pos:
            return False
        
        # Reducir la estabilidad de la casilla actual
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
    
    def _cell_stability(self, grid, x, y):
        """Evalúa qué tan estable es una celda (valores más altos son mejores)"""
        if not (0 <= x < len(grid[0]) and 0 <= y < len(grid)):
            return -100  # Fuera del tablero
        
        stability = grid[y][x]
        if stability <= 0:
            return -50  # Casilla inestable
        return stability
    
    def _trap_potential(self, grid, position, opponent_pos, grid_width, grid_height):
        """Evalúa el potencial para atrapar al oponente"""
        x, y = position
        moves = get_valid_moves(position, grid, opponent_pos, grid_width, grid_height)
        if not moves:
            return 100  # El oponente está atrapado
            
        # Calcula cuántas casillas alrededor del oponente son inestables
        opponent_x, opponent_y = opponent_pos
        adjacent_cells = [
            (opponent_x+1, opponent_y), (opponent_x-1, opponent_y),
            (opponent_x, opponent_y+1), (opponent_x, opponent_y-1)
        ]
        
        unstable_adjacent = 0
        for ax, ay in adjacent_cells:
            if not (0 <= ax < grid_width and 0 <= ay < grid_height):
                unstable_adjacent += 1
            elif grid[ay][ax] <= 1:  # Inestable o casi inestable
                unstable_adjacent += 1
                
        return unstable_adjacent * 5
    
    def _control_center(self, position, grid_width, grid_height):
        """Bonificación por estar cerca del centro del tablero"""
        center_x = grid_width / 2
        center_y = grid_height / 2
        distance_to_center = abs(position[0] - center_x) + abs(position[1] - center_y)
        max_distance = center_x + center_y
        
        # Normalizado entre 0 y 10
        return 10 * (1 - distance_to_center / max_distance)
    
    def _coin_value(self, grid, position, coins_group, opponent_pos):
        """Evalúa el valor de ir por monedas"""
        if not coins_group:
            return 0
            
        # Encuentra la moneda más cercana no recogida
        closest_coin_dist = float('inf')
        opponent_coin_dist = float('inf')
        
        for coin in coins_group:
            if not coin.collected:
                # Distancia de la IA a la moneda
                ai_dist = abs(position[0] - coin.x) + abs(position[1] - coin.y)
                if ai_dist < closest_coin_dist:
                    closest_coin_dist = ai_dist
                
                # Distancia del oponente a la moneda
                player_dist = abs(opponent_pos[0] - coin.x) + abs(opponent_pos[1] - coin.y)
                if player_dist < opponent_coin_dist:
                    opponent_coin_dist = player_dist
        
        if closest_coin_dist == float('inf'):
            return 0
            
        # Si estamos en la misma casilla que una moneda, alto valor
        if closest_coin_dist == 0:
            return 50
            
        # Si estamos más cerca que el oponente, más valor
        if closest_coin_dist < opponent_coin_dist:
            return 30 / (closest_coin_dist + 1)
        else:
            return 15 / (closest_coin_dist + 1)
    
    def _path_safety(self, grid, from_pos, to_pos):
        """Evalúa la seguridad del camino entre dos posiciones"""
        # Implementación simple: promedio de estabilidad en línea recta
        x1, y1 = from_pos
        x2, y2 = to_pos
        
        points = []
        dx = abs(x2 - x1)
        dy = abs(y2 - y1)
        sx = 1 if x1 < x2 else -1
        sy = 1 if y1 < y2 else -1
        err = dx - dy
        
        while True:
            points.append((x1, y1))
            if x1 == x2 and y1 == y2:
                break
            e2 = 2 * err
            if e2 > -dy:
                err -= dy
                x1 += sx
            if e2 < dx:
                err += dx
                y1 += sy
        
        # Calcula la estabilidad promedio del camino
        if not points:
            return 0
        
        stability_sum = sum(self._cell_stability(grid, x, y) for x, y in points)
        return stability_sum / len(points)
    
    def _mobility_score(self, my_moves, opponent_moves):
        """Evalúa la movilidad relativa"""
        if opponent_moves == 0:
            return 100  # Victoria
        if my_moves == 0:
            return -100  # Derrota
            
        mobility_ratio = my_moves / (my_moves + opponent_moves)
        return (mobility_ratio - 0.5) * 40  # Normalizado entre -20 y 20
    
    def evaluate(self, grid, player_pos, grid_width, grid_height, coins_group=None, depth=0):
        """Función de evaluación mejorada con múltiples heurísticas"""
        ai_moves = get_valid_moves(self.pos, grid, player_pos, grid_width, grid_height)
        player_moves = get_valid_moves(player_pos, grid, self.pos, grid_width, grid_height)
        
        if not player_moves:
            return 1000 + depth  # Victoria, preferimos victorias más rápidas
        if not ai_moves:
            return -1000 - depth  # Derrota, preferimos derrotas más lentas
        
        # 1. Movilidad
        mobility = self._mobility_score(len(ai_moves), len(player_moves))
        
        # 2. Estabilidad de la casilla actual
        current_stability = self._cell_stability(grid, self.pos[0], self.pos[1])
        
        # 3. Potencial para atrapar al oponente
        trap_score = self._trap_potential(grid, self.pos, player_pos, grid_width, grid_height)
        
        # 4. Control del centro
        center_control = self._control_center(self.pos, grid_width, grid_height)
        
        # 5. Valor de las monedas
        coin_score = self._coin_value(grid, self.pos, coins_group, player_pos)
        
        # Pesos basados en la fase del juego
        if self.game_phase == "early":
            # Fase temprana: priorizar monedas y estabilidad
            weights = {
                'mobility': 1.0,
                'stability': 2.0,
                'trap': 0.5,
                'center': 1.5,
                'coins': 3.0
            }
        elif self.game_phase == "mid":
            # Fase media: equilibrio
            weights = {
                'mobility': 1.5,
                'stability': 1.5,
                'trap': 1.0,
                'center': 1.0,
                'coins': 2.0
            }
        else:  # late game
            # Fase tardía: priorizar atrapar al oponente
            weights = {
                'mobility': 2.0,
                'stability': 1.0,
                'trap': 2.5,
                'center': 0.5,
                'coins': 1.0
            }
            
        # Si el jugador es agresivo, ajustar para ser más defensivo
        if self.player_aggressive:
            weights['stability'] *= 1.5
            weights['trap'] *= 1.2
        
        # Calcular puntuación final ponderada
        score = (
            weights['mobility'] * mobility +
            weights['stability'] * current_stability +
            weights['trap'] * trap_score +
            weights['center'] * center_control +
            weights['coins'] * coin_score
        )
        
        return score

    def _adaptive_depth(self, grid, grid_width, grid_height):
        """Determina la profundidad de búsqueda adaptativa según el estado del juego"""
        # Contar casillas disponibles para estimar complejidad
        available_cells = sum(1 for row in grid for cell in row if cell > 0)
        total_cells = grid_width * grid_height
        
        # En juegos muy avanzados con pocas casillas, podemos buscar más profundo
        if available_cells < total_cells * 0.3:
            return 5  # Profundidad alta en finales de juego
        elif available_cells < total_cells * 0.6:
            return 4  # Profundidad media en mid-game
        else:
            return 3  # Profundidad estándar en early-game
    
    def alpha_beta(self, grid, player_pos, depth, alpha, beta, maximizing, grid_width, grid_height, coins_group=None):
        if depth == 0 or self._is_terminal(grid, player_pos, grid_width, grid_height):
            return self.evaluate(grid, player_pos, grid_width, grid_height, coins_group, depth)

        if maximizing:
            max_eval = -float('inf')
            for move in get_valid_moves(self.pos, grid, player_pos, grid_width, grid_height):
                # Crear una copia profunda del grid
                new_grid = [row[:] for row in grid]
                
                # Simular el movimiento
                x, y = move
                new_grid[self.y][self.x] -= 1  # Reducir estabilidad de casilla actual
                
                # Simular recogida de monedas
                coins_collected = False
                if coins_group:
                    for coin in coins_group:
                        if not coin.collected and (x, y) == (coin.x, coin.y):
                            coins_collected = True
                
                eval = self.alpha_beta(new_grid, player_pos, depth - 1, alpha, beta, False, grid_width, grid_height, coins_group)
                
                # Bonificación inmediata por recoger monedas
                if coins_collected:
                    eval += 5
                
                max_eval = max(max_eval, eval)
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break  # Poda beta
            return max_eval
        else:
            min_eval = float('inf')
            for move in get_valid_moves(player_pos, grid, self.pos, grid_width, grid_height):
                # Crear una copia profunda del grid
                new_grid = [row[:] for row in grid]
                
                # Simular el movimiento del jugador
                new_grid[player_pos[1]][player_pos[0]] -= 1
                
                eval = self.alpha_beta(new_grid, move, depth - 1, alpha, beta, True, grid_width, grid_height, coins_group)
                min_eval = min(min_eval, eval)
                beta = min(beta, eval)
                if beta <= alpha:
                    break  # Poda alfa
            return min_eval

    def make_move(self, grid, player_pos, grid_width, grid_height, coins_group=None):
        # Actualizar el historial de posiciones del jugador
        self.last_player_positions.append(player_pos[:])
        if len(self.last_player_positions) > 5:
            self.last_player_positions.pop(0)
            
        # Actualizar fase del juego
        self._update_game_phase(grid)
        
        # Determinar profundidad adaptativa
        search_depth = self._adaptive_depth(grid, grid_width, grid_height)
        
        best_value = -float('inf')
        best_move = None
        
        # Lista de movimientos válidos
        valid_moves = get_valid_moves(self.pos, grid, player_pos, grid_width, grid_height)
        
        if not valid_moves:
            return False
            
        # Evaluamos cada movimiento
        for move in valid_moves:
            temp_grid = copy.deepcopy(grid)
            temp_grid[self.y][self.x] -= 1  # Reducir estabilidad de casilla actual
            
            # Verificar si el movimiento va a una casilla inestable
            if temp_grid[move[1]][move[0]] <= 0:
                continue  # Evitar casillas inestables
                
            # Evaluación del movimiento con búsqueda alpha-beta
            value = self.alpha_beta(
                temp_grid,
                player_pos,
                search_depth,
                -float('inf'),
                float('inf'),
                False,
                grid_width,
                grid_height,
                coins_group
            )
            
            # Bonificación adicional si este movimiento recoge una moneda
            if coins_group:
                for coin in coins_group:
                    if not coin.collected and (move[0], move[1]) == (coin.x, coin.y):
                        # Mayor bonificación en early game, menor en late game
                        if self.game_phase == "early":
                            value += 20
                        elif self.game_phase == "mid":
                            value += 15
                        else:
                            value += 10
            
            # Penalizar fuertemente movimientos a casillas con estabilidad baja
            cell_stability = temp_grid[move[1]][move[0]]
            if cell_stability == 1:  # Casilla que quedará inestable después de pisarla
                value -= 30
            
            if value > best_value:
                best_value = value
                best_move = move

        # Si no encontramos un buen movimiento, intentar el mejor disponible
        if not best_move and valid_moves:
            best_move = valid_moves[0]
            for move in valid_moves:
                # Priorizar casillas estables
                if grid[move[1]][move[0]] > grid[best_move[1]][best_move[0]]:
                    best_move = move

        if best_move:
            dx = best_move[0] - self.x
            dy = best_move[1] - self.y
            
            # Verificar si vamos a una casilla inestable como último recurso
            going_to_unstable = grid[best_move[1]][best_move[0]] <= 1
            
            success = self.move(dx, dy, grid, player_pos, grid_width, grid_height, coins_group)
            
            # Si vamos a una casilla que se volverá inestable después de pisarla
            if success and going_to_unstable:
                print("IA se mueve a casilla casi inestable como último recurso")
                
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
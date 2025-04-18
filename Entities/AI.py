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
        return [
            pygame.transform.smoothscale(sprite, (
                int(sprite.get_width() * self.sprite_scale),
                int(sprite.get_height() * self.sprite_scale)
            )) for sprite in sprites
        ]
    
    def set_scale(self, new_scale):
        self.sprite_scale = new_scale
        self.sprites = self._scale_sprites(self.original_sprites)
        self.image = self.sprites[int(self.current_sprite)]
        self.rect = self.image.get_rect(center=self.rect.center)

    @property
    def pos(self):
        return [self.x, self.y]
    
    def move(self, dx, dy, grid, player_pos, grid_width, grid_height):
        new_x, new_y = self.x + dx, self.y + dy
        if not (0 <= new_x < grid_width and 0 <= new_y < grid_height):
            return False
        if [new_x, new_y] == player_pos:
            return False

        grid[self.y][self.x] -= 1
        self.x, self.y = new_x, new_y

        self.rect.center = (
            self.x * self.tile_size + self.margin + self.tile_size // 2,
            self.y * self.tile_size + self.margin + self.tile_size // 2
        )
        return True

    def _infer_best_move(self, grid, player_pos, grid_width, grid_height, step_count):
        """Motor de inferencia lógico simple para tomar decisiones."""
        my_moves = get_valid_moves(self.pos, grid, player_pos, grid_width, grid_height)
        player_moves = get_valid_moves(player_pos, grid, self.pos, grid_width, grid_height)

        print(f"Paso {step_count}:")
        print(f"Agente en {self.pos}")
        print(f"Jugador en {player_pos}")
        print(f"Movimientos válidos del agente: {my_moves}")
        print(f"Movimientos válidos del jugador: {player_moves}")

        # Reglas básicas: [(condición, acción)]
        rules = []

        # Regla 1: si el jugador está acorralado, intentar acercarse
        if len(player_moves) <= 1:
            print("Consulta: ¿El jugador está acorralado?")
            print(f"Resultado: True (tiene {len(player_moves)} movimiento(s))")
            def closer(move):
                return abs(move[0] - player_pos[0]) + abs(move[1] - player_pos[1])
            best = sorted(my_moves, key=closer)
            rules.append(("acorralar", best))
            print(f"Acción: Aplicando regla 'acorralar', posibles movimientos ordenados: {best}")

        # Regla 2: si el AI está acorralado, buscar más espacio
        elif len(my_moves) <= 1:
            print("Consulta: ¿El agente está acorralado?")
            print(f"Resultado: True (tiene {len(my_moves)} movimiento(s))")
            def freedom(move):
                return len(get_valid_moves(move, grid, player_pos, grid_width, grid_height))
            best = sorted(my_moves, key=freedom, reverse=True)
            rules.append(("huir", best))
            print(f"Acción: Aplicando regla 'huir', posibles movimientos ordenados: {best}")

        # Regla 3: si hay espacios con más libertad, ve hacia allá
        else:
            print("Consulta: ¿Existen zonas con más libertad de movimiento?")
            print(f"Resultado: True")
            def zone_liberty(move):
                return len(get_valid_moves(move, grid, player_pos, grid_width, grid_height))
            best = sorted(my_moves, key=zone_liberty, reverse=True)
            rules.append(("zona_libre", best))
            print(f"Acción: Aplicando regla 'zona_libre', posibles movimientos ordenados: {best}")

        # Ejecuta la primera regla aplicable
        for label, options in rules:
            if options:
                print(f"Movimiento elegido: {options[0]}")
                print("=" * 40)
                return options[0]

        print("No hay movimientos válidos.")
        print("=" * 40)
        return None

    def make_move(self, grid, player_pos, grid_width, grid_height,step_count):
        best_move = self._infer_best_move(grid, player_pos, grid_width, grid_height, step_count)
        if best_move:
            dx = best_move[0] - self.x
            dy = best_move[1] - self.y
            success = self.move(dx, dy, grid, player_pos, grid_width, grid_height)
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
        self.rect.center = (
            self.x * tile_size + margin + tile_size // 2,
            self.y * tile_size + margin + tile_size // 2
        )
        screen.blit(self.image, self.rect)
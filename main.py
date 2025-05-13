import pygame
import sys
import random
from constantes import TILE_SIZE, GRID_WIDTH, GRID_HEIGHT, MARGIN, SCREEN_SIZE
from save_score import save_score
from Screens.Start_Screen import draw_start_screen
from Screens.End_Screen import draw_end_screen
from Screens.Shop_Screen import draw_shop_screen
from Screens.Shop_Screen import hats
from Screens.Leaderboard_Screen import cargar_puntajes, draw_leaderboard_screen
from Screens.Game_screen import GameScreen
from Entities.Player import Player
from Entities.AI_MinMax import AI
from Entities.AI_Prop import AI as AIProp
from Entities.FuzzyIA import FuzzyAI
from Entities.Coin import Coin
from Entities.Grid import generate_random_grid, get_valid_moves

# Para usar la IA que se desee evaluar escribir en la variable ia_a_usar alguna de las siguientes cadenas de texto: Fuzzy (para logica difusa), MinMax (algoritmo minmax), Prop (para logica proposicional)
ia_a_usar = 'MinMax'

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_SIZE, SCREEN_SIZE))
        pygame.display.set_caption("UNSTABLE")
        
        self.clock = pygame.time.Clock()
        self.game_screen = GameScreen()
        
        self.show_start_screen = True
        self.show_leaderboard = False
        self.game_over = False
        self.winner = None
        self.turno_jugador = True
        self.esperando_ia = False
        self.IA_DELAY = 500
        self.last_move_time = 0
        self.coins = pygame.sprite.Group()
        self.coins_count = 0
        self.score = 0

        self.show_store = False
        # self.monedas = self.coins_count
        self.sombrero_actual = None
        self.sombreros_comprados = []
        self.shop_button_rects = []
        self.shop_menu_rect = None
        self.shop_jugar_rect = None

        self.leaderboard_scroll_y = 0
        self.leaderboard_scroll_speed = 20
        self.leaderboard_max_scroll = 0
        self.leaderboard_table_rect = None

        self.scroll_offset = 0

        self.grid = None
        self.player = None
        self.ai = None
        
        self.shop_error_message = None 

        self.reset_game()
        
    def generate_coins(self, num_coins):
        positions_used = [[self.player.x, self.player.y], [self.ai.x, self.ai.y]]
        
        for _ in range(num_coins):
            while True:

                x = random.randint(0, GRID_WIDTH - 1)
                y = random.randint(0, GRID_HEIGHT - 1)
                
                if [x, y] not in positions_used and self.grid[y][x] > 0:
                    new_coin = Coin(x, y)
                    self.coins.add(new_coin)
                    positions_used.append([x, y])
                    break

    def reset_game(self):
        self.grid = generate_random_grid(GRID_WIDTH, GRID_HEIGHT)
        self.player = Player(0, 0, sombrero_actual=self.sombrero_actual)
        if ia_a_usar == 'MinMax':
            self.ai = AI(GRID_WIDTH - 1, GRID_HEIGHT - 1)
        elif ia_a_usar == 'Prop':
            self.ai = AIProp(GRID_WIDTH - 1, GRID_HEIGHT - 1)
        elif ia_a_usar == 'Fuzzy':
            self.ai = FuzzyAI(GRID_WIDTH - 1, GRID_HEIGHT - 1)
        self.turno_jugador = True
        self.esperando_ia = False
        self.game_over = False
        self.winner = None
        self.coins.empty()
        self.score = 0
        self.generate_coins(5) 

    def check_game_over(self):
        player_moves = get_valid_moves(self.player.pos, self.grid, self.ai.pos, GRID_WIDTH, GRID_HEIGHT)
        ai_moves = get_valid_moves(self.ai.pos, self.grid, self.player.pos, GRID_WIDTH, GRID_HEIGHT)
        
        if not player_moves or not ai_moves:
            self.game_over = True
            if len(player_moves) > len(ai_moves):
                self.winner = "player"
            else:
                self.winner = "ai"

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False

            # Pantalla de inicio
            if self.show_start_screen:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    start_rect, ranking_rect, exit_rect = draw_start_screen(self.screen)
                    
                    if start_rect.collidepoint(event.pos):
                        self.show_start_screen = False
                        self.reset_game()
                        print("DEBUG: Botón Iniciar presionado")
                    
                    elif ranking_rect.collidepoint(event.pos):
                        self.show_start_screen = False
                        self.show_leaderboard = True
                        self.leaderboard_scroll_y = 0
                        # Forzar recarga de puntajes
                        puntajes = cargar_puntajes()
                        self.leaderboard_max_scroll = max(0, len(puntajes) * 50 - 400)
                        print("DEBUG: Botón Ranking presionado - Mostrando leaderboard")
                    
                    elif exit_rect.collidepoint(event.pos):
                        print("DEBUG: Botón Salir presionado")
                        return False

            elif self.game_over:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    button_rects = draw_end_screen(self.screen, self.winner)
                    
                    if button_rects[0].collidepoint(event.pos):  # Reintentar
                        self.reset_game()
                        self.game_over = False
                    
                    elif button_rects[1].collidepoint(event.pos):  # Guardar
                        if save_score(self.score, self.screen):
                            self.game_over = False
                            self.show_leaderboard = True
                            self.leaderboard_scroll_y = 0
                    
                    elif button_rects[2].collidepoint(event.pos):  # Tienda
                        self.show_store = True
                        self.game_over = False
                    
                    elif button_rects[3].collidepoint(event.pos):  # Menú
                        self.show_start_screen = True
                        self.game_over = False

            
            if self.show_store:
                    if event.type == pygame.MOUSEWHEEL:
                        scroll_speed = 30 
                        self.scroll_offset -= event.y * scroll_speed
                        # Limitar el scroll_offset entre 0 y el máximo permitido
                        max_scroll = max(0, len(hats) * 80 - (SCREEN_SIZE - 250))  # Calcula el máximo scroll posible
                        self.scroll_offset = max(0, min(self.scroll_offset, max_scroll))
                    
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        for rect, hat in self.shop_button_rects:
                            if rect.collidepoint(event.pos):
                                if hat["nombre"] in self.sombreros_comprados:
                                    self.sombrero_actual = hat["nombre"]
                                    self.shop_error_message = None
                                elif self.coins_count >= hat["precio"]:
                                    self.coins_count -= hat["precio"]
                                    self.sombreros_comprados.append(hat["nombre"])
                                    self.sombrero_actual = hat["nombre"]
                                    self.shop_error_message = None
                                else:
                                    self.shop_error_message = "¡No tienes suficientes monedas!"
                        
                        # Manejo de botones MENÚ y JUGAR
                        if self.shop_menu_rect and self.shop_menu_rect.collidepoint(event.pos):
                            self.show_store = False
                            self.show_start_screen = True
                            self.scroll_offset = 0  # Resetear el scroll al salir
                            self.shop_error_message = None
                        elif self.shop_jugar_rect and self.shop_jugar_rect.collidepoint(event.pos):
                            self.show_store = False
                            self.scroll_offset = 0  # Resetear el scroll al salir
                            self.reset_game()
                            self.shop_error_message = None
                            
            elif self.show_leaderboard:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    back_rect, _ = draw_leaderboard_screen(
                        self.screen,
                        self.leaderboard_scroll_y,
                        self.leaderboard_max_scroll
                    )
                    if back_rect.collidepoint(event.pos):
                        self.show_leaderboard = False
                        self.show_start_screen = True
                
                if event.type == pygame.MOUSEWHEEL:
                    self.leaderboard_scroll_y -= event.y * 20
                    self.leaderboard_scroll_y = max(0, min(
                        self.leaderboard_scroll_y,
                        self.leaderboard_max_scroll
                    ))

            if not self.game_over and not self.show_start_screen and not self.show_store:
                if event.type == pygame.KEYDOWN:
                    if self.turno_jugador:
                        dx, dy = 0, 0
                        if event.key in (pygame.K_w, pygame.K_UP): dy = -1
                        elif event.key in (pygame.K_s, pygame.K_DOWN): dy = 1
                        elif event.key in (pygame.K_a, pygame.K_LEFT): dx = -1
                        elif event.key in (pygame.K_d, pygame.K_RIGHT): dx = 1

                        if self.player.move(dx, dy, self.grid, self.ai.pos, GRID_WIDTH, GRID_HEIGHT):
                            self.score += 1
                            for coin in list(self.coins):
                                if not coin.collected and coin.check_collision(self.player.pos):
                                    self.coins_count += 1
                                    self.score += 10
                                    print('Moneda Recogida')
                            
                            current_cell_value = self.grid[self.player.y][self.player.x]
                            if current_cell_value <= 0:
                                self.winner = "ai"
                                self.coins_count = 0
                                self.game_over = True
                            else:
                                self.turno_jugador = False
                                self.esperando_ia = True
                                self.last_move_time = pygame.time.get_ticks()

                elif event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                    print("Reiniciando juego...")
                    self.reset_game()
                
                if self.show_store:
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                        self.show_store = False

        return True

    def update(self):
        current_time = pygame.time.get_ticks()
        
        if not self.game_over and not self.show_start_screen:
            
            self.player.update()  
            if hasattr(self.ai, 'update'): 
                self.ai.update()
                
            self.coins.update()
            
            all_collected = all(coin.collected for coin in self.coins)
            if all_collected and len(self.coins) > 0:
                self.generate_coins(3) 
                
            if ia_a_usar == 'MinMax':
                if self.esperando_ia and current_time - self.last_move_time > self.IA_DELAY:
                    if get_valid_moves(self.ai.pos, self.grid, self.player.pos, GRID_WIDTH, GRID_HEIGHT):
                        if self.ai.make_move(self.grid, self.player.pos, GRID_WIDTH, GRID_HEIGHT, self.coins):
                            self.winner = "player"
                            self.game_over = True
                    else:
                        self.winner = "player"
                        self.game_over = True
                    self.esperando_ia = False
                    self.turno_jugador = True
            
            elif ia_a_usar == 'Fuzzy':
                if self.esperando_ia and current_time - self.last_move_time > self.IA_DELAY:
                    if get_valid_moves(self.ai.pos, self.grid, self.player.pos, GRID_WIDTH, GRID_HEIGHT):
                        if self.ai.make_move(self.grid, self.player.pos, GRID_WIDTH, GRID_HEIGHT, self.coins):
                            current_cell_value = self.grid[self.ai.y][self.ai.x]
                            if current_cell_value <= 0:
                                self.winner = "player"
                                self.game_over = True
                    else:
                        self.winner = "player"
                        self.game_over = True
                    self.esperando_ia = False
                    self.turno_jugador = True
            
            elif ia_a_usar == 'Prop':
                if self.esperando_ia and current_time - self.last_move_time > self.IA_DELAY:
                    
                    success, collected_coin, unstable_cell = self.ai.make_move(
                        self.grid, 
                        self.player.pos, 
                        GRID_WIDTH, 
                        GRID_HEIGHT, 
                        self.coins
                    )
                    
                    if collected_coin:
                        print("IA recogió una moneda")
                    
                    if not success or unstable_cell:
                        self.winner = "player"
                        self.game_over = True
                    elif success:
                        current_cell_value = self.grid[self.ai.y][self.ai.x]
                        if current_cell_value <= 0:
                            self.winner = "player"
                            self.game_over = True
                    
                    self.esperando_ia = False
                    self.turno_jugador = True
            
            self.check_game_over()

    def render(self):
        if self.show_start_screen:
            draw_start_screen(self.screen)
        
        elif self.show_leaderboard:
            # Dibujar leaderboard y actualizar scroll máximo
            back_rect, table_rect = draw_leaderboard_screen(
                self.screen,
                self.leaderboard_scroll_y,
                self.leaderboard_max_scroll
            )
            # Actualizar el scroll máximo basado en el contenido real
            content_height = len(cargar_puntajes()) * 50
            if table_rect:
                self.leaderboard_max_scroll = max(0, content_height - table_rect.height)
        
        elif self.show_store:
            self.shop_button_rects, self.shop_menu_rect, self.shop_jugar_rect = draw_shop_screen(
                self.screen,
                self.coins_count,
                self.sombrero_actual,
                self.sombreros_comprados,
                self.scroll_offset
            )
        
        elif self.game_over:
            draw_end_screen(self.screen, self.winner)
        
        else:
            self.game_screen.draw(self.screen, self.grid, self.player, self.ai, self.coins, self.coins_count, self.score)
        
        pygame.display.flip()


    def run(self):
        running = True
        while running:
            running = self.handle_events()
            self.update()
            self.render()
            self.clock.tick(60)
        
        pygame.quit()
        sys.exit()

    

if __name__ == "__main__":
    juego = Game()
    while True:
        if not juego.handle_events():
            break
        juego.update()
        juego.render()
        juego.clock.tick(60)


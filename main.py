import pygame
import sys
import random
from constantes import TILE_SIZE, GRID_WIDTH, GRID_HEIGHT, MARGIN, SCREEN_SIZE
from Screens.Start_Screen import draw_start_screen
from Screens.End_Screen import draw_end_screen
from Screens.Shop_Screen import draw_shop_screen
from Screens.Game_screen import GameScreen
from Entities.Player import Player
from Entities.AI_MinMax import AI
from Entities.AI_Prop import AI as AIProp
from Entities.Coin import Coin
from Entities.Grid import generate_random_grid, get_valid_moves

# Para usar la IA de logica proposicional, comentar la IA de min max en la función reset_game y comentar el metodo de la clase AI llamado make_move usado en función update

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_SIZE, SCREEN_SIZE))
        pygame.display.set_caption("UNSTABLE")
        
        self.clock = pygame.time.Clock()
        self.game_screen = GameScreen()
        
        self.show_start_screen = True
        self.game_over = False
        self.winner = None
        self.turno_jugador = True
        self.esperando_ia = False
        self.IA_DELAY = 500
        self.last_move_time = 0
        self.coins = pygame.sprite.Group()
        self.coins_count = 0

        self.show_store = False
        # self.monedas = self.coins_count
        self.sombrero_actual = None
        self.sombreros_comprados = []
        self.shop_button_rects = []
        self.shop_menu_rect = None
        self.shop_jugar_rect = None


        self.scroll_offset = 0

        self.grid = None
        self.player = None
        self.ai = None
        
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
        self.player = Player(0, 0)
        #self.ai = AI(GRID_WIDTH - 1, GRID_HEIGHT - 1)
        self.ai = AIProp(GRID_WIDTH - 1, GRID_HEIGHT - 1)
        self.turno_jugador = True
        self.esperando_ia = False
        self.game_over = False
        self.winner = None
        self.coins.empty()
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


            if self.show_start_screen:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    start_button_rect, exit_button_rect = draw_start_screen(self.screen)
                    if start_button_rect.collidepoint(event.pos):
                        self.show_start_screen = False
                        self.reset_game()
                        self.game_screen = GameScreen()
                    elif exit_button_rect.collidepoint(event.pos):
                        pygame.quit()
                        sys.exit()

           
            if self.game_over:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    button_rects = draw_end_screen(self.screen, self.winner)

                    if button_rects[0].collidepoint(event.pos):  # REINTENTAR
                        self.reset_game()
                        self.game_over = False  # volver al juego
                        self.show_start_screen = False

                    elif button_rects[1].collidepoint(event.pos):  # TIENDA
                        self.scroll_offset = 0
                        # self.monedas = self.coins_count
                        self.show_store = True
                        self.game_over = False


                    elif button_rects[2].collidepoint(event.pos):  # MENÚ
                        self.reset_game()
                        self.show_start_screen = True
                        self.game_over = False  # importante salir del estado de game over

            if self.show_store:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    # Scroll
                    if event.button == 4:
                        self.scroll_offset = max(0, self.scroll_offset - 20)
                    elif event.button == 5:
                        self.scroll_offset += 20

                    elif event.button == 1:
                        # Click en sombreros
                        for rect, hat in self.shop_button_rects:
                            if rect.collidepoint(event.pos):
                                if hat["nombre"] in self.sombreros_comprados:
                                    self.sombrero_actual = hat["nombre"]
                                elif self.coins_count >= hat["precio"]:
                                    self.coins_count -= hat["precio"]
                                    self.sombreros_comprados.append(hat["nombre"])
                                    self.sombrero_actual = hat["nombre"]

                        # Botón MENÚ
                        if self.shop_menu_rect and self.shop_menu_rect.collidepoint(event.pos):
                            self.show_store = False
                            self.show_start_screen = True
                            self.reset_game()

                        # Botón JUGAR
                        elif self.shop_jugar_rect and self.shop_jugar_rect.collidepoint(event.pos):
                            self.show_store = False
                            self.reset_game()
                            self.game_screen = GameScreen()



            
            if not self.game_over and not self.show_start_screen:
                if event.type == pygame.KEYDOWN:
                    if self.turno_jugador:
                        dx, dy = 0, 0
                        if event.key in (pygame.K_w, pygame.K_UP): dy = -1
                        elif event.key in (pygame.K_s, pygame.K_DOWN): dy = 1
                        elif event.key in (pygame.K_a, pygame.K_LEFT): dx = -1
                        elif event.key in (pygame.K_d, pygame.K_RIGHT): dx = 1

                        if self.player.move(dx, dy, self.grid, self.ai.pos, GRID_WIDTH, GRID_HEIGHT):
                            for coin in list(self.coins):
                                if not coin.collected and coin.check_collision(self.player.pos):
                                    self.coins_count += 1
                                    print('Moneda Recogida')
                                    
                        
                            current_cell_value = self.grid[self.player.y][self.player.x]
                            if current_cell_value <= 0:
                                self.winner = "ai"
                                self.coins_count = 0
                                self.game_over = True
                                # print(f"¡Jugador pierde! Celda ({self.player.x},{self.player.y}) = {current_cell_value}")
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
            
            if self.esperando_ia and current_time - self.last_move_time > self.IA_DELAY:
                if get_valid_moves(self.ai.pos, self.grid, self.player.pos, GRID_WIDTH, GRID_HEIGHT):
                    #if self.ai.make_move(self.grid, self.player.pos, GRID_WIDTH, GRID_HEIGHT, self.coins):
                    if self.ai.make_move(self.grid, self.player.pos, GRID_WIDTH, GRID_HEIGHT):
                        self.winner = "player"
                        self.game_over = True
                else:
                    self.winner = "player"
                    self.game_over = True
                self.esperando_ia = False
                self.turno_jugador = True
            
            self.check_game_over()

    def render(self):
        if self.show_start_screen:
            draw_start_screen(self.screen)
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
            self.game_screen.draw(self.screen, self.grid, self.player, self.ai, self.coins, self.coins_count)


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
    game = Game()
    game.run()

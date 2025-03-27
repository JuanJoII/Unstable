import pygame
import sys
from constantes import TILE_SIZE, GRID_WIDTH, GRID_HEIGHT, MARGIN, SCREEN_SIZE
from Screens.Start_Screen import draw_start_screen
from Screens.End_Screen import draw_end_screen
from Screens.Game_screen import GameScreen
from Entities.Player import Player
from Entities.AI import AI
from Entities.Grid import generate_random_grid, get_valid_moves

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_SIZE, SCREEN_SIZE))
        pygame.display.set_caption("Arcade - Turno por Turno VISUAL")
        
        self.clock = pygame.time.Clock()
        self.game_screen = GameScreen()
        
        # Game state
        self.show_start_screen = True
        self.game_over = False
        self.winner = None
        self.turno_jugador = True
        self.esperando_ia = False
        self.IA_DELAY = 500
        self.last_move_time = 0
        
        # Game objects
        self.grid = None
        self.player = None
        self.ai = None
        
        # Initialize game
        self.reset_game()

    def reset_game(self):
        """Reset all game state to initial values"""
        self.grid = generate_random_grid(GRID_WIDTH, GRID_HEIGHT)
        self.player = Player(0, 0)
        self.ai = AI(GRID_WIDTH - 1, GRID_HEIGHT - 1)
        self.turno_jugador = True
        self.esperando_ia = False
        self.game_over = False
        self.winner = None

    def check_game_over(self):
        """Check if the game has reached a terminal state"""
        player_moves = get_valid_moves(self.player.pos, self.grid, self.ai.pos, GRID_WIDTH, GRID_HEIGHT)
        ai_moves = get_valid_moves(self.ai.pos, self.grid, self.player.pos, GRID_WIDTH, GRID_HEIGHT)
        
        if not player_moves or not ai_moves:
            self.game_over = True
            if len(player_moves) > len(ai_moves):
                self.winner = "player"
            else:
                self.winner = "ai"

    def handle_events(self):
        """Handle all pygame events including player movement and game states"""
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                return False

            
            if self.show_start_screen:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    start_button = draw_start_screen(self.screen)
                    if start_button and start_button.collidepoint(event.pos):
                        self.show_start_screen = False
                        self.reset_game()
                return True  

           
            if self.game_over:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    button_rect = draw_end_screen(self.screen, self.winner)
                    if button_rect and button_rect.collidepoint(event.pos):
                        self.reset_game()
                        self.show_start_screen = True
                return True 

            
            if not self.game_over and not self.show_start_screen:
                if event.type == pygame.KEYDOWN:
                    dx, dy = 0, 0
                    if event.key in (pygame.K_w, pygame.K_UP): dy = -1
                    elif event.key in (pygame.K_s, pygame.K_DOWN): dy = 1
                    elif event.key in (pygame.K_a, pygame.K_LEFT): dx = -1
                    elif event.key in (pygame.K_d, pygame.K_RIGHT): dx = 1

                    if self.player.move(dx, dy, self.grid, self.ai.pos, GRID_WIDTH, GRID_HEIGHT):
                        current_cell_value = self.grid[self.player.y][self.player.x]
                        if current_cell_value <= 0:
                            self.winner = "ai"
                            self.game_over = True
                            print(f"¡Jugador pierde! Celda ({self.player.x},{self.player.y}) = {current_cell_value}")
                        else:
                            self.turno_jugador = False
                            self.esperando_ia = True
                            self.last_move_time = pygame.time.get_ticks()

                
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                    print("Reiniciando juego...")
                    self.reset_game()

        return True  


    def update(self):
        """Update game state"""
        current_time = pygame.time.get_ticks()
        
        if not self.game_over and not self.show_start_screen:
            
            self.player.update()  
            if hasattr(self.ai, 'update'): 
                self.ai.update()
            
            if self.esperando_ia and current_time - self.last_move_time > self.IA_DELAY:
                if get_valid_moves(self.ai.pos, self.grid, self.player.pos, GRID_WIDTH, GRID_HEIGHT):
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
        """Render the current game state"""
        if self.show_start_screen:
            draw_start_screen(self.screen)
        elif self.game_over:
            draw_end_screen(self.screen, self.winner)
        else:
            self.game_screen.draw(self.screen, self.grid, self.player, self.ai)

    def run(self):
        """Main game loop"""
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

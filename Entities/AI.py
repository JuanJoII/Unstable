import copy
import pygame
from Entities.Grid import get_valid_moves

class AI:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.color = (255, 0, 0)  # Red
    
    @property
    def pos(self):
        return [self.x, self.y]
    
    def draw(self, screen, tile_size, margin):
        pygame.draw.rect(screen, self.color, 
                        (self.x * tile_size + margin, 
                         self.y * tile_size + margin, 
                         tile_size, tile_size))
    
    def _is_terminal(self, grid, player_pos, grid_width, grid_height):
        """Check if the game has reached a terminal state"""
        player_moves = get_valid_moves(player_pos, grid, self.pos, grid_width, grid_height)
        ai_moves = get_valid_moves(self.pos, grid, player_pos, grid_width, grid_height)
        return len(player_moves) == 0 or len(ai_moves) == 0
    
    def evaluate(self, grid, player_pos, grid_width, grid_height):
        """Evaluate the current game state"""
        player_moves = len(get_valid_moves(player_pos, grid, self.pos, grid_width, grid_height))
        ai_moves = len(get_valid_moves(self.pos, grid, player_pos, grid_width, grid_height))
        return ai_moves - player_moves

    def alpha_beta(self, grid, player_pos, depth, alpha, beta, maximizing, grid_width, grid_height):
        """Alpha-beta pruning algorithm for AI decision making"""
        if depth == 0 or self._is_terminal(grid, player_pos, grid_width, grid_height):
            return self.evaluate(grid, player_pos, grid_width, grid_height)

        if maximizing:
            max_eval = -float('inf')
            for move in get_valid_moves(self.pos, grid, player_pos, grid_width, grid_height):
                new_grid = [row[:] for row in grid]
                new_grid[move[1]][move[0]] -= 1
                eval = self.alpha_beta(new_grid, player_pos, depth - 1, alpha, beta, False, grid_width, grid_height)
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
                eval = self.alpha_beta(new_grid, move, depth - 1, alpha, beta, True, grid_width, grid_height)
                min_eval = min(min_eval, eval)
                beta = min(beta, eval)
                if beta <= alpha:
                    break
            return min_eval

    def make_move(self, grid, player_pos, grid_width, grid_height):
        """Determine and execute the AI's best move"""
        best_value = float('-inf')
        best_move = None
        for move in get_valid_moves(self.pos, grid, player_pos, grid_width, grid_height):
            temp_grid = copy.deepcopy(grid)
            temp_grid[move[1]][move[0]] -= 1
            value = self.alpha_beta(temp_grid, player_pos, 3, -float('inf'), float('inf'), False, grid_width, grid_height)
            if value > best_value:
                best_value = value
                best_move = move

        if best_move:
            self.x, self.y = best_move
            grid[best_move[1]][best_move[0]] -= 1
            return grid[best_move[1]][best_move[0]] < 0
        return False
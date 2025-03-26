import pygame

class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.color = (0, 0, 255)  # Blue
    
    @property
    def pos(self):
        return [self.x, self.y]
    
    def move(self, dx, dy, grid, ai_pos, grid_width, grid_height):
        new_x, new_y = self.x + dx, self.y + dy
        if (0 <= new_x < grid_width) and (0 <= new_y < grid_height) and [new_x, new_y] != ai_pos:
            self.x, self.y = new_x, new_y
            grid[new_y][new_x] -= 1
            return True
        return False
    
    def draw(self, screen, tile_size, margin):
        pygame.draw.rect(screen, self.color, 
                        (self.x * tile_size + margin, 
                         self.y * tile_size + margin, 
                         tile_size, tile_size))
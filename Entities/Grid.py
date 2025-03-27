import random

def generate_random_grid(width, height):
    """Generate a new random grid with values between 1 and 3"""
    return [[random.randint(1, 3) for _ in range(width)] for _ in range(height)]

def get_valid_moves(pos, grid, other_pos, grid_width, grid_height):
    """Get truly valid moves considering ALL game rules"""
    x, y = pos
    valid_moves = []
    
    if not (0 <= x < grid_width and 0 <= y < grid_height):
        return [] 
    
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    
    for dx, dy in directions:
        nx, ny = x + dx, y + dy
        
        if (0 <= nx < grid_width and 
            0 <= ny < grid_height and
            [nx, ny] != list(other_pos) and  
            grid[ny][nx] > 0):  
            
            valid_moves.append((nx, ny))
    
    return valid_moves
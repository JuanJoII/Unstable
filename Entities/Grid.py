import random

def generate_random_grid(width, height):
    """Generate a new random grid with values between 1 and 3"""
    return [[random.randint(1, 3) for _ in range(width)] for _ in range(height)]

def get_valid_moves(pos, grid, other_pos, grid_width, grid_height):
    """Get all valid moves from a position, excluding cells with value <= 0"""
    moves = []
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # Arriba, abajo, izquierda, derecha
    
    for dx, dy in directions:
        nx, ny = pos[0] + dx, pos[1] + dy
        
        # Validaciones en orden de eficiencia (primero las más rápidas)
        if (0 <= nx < grid_width and 
            0 <= ny < grid_height and 
            [nx, ny] != other_pos and 
            grid[ny][nx] > 0):  # ← Excluye 0 y negativos
            
            moves.append((nx, ny))
    
    return moves
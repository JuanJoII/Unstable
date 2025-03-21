import pygame
import constantes

class Character():
    def __init__(self, x, y):
        self.shape = pygame.Rect(0, 0, constantes.CHARACTER_WIDTH, constantes.CHARACTER_HEIGHT)
        self.shape.center = (x, y)

    def movimiento(self, delta_x, delta_y):
        self.shape.x = self.shape.x + delta_x
        self.shape.y = self.shape.y + delta_y

    def draw(self, interface):
        pygame.draw.rect(interface, constantes.CHARACTER_COLOR, self.shape)
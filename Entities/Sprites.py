import pygame

class PlayerIdle(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.sprites = [
            pygame.image.load('Assets/Base Character/Frog/frogidle_1.png'),
            pygame.image.load('Assets/Base Character/Frog/frogidle_2.png'),
            pygame.image.load('Assets/Base Character/Frog/frogidle_3.png'),
            pygame.image.load('Assets/Base Character/Frog/frogidle_4.png')
        ]
        self.current_sprite = 0
        self.image = self.sprites[self.current_sprite]
        self.rect = self.image.get_rect(center=(x, y))
        self.animation_speed = 0.1

    def update(self):
        self.current_sprite += self.animation_speed
        if self.current_sprite >= len(self.sprites):
            self.current_sprite = 0
        self.image = self.sprites[int(self.current_sprite)]


class EnemyIdle(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.sprites = [
            pygame.image.load('Assets/Base Character/Frog/Enemyfrogidle_1.png'),
            pygame.image.load('Assets/Base Character/Frog/Enemyfrogidle_2.png'),
            pygame.image.load('Assets/Base Character/Frog/Enemyfrogidle_3.png'),
            pygame.image.load('Assets/Base Character/Frog/Enemyfrogidle_4.png')
        ]
        self.current_sprite = 0
        self.image = self.sprites[self.current_sprite]
        self.rect = self.image.get_rect(center=(x, y))
        self.animation_speed = 0.1

    def update(self):
        self.current_sprite += self.animation_speed
        if self.current_sprite >= len(self.sprites):
            self.current_sprite = 0
        self.image = self.sprites[int(self.current_sprite)]

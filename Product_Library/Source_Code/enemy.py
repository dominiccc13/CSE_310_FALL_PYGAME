import pygame
import random

class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load('CSE_310_FALL_PYGAME/Product_Library/Source_Code/art/enemy.png')
        self.image = pygame.transform.scale(self.image, (40, 40))
        self.rect = self.image.get_rect(topleft=(x, y))
        self.speed = random.choice([-2, 2])

    def update(self):
        self.rect.x += self.speed
        if self.rect.left < 0 or self.rect.right > 1000:
            self.speed *= -1

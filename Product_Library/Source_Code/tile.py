# tile.py
import pygame

class Tile(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        super().__init__()
        self.image = pygame.Surface((width, height))
        self.image.fill((34, 177, 76))  # Green color for the platforms
        self.rect = self.image.get_rect(topleft=(x, y))

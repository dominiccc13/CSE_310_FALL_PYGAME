import pygame

class Player(pygame.sprite.Sprite):
    def __init__(self, player_image):
        super().__init__()  # Properly initialize the Sprite base class
        self.image = pygame.image.load(player_image).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.topleft = (0, 0)  # Temporary position; the main file will set the actual starting position

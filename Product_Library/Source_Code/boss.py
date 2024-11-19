import pygame

class Boss(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load('CSE_310_FALL_PYGAME/Product_Library/Source_Code/art/player.png')
        self.image = pygame.transform.scale(self.image, (100, 100))
        self.rect = self.image.get_rect(center=(500, 300))
        self.active = False
        self.health = 100

    def update(self):
        # Add boss behavior here
        pass

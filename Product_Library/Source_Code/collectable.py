import pygame

class Collectable(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load('CSE_310_FALL_PYGAME/Product_Library/Source_Code/art/collectable.png')
        self.image = pygame.transform.scale(self.image, (30, 30))
        self.rect = self.image.get_rect(topleft=(x, y))

    def update(self):
        # Optional behavior for collectables
        pass

import pygame

class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        super().__init__()
        self.image = pygame.Surface((width, height))
        self.image.fill((34, 177, 76))  # Green color for the platforms
        self.rect = self.image.get_rect(topleft=(x, y))

    def update(self):
        # Update method can be added for future logic if needed
        pass

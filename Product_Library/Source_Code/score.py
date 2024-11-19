import pygame

class Score:
    def __init__(self):
        self.font = pygame.font.Font(None, 36)
        self.value = 0

    def increase(self, amount=10):
        self.value += amount

    def draw(self, screen):
        text = self.font.render(f"Score: {self.value}", True, (255, 255, 255))
        screen.blit(text, (10, 10))

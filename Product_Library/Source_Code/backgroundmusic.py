import pygame

class BackgroundMusic:
    def __init__(self):
        pygame.mixer.music.load('CSE_310_FALL_PYGAME/Product_Library/Source_Code/music/8-bit-music-on-245249.mp3')

    def play_music(self):
        pygame.mixer.music.play(-1)  # Loop indefinitely

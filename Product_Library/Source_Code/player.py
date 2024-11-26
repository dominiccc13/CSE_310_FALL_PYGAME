import pygame
from entity import Entity
from platform_module import Platform
from typing import List
# from main import SCREEN_WIDTH
SCREEN_WIDTH, SCREEN_HEIGHT = 1000, 600

class Player(Entity):
    def __init__(self, health: int):
        # Initialize the parent class
        super().__init__(health)
        
        # Load player sprite
        self.image = pygame.image.load("Product_Library/Source_Code/art/player_frame1_True.png")
        self.rect = self.image.get_rect()
        self.rect.topleft = (500, 500)

        self.half_jump_height = 12
        self.is_jumping = False
        self.jumps_left = 2

        # Initialize player-specific attributes
        self.level = 1  # Start the player at level 1
        self.animation_True = [
            "Product_Library/Source_Code/art/player_frame1_True.png",
            "Product_Library/Source_Code/art/player_frame2_True.png"
        ]
        self.animation_False = [
            "Product_Library/Source_Code/art/player_frame1_False.png",
            "Product_Library/Source_Code/art/player_frame2_False.png"
        ]

    def update_entity(self):
        #! Below is the current error message when this function is implemented
        # """Traceback (most recent call last):
        # File "c:\Users\Grant Jones\Desktop\Fall2024\CSE_310\Team_Project\CSE_310_FALL_PYGAME\Product_Library\Source_Code\main.py", line 5, in <module>
        #     from player import Player
        # File "c:\Users\Grant Jones\Desktop\Fall2024\CSE_310\Team_Project\CSE_310_FALL_PYGAME\Product_Library\Source_Code\player.py", line 3, in <module>
        #     from main import SCREEN_WIDTH
        # File "c:\Users\Grant Jones\Desktop\Fall2024\CSE_310\Team_Project\CSE_310_FALL_PYGAME\Product_Library\Source_Code\main.py", line 5, in <module>
        #     from player import Player
        # ImportError: cannot import name 'Player' from partially initialized module 'player' (most likely due to a circular import) (c:\Users\Grant Jones\Desktop\Fall2024\CSE_310\Team_Project\CSE_310_FALL_PYGAME\Product_Library\Source_Code\player.py)
        # """
                # Player input handling
        keys = pygame.key.get_pressed()

        # Movement
        if keys[pygame.K_a] and self.rect.left > 0:
            self.flip_False()
            self.update_frame()
            self.rect.x -= self.move_speed
        if keys[pygame.K_d] and self.rect.right < SCREEN_WIDTH:
            self.flip_True()
            self.update_frame()
            self.rect.x += self.move_speed

        #  # Jumping logic with double jump
        # if keys[pygame.K_SPACE]:
        #     if self.jumps_left > 0 and not self.is_jumping:
        #         self.velocity_y = -self.half_jump_height if self.jumps_left == 2 else -self.half_jump_height
        #         self.jumps_left -= 1
        #         self.is_jumping = True

        # # Apply gravity
        # self.rect.y += self.velocity_y
        # if self.velocity_y < 0:
        #     self.is_jumping = True
        # elif self.velocity_y > 0:
        #     self.is_jumping = False

        # if self.rect.colliderect(Platform):
        #     if self.velocity_y > 0:
        #         self.rect.bottom = Platform.rect.top
        #         self.velocity_y = 0
        #         self.is_jumping = False
        #         self.jumps_left = 2
                

            
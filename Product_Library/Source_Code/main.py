import pygame
import sys
import random
import math
from player import Player
from enemy import Enemy
from platform import Platform

# from db import create_save
# from db import load_player_save
# from db import load_enemies_save
# from db import load_platforms_save

pygame.init()

try:
    pygame.mixer.init()
except pygame.error as e:
    print(f"Error initializing Pygame mixer: {e}")
    sys.exit(1)

# Constants
BACKGROUND_IMAGES = [
    'Product_Library/Source_Code/art/background_1.png',
    'Product_Library/Source_Code/art/background_2.png',
    'Product_Library/Source_Code/art/background_3.png',
    'Product_Library/Source_Code/art/background_4.png',
    'Product_Library/Source_Code/art/background_5.png',
    'Product_Library/Source_Code/art/background_6.png',
    'Product_Library/Source_Code/art/background_7.png',
    'Product_Library/Source_Code/art/background_8.png',
    'Product_Library/Source_Code/art/background_9.png',
    'Product_Library/Source_Code/art/background_10.png'
]
# PLAYER_IMAGE = 'Product_Library/Source_Code/art/player.png'
SCREEN_WIDTH, SCREEN_HEIGHT = 1000, 600

# Player movement settings
move_speed = 4
jump_height = 25
gravity = 1
velocity_y = 0
is_jumping = False

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# Function to load a random background image
def load_random_background():
    background_image_path = random.choice(BACKGROUND_IMAGES)
    try:
        background_image = pygame.image.load(background_image_path)
        return pygame.transform.scale(background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
    except pygame.error as e:
        print(f"Error loading background image: {e}")
        sys.exit(1)

# Function to generate platforms
def generate_platforms(num_platforms, exit_rect):
    platforms = pygame.sprite.Group()
    for _ in range(num_platforms):
        while True:
            width = random.randint(80, 200)
            height = 20
            x = random.randint(0, SCREEN_WIDTH - width)
            y = random.randint(50, SCREEN_HEIGHT - height - 50)

            # Create a new platform
            new_platform = Platform(x, y, width, height)
            if not new_platform.rect.colliderect(exit_rect):  # Ensure it doesn't overlap with exit
                platforms.add(new_platform)
                break
    return platforms

# Function to generate exit rectangle
def generate_exit(platforms):
    while True:
        exit_width = 50
        exit_height = 50
        x = random.randint(0, SCREEN_WIDTH - exit_width)
        y = random.randint(50, SCREEN_HEIGHT - exit_height - 50)

        exit_rect = pygame.Rect(x, y, exit_width, exit_height)

        # Check if the exit is on a platform
        if any(platform.rect.colliderect(exit_rect) for platform in platforms):
            return exit_rect

# Load initial background image
background_image = load_random_background()

# Generate platforms and exit
num_platforms = random.randint(6, 9)
platforms = generate_platforms(num_platforms, pygame.Rect(0, 0, 50, 50))  # Dummy exit rect for initial generation
exit_rect = generate_exit(platforms)

# Load player and set starting position randomly on a platform
player = Player(10)
platforms_list = list(platforms)
random_platform = random.choice(platforms_list)
player.rect.midbottom = (random_platform.rect.centerx, random_platform.rect.top)

# Frame rate control
clock = pygame.time.Clock()

# Game loop
while True:
    pygame.event.pump()

    # Frame rate control
    clock.tick(60)  # Limit to 60 frames per second

    # Player input handling
    keys = pygame.key.get_pressed()
        
    # Move Left
    if keys[pygame.K_a] and player.rect.left > 0:
        player.flip_False()
        player.rect.x -= 8
    
        # Move Right
    if keys[pygame.K_d] and player.rect.right < 1000:
        player.flip_True()
        player.rect.x += 8

        # Jump
    if keys[pygame.K_SPACE] and not is_jumping:
        is_jumping = True
        velocity_y = -jump_height

    # Apply gravity or jumping
    player.rect.y += velocity_y
    velocity_y += gravity if is_jumping else 0

    # Collision detection with platforms
    on_platform = False
    for platform in platforms:
        if player.rect.colliderect(platform.rect):
            if velocity_y > 0:  # Player is falling
                player.rect.bottom = platform.rect.top
                velocity_y = 0
                is_jumping = False
                on_platform = True
                break

    # Apply gravity only if not on any platform
    if not on_platform and player.rect.bottom < SCREEN_HEIGHT:
        velocity_y += gravity

    # Check for level exit
    if player.rect.colliderect(exit_rect):
        # Load new level
        background_image = load_random_background()
        platforms = generate_platforms(num_platforms, exit_rect)  # Regenerate platforms
        exit_rect = generate_exit(platforms)  # Generate new exit
        
        # Convert platforms group to a list and respawn player on a new platform
        platforms_list = list(platforms)
        random_platform = random.choice(platforms_list) if platforms_list else None  # Check if there are platforms
        if random_platform:
            player.rect.midbottom = (random_platform.rect.centerx, random_platform.rect.top)

        # Check if the player has fallen past the bottom of the screen
    if player.rect.top >= SCREEN_HEIGHT:
        # Convert platforms group to a list and respawn player on a new platform
        platforms_list = list(platforms)
        random_platform = random.choice(platforms_list) if platforms_list else None  # Check if there are platforms
        if random_platform:
            # Respawn the player on the selected platform
            player.rect.midbottom = (random_platform.rect.centerx, random_platform.rect.top)
            # Reset vertical velocity to prevent immediate falling
            velocity_y = 0
            is_jumping = False

    # Exit condition
    if keys[pygame.K_ESCAPE]:
        break

    screen.blit(background_image, (0,0))
    platforms.draw(screen)
    pygame.draw.rect(screen, (255, 0, 0), exit_rect)  # Draw exit rectangle
    screen.blit(player.image, player.rect)  # Draw player on the screen
    pygame.display.flip()  # Update the display

    clock.tick(60)

pygame.quit()
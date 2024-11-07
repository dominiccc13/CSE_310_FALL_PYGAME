import pygame
import sys
import random
from player import Player
from tile import Tile

pygame.init()

try:
    pygame.mixer.init()
except pygame.error as e:
    print(f"Error initializing Pygame mixer: {e}")
    sys.exit(1)

# Constants
BACKGROUND_IMAGES = [
    'CSE_310_FALL_PYGAME/Product_Library/Source_Code/art/background_1.png',
    'CSE_310_FALL_PYGAME/Product_Library/Source_Code/art/background_2.png',
    'CSE_310_FALL_PYGAME/Product_Library/Source_Code/art/background_3.png',
    'CSE_310_FALL_PYGAME/Product_Library/Source_Code/art/background_4.png',
    'CSE_310_FALL_PYGAME/Product_Library/Source_Code/art/background_5.png',
    'CSE_310_FALL_PYGAME/Product_Library/Source_Code/art/background_6.png',
    'CSE_310_FALL_PYGAME/Product_Library/Source_Code/art/background_7.png',
    'CSE_310_FALL_PYGAME/Product_Library/Source_Code/art/background_8.png',
    'CSE_310_FALL_PYGAME/Product_Library/Source_Code/art/background_9.png',
    'CSE_310_FALL_PYGAME/Product_Library/Source_Code/art/background_10.png'
]
PLAYER_IMAGE = 'CSE_310_FALL_PYGAME/Product_Library/Source_Code/art/player.png'
SCREEN_WIDTH, SCREEN_HEIGHT = 1000, 600

# Player movement settings
move_speed = 4
jump_height = 20
gravity = 0.5
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
    min_gap_x = 200  # Minimum horizontal gap between platforms
    max_gap_x = 300  # Maximum horizontal gap between platforms
    min_gap_y = 200   # Minimum vertical gap between platforms
    max_gap_y = 400  # Maximum vertical gap between platforms

    for _ in range(num_platforms):
        while True:
            width = random.randint(80, 200)
            height = 20
            
            if len(platforms) == 0:
                # Position the first platform near the bottom of the screen
                x = random.randint(0, SCREEN_WIDTH - width)
                y = random.randint(SCREEN_HEIGHT - 100, SCREEN_HEIGHT - 50)
            else:
                # Position subsequent platforms based on previous platform
                prev_platform = random.choice(platforms.sprites())
                x = random.randint(
                    max(0, prev_platform.rect.x - max_gap_x),
                    min(SCREEN_WIDTH - width, prev_platform.rect.x + max_gap_x)
                )
                y = random.randint(
                    max(50, prev_platform.rect.y - max_gap_y),
                    min(SCREEN_HEIGHT - height - 50, prev_platform.rect.y + max_gap_y)
                )

            # Create a new platform
            new_platform = Tile(x, y, width, height)
            if not new_platform.rect.colliderect(exit_rect):  # Ensure it doesn't overlap with the exit
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
player = Player(PLAYER_IMAGE)
platforms_list = list(platforms)
random_platform = random.choice(platforms_list)
player.rect.midbottom = (random_platform.rect.centerx, random_platform.rect.top)

# Frame rate control
clock = pygame.time.Clock()

# Game loop
while True:
    pygame.event.pump()
    keys = pygame.key.get_pressed()
    
    # Horizontal movement
    if keys[pygame.K_a] and player.rect.left > 0:
        player.rect.x -= move_speed
    if keys[pygame.K_d] and player.rect.right < SCREEN_WIDTH:
        player.rect.x += move_speed

    # Jump initiation
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

    # Exit condition
    if keys[pygame.K_ESCAPE]:
        break

    # Drawing
    screen.blit(background_image, (0, 0))  # Draw the background image
    platforms.draw(screen)                  # Draw platforms on top of the background
    pygame.draw.rect(screen, (255, 0, 0), exit_rect)  # Draw exit rectangle
    screen.blit(player.image, player.rect)  # Draw the player
    pygame.display.flip()                   # Update the display

    # Frame rate control
    clock.tick(60)  # Limit to 60 frames per second

pygame.quit()
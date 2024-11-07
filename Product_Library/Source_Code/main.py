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
NORMAL_BACKGROUND_IMAGES = [
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
    # add all normal background images
]
DUNGEON_BACKGROUND_IMAGES = [
    'CSE_310_FALL_PYGAME/Product_Library/Source_Code/art/dungeon_background_1.png',
    'CSE_310_FALL_PYGAME/Product_Library/Source_Code/art/dungeon_background_2.png',
    'CSE_310_FALL_PYGAME/Product_Library/Source_Code/art/dungeon_background_3.png',
    'CSE_310_FALL_PYGAME/Product_Library/Source_Code/art/dungeon_background_4.png',
    'CSE_310_FALL_PYGAME/Product_Library/Source_Code/art/dungeon_background_5.png'
    
    # add dungeon-specific images
]

PLAYER_IMAGE = 'CSE_310_FALL_PYGAME/Product_Library/Source_Code/art/player.png'
SCREEN_WIDTH, SCREEN_HEIGHT = 1000, 600

# Player movement settings
move_speed = 4
jump_height = 20
gravity = 0.5
velocity_y = 0
is_jumping = False

# Level settings
level_count = 1
used_backgrounds = []

# Screen setup
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()

# Load player
player = Player(PLAYER_IMAGE)

# Function to load a random background, ensuring no repeats until all images are used
def load_random_background(is_dungeon=False):
    global used_backgrounds
    background_list = DUNGEON_BACKGROUND_IMAGES if is_dungeon else NORMAL_BACKGROUND_IMAGES
    if len(used_backgrounds) == len(background_list):
        used_backgrounds = []  # Reset used images when all have been used

    background_image_path = random.choice([bg for bg in background_list if bg not in used_backgrounds])
    used_backgrounds.append(background_image_path)
    try:
        background_image = pygame.image.load(background_image_path)
        return pygame.transform.scale(background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
    except pygame.error as e:
        print(f"Error loading background image: {e}")
        sys.exit(1)

# Function to generate platforms with no overlap
def generate_platforms(num_platforms, exit_rect):
    platforms = pygame.sprite.Group()
    for _ in range(num_platforms):
        attempt = 0
        while attempt < 10:  # Retry limit to avoid infinite loops
            width = random.randint(80, 200)
            height = 20
            x = random.randint(0, SCREEN_WIDTH - width)
            y = random.randint(50, SCREEN_HEIGHT - height - 50)
            new_platform = Tile(x, y, width, height)

            # Check for overlap with existing platforms or exit
            if not any(platform.rect.colliderect(new_platform.rect) for platform in platforms) and \
               not new_platform.rect.colliderect(exit_rect):
                platforms.add(new_platform)
                break
            attempt += 1
    return platforms

# Function to generate exit rectangle
def generate_exit(platforms):
    while True:
        exit_width, exit_height = 50, 50
        x = random.randint(0, SCREEN_WIDTH - exit_width)
        y = random.randint(50, SCREEN_HEIGHT - exit_height - 50)
        exit_rect = pygame.Rect(x, y, exit_width, exit_height)
        if any(platform.rect.colliderect(exit_rect) for platform in platforms):
            return exit_rect

# Function to display level transition with fade effect
def level_transition(level):
    fade_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
    fade_surface.fill((0, 0, 0))
    for alpha in range(0, 255, 5):
        fade_surface.set_alpha(alpha)
        screen.blit(fade_surface, (0, 0))
        font = pygame.font.Font(None, 60)
        text = font.render(f"Level {level}", True, (255, 255, 255))
        text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        screen.blit(text, text_rect)
        pygame.display.flip()
        pygame.time.delay(30)

# Initial background, platforms, and exit generation
background_image = load_random_background()
num_platforms = random.randint(6, 9)
platforms = generate_platforms(num_platforms, pygame.Rect(0, 0, 50, 50))  # Dummy exit rect for initial generation
exit_rect = generate_exit(platforms)

# Initial player position on a random platform
platforms_list = list(platforms)
random_platform = random.choice(platforms_list)
player.rect.midbottom = (random_platform.rect.centerx, random_platform.rect.top)

# Game loop
while True:
    pygame.event.pump()
    keys = pygame.key.get_pressed()

    # Movement
    if keys[pygame.K_a] and player.rect.left > 0:
        player.rect.x -= move_speed
    if keys[pygame.K_d] and player.rect.right < SCREEN_WIDTH:
        player.rect.x += move_speed

    if keys[pygame.K_SPACE] and not is_jumping:
        is_jumping = True
        velocity_y = -jump_height

    player.rect.y += velocity_y
    velocity_y += gravity if is_jumping else 0

    # Collision detection
    on_platform = False
    for platform in platforms:
        if player.rect.colliderect(platform.rect):
            if velocity_y > 0:
                player.rect.bottom = platform.rect.top
                velocity_y = 0
                is_jumping = False
                on_platform = True
                break

    if not on_platform and player.rect.bottom < SCREEN_HEIGHT:
        velocity_y += gravity

    # Level transition on exit collision
    if player.rect.colliderect(exit_rect):
        level_count += 1
        level_transition(level_count)

        # Determine level type and reset assets
        is_dungeon = (level_count % 10 == 0)
        background_image = load_random_background(is_dungeon)
        platforms = generate_platforms(num_platforms, exit_rect)
        exit_rect = generate_exit(platforms)
        random_platform = random.choice(list(platforms))
        player.rect.midbottom = (random_platform.rect.centerx, random_platform.rect.top)

    # Exit on escape
    if keys[pygame.K_ESCAPE]:
        break

    # Drawing
    screen.blit(background_image, (0, 0))
    platforms.draw(screen)
    pygame.draw.rect(screen, (255, 0, 0), exit_rect)
    screen.blit(player.image, player.rect)
    pygame.display.flip()
    clock.tick(60)

pygame.quit()

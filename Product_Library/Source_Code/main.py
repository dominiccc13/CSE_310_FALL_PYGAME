import pygame
import sys
import random
from player import Player
from platform import Platform

pygame.init()

try:
    pygame.mixer.init()
except pygame.error as e:
    print(f"Error initializing Pygame mixer: {e}")
    sys.exit(1)

# Constants
NORMAL_BACKGROUND_IMAGES = [
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
DUNGEON_BACKGROUND_IMAGES = [
    'Product_Library/Source_Code/art/dungeon_background_1.png',
    'Product_Library/Source_Code/art/dungeon_background_2.png',
    'Product_Library/Source_Code/art/dungeon_background_3.png',
    'Product_Library/Source_Code/art/dungeon_background_4.png',
    'Product_Library/Source_Code/art/dungeon_background_5.png'
]

PLAYER_IMAGE = 'Product_Library/Source_Code/art/player.png'
SCREEN_WIDTH, SCREEN_HEIGHT = 1000, 600

# Player movement settings
move_speed = 4
jump_height = 20
half_jump_height = 10
gravity = 0.5
velocity_y = 0
is_jumping = False
jump_count = 0
can_double_jump = False

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

# Constants for minimum and maximum gaps between platforms
MIN_GAP_X = 100  # minimum gap in the x direction
MAX_GAP_X = 400  # maximum gap in the x direction
MIN_GAP_Y = 80   # minimum gap in the y direction
MAX_GAP_Y = 300  # maximum gap in the y direction

# Modified generate_platforms function to ensure gaps between platforms
def generate_platforms(num_platforms, exit_rect):
    platforms = pygame.sprite.Group()
    last_platform_rect = None

    for _ in range(num_platforms):
        attempt = 0
        while attempt < 10:
            width = random.randint(80, 200)
            height = 20
            if last_platform_rect:
                # Set x and y based on the last platform to maintain gaps
                x = last_platform_rect.right + random.randint(MIN_GAP_X, MAX_GAP_X)
                y = last_platform_rect.top + random.randint(-MAX_GAP_Y, MAX_GAP_Y)
                # Ensure new platform doesn't go off-screen
                if x + width > SCREEN_WIDTH:
                    x = random.randint(0, SCREEN_WIDTH - width)
                if y < 50 or y > SCREEN_HEIGHT - height - 50:
                    y = random.randint(50, SCREEN_HEIGHT - height - 50)
            else:
                # Position first platform randomly within screen bounds
                x = random.randint(0, SCREEN_WIDTH - width)
                y = random.randint(50, SCREEN_HEIGHT - height - 50)

            new_platform = Tile(x, y, width, height)

            # Ensure no overlap with existing platforms and no collision with exit
            if not any(platform.rect.colliderect(new_platform.rect) for platform in platforms) and \
               not new_platform.rect.colliderect(exit_rect):
                platforms.add(new_platform)
                last_platform_rect = new_platform.rect  # Update last platform position
                break
            attempt += 1
    return platforms

# Function to generate exit rectangle on top of a platform
def generate_exit(platforms):
    selected_platform = random.choice(list(platforms))
    exit_width, exit_height = 50, 50
    x = selected_platform.rect.centerx - exit_width // 2
    y = selected_platform.rect.top - exit_height
    return pygame.Rect(x, y, exit_width, exit_height)

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
num_platforms = random.randint(10, 12)
platforms = generate_platforms(num_platforms, pygame.Rect(0, 0, 50, 50))
exit_rect = generate_exit(platforms)

# Initial player position on a random platform that is not the same as the exit platform
platforms_list = list(platforms)
exit_platform = next((platform for platform in platforms if platform.rect.colliderect(exit_rect)), None)
available_platforms = [platform for platform in platforms_list if platform != exit_platform]
random_platform = random.choice(available_platforms) if available_platforms else random.choice(platforms_list)
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

    # Jumping logic
    if keys[pygame.K_SPACE]:
        if not is_jumping:
            velocity_y = -jump_height
            is_jumping = True
            can_double_jump = True
        elif can_double_jump:
            velocity_y = -half_jump_height
            can_double_jump = False

    # Apply gravity
    player.rect.y += velocity_y
    if velocity_y < 0:
        is_jumping = True
    elif velocity_y > 0:
        is_jumping = False

    # Collision detection
    on_platform = False
    for platform in platforms:
        if player.rect.colliderect(platform.rect):
            if velocity_y > 0:
                player.rect.bottom = platform.rect.top
                velocity_y = 0
                is_jumping = False
                can_double_jump = False
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
        exit_platform = next((platform for platform in platforms if platform.rect.colliderect(exit_rect)), None)
        available_platforms = [platform for platform in platforms if platform != exit_platform]
        random_platform = random.choice(available_platforms) if available_platforms else random.choice(list(platforms))
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
sys.exit()

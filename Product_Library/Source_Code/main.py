import pygame
import sys
import random
import math
from player import Player
from flying_enemy import Flying_Enemy
from tile import Tile

pygame.init()

try:
    pygame.mixer.init()
except pygame.error as e:
    print(f"Error initializing Pygame mixer: {e}")
    sys.exit(1)

#-----------------------------------------------------------------------------------------------------
#* Constants
BACKGROUND = (53, 81, 92)
PLAYER = 'Product_Library/Source_Code/art/player_frame1_True.png'
ENEMY = 'Product_Library/Source_Code/art/enemy_frame1_True.png'
SCREEN_WIDTH, SCREEN_HEIGHT = 1000, 600

#-----------------------------------------------------------------------------------------------------
#* Player movement settings
move_speed = 4          # Speed for left/right movement
jump_height = 17        # Initial upward jump velocity
gravity = 0.5           # Gravity for a smoother fall
velocity_y = 0          # Vertical velocity
is_jumping = False       # Jumping state

#-----------------------------------------------------------------------------------------------------
#* Window and Object Initialization
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
back_wall = pygame.image.load("Product_Library/Source_Code/art/dungeon_wall.png").convert()
back_wall_width = back_wall.get_width()
back_wall_rect = back_wall.get_rect()
player = Player(PLAYER)
enemy = Flying_Enemy(ENEMY)
#-----------------------------------------------------------------------------------------------------

#-----------------------------------------------------------------------------------------------------
#* Creating infinite Background
scroll = 0
wall_tiles = math.ceil(SCREEN_WIDTH / back_wall_width) + 1

#-----------------------------------------------------------------------------------------------------
# Define a more complex map layout
platforms = pygame.sprite.Group()
map_layout = [
    (0, 580, 1000, 20),    # Ground platform
    (150, 450, 150, 20),   # Platform 1
    (400, 380, 200, 20),   # Platform 2
    (700, 300, 180, 20),   # Platform 3
    (500, 200, 100, 20),   # Platform 4 (higher)
    (850, 150, 100, 20),   # Platform 5
    (200, 100, 150, 20),   # Platform 6
]

for x, y, width, height in map_layout:
    platforms.add(Tile(x, y, width, height))

#-----------------------------------------------------------------------------------------------------
# Load player and set starting position randomly on top of one of the platforms
random_platform = random.choice(map_layout)
player.rect.midbottom = (random_platform[0] + random_platform[2] // 2, random_platform[1])

#-----------------------------------------------------------------------------------------------------
# Frame rate control
clock = pygame.time.Clock()

#-----------------------------------------------------------------------------------------------------
# Game loop
while True:
    pygame.event.pump()

    # Frame rate control
    clock.tick(60)  # Limit to 60 frames per second

    # Draw Scrolling Backround
    for i in range(wall_tiles):
        screen.blit(back_wall, (i * back_wall_width + scroll, 0))

    # Background Scroll Speed
    scroll -= 0

    # Player input handling
    keys = pygame.key.get_pressed()
    
        # Move Left
    if keys[pygame.K_a] and player.rect.left > 0:
        player.flip_False()
        player.rect.x -= 3
    
        # Move Right
    if keys[pygame.K_d] and player.rect.right < 1000:
        player.flip_True()
        player.rect.x += 3

        # Jump
    if keys[pygame.K_SPACE] and not is_jumping:
            is_jumping = True
            velocity_y = -jump_height  # Initiate jump by setting upward velocity

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

    # Set Enemy Control
    enemy.patrol()

    #reset scroll
    if abs(scroll) >= back_wall_width:
        scroll = 0

    # Exit condition
    if keys[pygame.K_ESCAPE]:
        break
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            break

    # Drawing
    
    screen.blit(player.image, player.rect)  # Draw player on the screen
    screen.blit(enemy.image, enemy.rect)  # Draw enemy on the screen
    platforms.draw(screen)
    pygame.display.flip()
#-----------------------------------------------------------------------------------------------------

pygame.quit()

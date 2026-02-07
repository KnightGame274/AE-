import pygame
import math

# Initialize pygame
pygame.init()

# Set up the game window
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("My First Game")

# Player settings
player_x = 370
player_y = 480
player_speed = 0.5

# Enemy settings
enemy_x = 200
enemy_y = 50
enemy_speed = 0.3

# Game variables
score = 0
lives = 3

# Collision function
def is_collision(px, py, ex, ey):
    distance = math.sqrt((px - ex)**2 + (py - ey)**2)
    return distance < 50

# Game loop
running = True
while running:
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Player movement
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        player_x -= player_speed
    if keys[pygame.K_RIGHT]:
        player_x += player_speed

    # Enemy movement
    enemy_x += enemy_speed
    if enemy_x >= 750 or enemy_x <= 0:
        enemy_speed *= -1  # Reverse direction

    # Collision detection
    if is_collision(player_x, player_y, enemy_x, enemy_y):
        lives -= 1
        if lives == 0:
            print("Game Over!")
            running = False
        else:
            # Reset positions
            player_x = 370
            enemy_x = 200

    # Update score
    score += 1
    print(f"Score: {score} Lives: {lives}")

    # Drawing
    screen.fill((0, 0, 255))  # Blue background
    pygame.draw.rect(screen, (255, 0, 0), (player_x, player_y, 50, 50))  # Player
    pygame.draw.rect(screen, (0, 255, 0), (enemy_x, enemy_y, 50, 50))    # Enemy

    pygame.display.update()

pygame.quit()
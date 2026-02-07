import pygame
import random
import math

# Initialize pygame
pygame.init()

# Ekran ayarları
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Top-Down Shooter")

# Renkler
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED   = (255, 0, 0)
GREEN = (0, 255, 0)
YELLOW= (255, 255, 0)

# Font
font = pygame.font.Font(None, 36)

# Oyuncu
player_x = WIDTH // 2
player_y = HEIGHT - 60
player_speed = 5

# Mermiler
bullets = []

# Düşmanlar
enemies = []
for i in range(5):
    enemies.append([random.randint(0, WIDTH-40), random.randint(50, 200), 2])

# Skor ve can
score = 0
lives = 3

def is_collision(x1, y1, x2, y2):
    distance = math.sqrt((x1-x2)**2 + (y1-y2)**2)
    return distance < 30

def show_score_lives():
    score_text = font.render(f"Score: {score}", True, WHITE)
    lives_text = font.render(f"Lives: {lives}", True, WHITE)
    screen.blit(score_text, (10, 10))
    screen.blit(lives_text, (10, 40))

# Oyun döngüsü
running = True
while running:
    screen.fill(BLACK)

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                bullets.append([player_x+15, player_y])

    # Oyuncu hareketi
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and player_x > 0:
        player_x -= player_speed
    if keys[pygame.K_RIGHT] and player_x < WIDTH-40:
        player_x += player_speed
    if keys[pygame.K_UP] and player_y > 0:
        player_y -= player_speed
    if keys[pygame.K_DOWN] and player_y < HEIGHT-40:
        player_y += player_speed

    # Oyuncu çizimi
    pygame.draw.rect(screen, GREEN, (player_x, player_y, 40, 40))

    # Mermiler
    for bullet in bullets[:]:
        bullet[1] -= 10
        pygame.draw.rect(screen, YELLOW, (bullet[0], bullet[1], 10, 20))
        if bullet[1] < 0:
            bullets.remove(bullet)
        else:
            for enemy in enemies:
                if is_collision(bullet[0], bullet[1], enemy[0], enemy[1]):
                    score += 10
                    bullets.remove(bullet)
                    enemy[0] = random.randint(0, WIDTH-40)
                    enemy[1] = random.randint(50, 200)
                    break

    # Düşmanlar
    for enemy in enemies:
        enemy[1] += enemy[2]
        if enemy[1] > HEIGHT:
            enemy[0] = random.randint(0, WIDTH-40)
            enemy[1] = random.randint(50, 200)
            lives -= 1
            if lives == 0:
                print("Game Over!")
                running = False
        pygame.draw.rect(screen, RED, (enemy[0], enemy[1], 40, 40))

    # Skor ve can
    show_score_lives()

    pygame.display.update()
    pygame.time.Clock().tick(30)

pygame.quit() 
import pygame
import random
import math
from pygame import mixer

# initialize the pygame
pygame.init()

# create the screen
screen = pygame.display.set_mode((800, 600))

# background
background = pygame.image.load("space.png")

# background sound
mixer.music.load('background.wav')
mixer.music.play(-1)

# Title and Icon
pygame.display.set_caption("Attack Of The Space Cats")
icon = pygame.image.load('space-ship.png')
pygame.display.set_icon(icon)

# Player
PlayerImg = pygame.image.load('jet.png')
PlayerX = 370
PlayerY = 480
PlayerX_change = 0

# Enemy
EnemyImg = []
EnemyX = []
EnemyY = []
EnemyX_change = []
EnemyY_change = []
num_of_enemies = 7

for i in range(num_of_enemies):
    EnemyImg.append(pygame.image.load('cat.png'))
    EnemyX.append(random.randint(0, 735))
    EnemyY.append(random.randint(50, 150))
    EnemyX_change.append(3)
    EnemyY_change.append(40)

# Bullet
BulletImg = pygame.image.load('nuclear-bomb.png')
BulletX = 0
BulletY = 480
BulletX_change = 0
BulletY_change = 5.5
Bullet_State = "ready"

# nani missile
missleImg = pygame.image.load('missile.png')
missleX = 0
missleY = 480
missleX_change = 0
missleY_change = 1.5
missle_State = "ready"

# score
score_value = 0
font = pygame.font.Font('freesansbold.ttf', 32)

textX = 10
textY = 10

# game over text
gameOver_font = pygame.font.Font('freesansbold.ttf', 64)


def game_over_text():
    over_text = gameOver_font.render("GAME OVER", True, (255, 255, 255))
    screen.blit(over_text, (200, 250))


def show_Score(x, y):
    score = font.render("Score: " + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))


def player(x, y):
    screen.blit(PlayerImg, (x, y))


def enemy(x, y, i):
    screen.blit(EnemyImg[i], (x, y))


def fire_bullet(x, y):
    global Bullet_State
    Bullet_State = "fire"
    screen.blit(BulletImg, (x + 16, y + 10))


def fire_missle(x, y):
    global missle_State
    missle_State = "fire"
    screen.blit(missleImg, (x + 16, y + 10))


def isCollision(EnemyX, EnemyY, BulletX, BulletY):
    distance = math.sqrt(math.pow(EnemyX - BulletX, 2) + (math.pow(EnemyY - BulletY, 2)))
    if distance < 27:
        return True
    else:
        return False


def isCollide(EnemyX, EnemyY, missileX, missileY):
    dist = math.sqrt(math.pow(EnemyX - missileX, 2) + (math.pow(EnemyY - missileY, 2)))
    if dist < 27:
        return True
    else:
        return False


# Game Loop
running = True
while running:

    # RGB
    screen.fill((0, 0, 0))
    # background image
    screen.blit(background, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # keystroke detection
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                PlayerX_change = -5
            if event.key == pygame.K_d:
                PlayerX_change = 5
            if event.key == pygame.K_SPACE:
                if Bullet_State is "ready":
                    bullet_sound = mixer.Sound('laser.wav')
                    bullet_sound.play()
                    BulletX = PlayerX
                    fire_bullet(PlayerX, BulletY)
            if event.key == pygame.K_f:
                missle_sound = mixer.Sound('laser.wav')
                missle_sound.play()
                missleX = PlayerX
                fire_missle(PlayerX, missleY)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a or event.key == pygame.K_d:
                PlayerX_change = 0

    # player movement
    PlayerX += PlayerX_change
    if PlayerX <= 0:
        PlayerX = 0
    elif PlayerX >= 736:
        PlayerX = 736

    # enemy movement
    for i in range(num_of_enemies):

        # game over screen
        if EnemyY[i] > 440:
            for j in range(num_of_enemies):
                EnemyY[j] = 2000
            game_over_text()
            break

        EnemyX[i] += EnemyX_change[i]
        if EnemyX[i] <= 0:
            EnemyX_change[i] = 4
            EnemyY[i] += EnemyY_change[i]
        elif EnemyX[i] >= 736:
            EnemyX_change[i] = -4
            EnemyY[i] += EnemyY_change[i]

        # Collision
        collision = isCollision(EnemyX[i], EnemyY[i], BulletX, BulletY)
        if collision:
            collide_sound = mixer.Sound('explosion.wav')
            collide_sound.play()
            BulletY = 480
            Bullet_State = "ready"
            score_value += 1
            EnemyX[i] = random.randint(0, 735)
            EnemyY[i] = random.randint(50, 150)

        colision2 = isCollide(EnemyX[i], EnemyY[i], missleX, missleY)
        if colision2:
            collide_sound = mixer.Sound('explosion.wav')
            collide_sound.play()
            missleY = 480
            missle_State = "ready"
            score_value += 2
            EnemyX[i] = random.randint(0, 735)
            EnemyY[i] = random.randint(10, 120)
        enemy(EnemyX[i], EnemyY[i], i)

    # Bullet Movement
    if BulletY <= 0:
        BulletY = 480
        Bullet_State = "ready"

    if Bullet_State is "fire":
        fire_bullet(BulletX, BulletY)
        BulletY -= BulletY_change

    # missile movement
    if missleY <= 0:
        missleY = 480
        missle_State = "ready"

    if missle_State is "fire":
        fire_missle(missleX, missleY)
        missleY -= missleY_change

    player(PlayerX, PlayerY)
    show_Score(textX, textY)
    pygame.display.update()

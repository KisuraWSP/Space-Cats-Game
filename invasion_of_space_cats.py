import pygame
import os
import time
import random
from pygame import mixer

# background sound
pygame.init()
mixer.music.load("background.wav")
mixer.music.play(-1)

pygame.font.init()
# window
width, height = 650, 650
win = pygame.display.set_mode((width, height))
pygame.display.set_caption("Invasion Of The Space Cats")
icon = pygame.image.load(os.path.join("images", "cat3.png"))
pygame.display.set_icon(icon)

# Load images
cat1_enemy = pygame.image.load(os.path.join("images", "cat.png"))
cat_enemy2 = pygame.image.load(os.path.join("images", "cat2.png"))
cat_enemy3 = pygame.image.load(os.path.join("images", "cat3.png"))
cat_enemy4 = pygame.image.load(os.path.join("images", "cat4.png"))
cat_enemy5 = pygame.image.load(os.path.join("images", "cat5.png"))

# Player
player_char = pygame.image.load(os.path.join("images", "space-ship.png"))

# weapons_enemy
cat1_wep = pygame.image.load(os.path.join("images", "laser.png"))
cat2_wep = pygame.image.load(os.path.join("images", "bullet2.png"))
cat3_wep = pygame.image.load(os.path.join("images", "missile2.png"))
cat4_wep = pygame.image.load(os.path.join("images", "bullet.png"))
cat5_wep = pygame.image.load(os.path.join("images", "nuclear-bomb.png"))

# player_weapon
player_wep = pygame.image.load(os.path.join("images", "missile.png"))

# background
bg = pygame.image.load(os.path.join("images", "space2.png"))


class Laser:
    def __init__(self, x, y, img):
        self.x = x
        self.y = y
        self.img = img
        self.mask = pygame.mask.from_surface(self.img)

    def draw(self, window):
        window.blit(self.img, (self.x, self.y))

    def move(self, vel):
        self.y += vel

    def off_screen(self, height):
        return not (self.y < height and self.y >= 0)

    def collision(self, obj):
        return collide(obj, self)


class Ship:
    COOLDOWN = 30

    def __init__(self, xpos, ypos, health=100):
        self.x = xpos
        self.y = ypos
        self.health = health
        self.ship_img = None
        self.laser_img = None
        self.lasers = []
        self.cool_down_counter = 0

    def draw(self, window):
        window.blit(self.ship_img, (self.x, self.y))
        for laser in self.lasers:
            laser.draw(window)

    def moveLasers(self, vel, obj):
        self.cooldown()
        for laser in self.lasers:
            laser.move(vel)
            if laser.off_screen(height):
                self.lasers.remove(laser)
            elif laser.collision(obj):
                obj.health -= 10
                self.lasers.remove(laser)

    def cooldown(self):
        if self.cool_down_counter >= self.COOLDOWN:
            self.cool_down_counter = 0
        elif self.cool_down_counter > 0:
            self.cool_down_counter += 1

    def shoot(self):
        if self.cool_down_counter == 0:
            laser = Laser(self.x, self.y, self.laser_img)
            self.lasers.append(laser)
            self.cool_down_counter = 1

    def get_width(self):
        return self.ship_img.get_width()

    def get_height(self):
        return self.ship_img.get_height()


class Player(Ship):
    def __init__(self, xpos, ypos, health=100):
        super().__init__(xpos, ypos, health)
        self.ship_img = player_char
        self.laser_img = player_wep
        self.mask = pygame.mask.from_surface(self.ship_img)
        self.max_health = health

    def moveLasers(self, vel, objs):
        self.cooldown()
        for laser in self.lasers:
            laser.move(vel)
            if laser.off_screen(height):
                self.lasers.remove(laser)
            else:
                for obj in objs:
                    if laser.collision(obj):
                        objs.remove(obj)
                        if laser in self.lasers:
                            self.lasers.remove(laser)

    def draw(self, window):
        super().draw(window)
        self.health_bar(window)

    def health_bar(self, window):
        pygame.draw.rect(window, (255, 0, 0),
                         (self.x, self.y + self.ship_img.get_height() + 10, self.ship_img.get_width(), 10))
        pygame.draw.rect(window, (0, 255, 0), (
            self.x, self.y + self.ship_img.get_height() + 10,
            self.ship_img.get_width() * (self.health / self.max_health),
            10))


class Enemy(Ship):
    ENEMY_TYPE = {
        "cat_invader": (cat1_enemy, cat1_wep),
        "cat_brawler": (cat_enemy2, cat2_wep),
        "cat_devil": (cat_enemy3, cat3_wep),
        "cat_ultimato": (cat_enemy4, cat4_wep),
        "cat_airforce": (cat_enemy5, cat5_wep)
    }

    def __init__(self, xpos, ypos, type, health=100):
        super().__init__(xpos, ypos, health)
        self.ship_img, self.laser_img = self.ENEMY_TYPE[type]
        self.mask = pygame.mask.from_surface(self.ship_img)

    def move(self, vel):
        self.y += vel

    def shoot(self):
        if self.cool_down_counter == 0:
            laser = Laser(self.x - 10, self.y, self.laser_img)
            self.lasers.append(laser)
            self.cool_down_counter = 1


def collide(obj1, obj2):
    offset_x = obj2.x - obj1.x
    offset_y = obj2.y - obj1.y
    return obj1.mask.overlap(obj2.mask, (offset_x, offset_y)) != None


# main loop
def main(score=None):
    run = True
    fps = 60
    level = 0
    lives = 3
    main_font = pygame.font.SysFont("comicsans", 50)
    lost_font = pygame.font.SysFont("comicsans", 60)
    score_font = pygame.font.SysFont("comicsans", 32)
    enemies = []
    wave_length = 3
    enemy_vel = 1

    player_vel = 5
    laser_vel = 4
    player = Player(300, 550)

    clock = pygame.time.Clock()
    lost = False
    lost_count = 0

    def reDrawWindow():
        win.blit(bg, (0, 0))
        # draw text
        lives_label = main_font.render(f"lives: {lives}", 1, (255, 255, 255))
        level_label = main_font.render(f"level: {level}", 1, (255, 255, 255))

        win.blit(lives_label, (10, 10))
        win.blit(level_label, (width - level_label.get_width() - 10, 10))

        for enemy in enemies:
            enemy.draw(win)

        player.draw(win)
        if lost:
            lost_label = lost_font.render("GAME OVER!", 1, (255, 255, 255))
            # score_label = score_font.render(f"score: {score}", 1, (255, 0, 0))
            win.blit(lost_label, (width / 2 - lost_label.get_width() / 2, 270))
            # win.blit(score_label,(width / 2 - score_label.get_width() / 2, 340))

        pygame.display.update()

    while run:
        clock.tick(fps)
        reDrawWindow()
        if lives <= 0 or player.health <= 0:
            lost = True
            lost_count += 1

        if lost:
            if lost_count > fps * 3:
                run = False
            else:
                continue

        if len(enemies) == 0:
            level += 1
            enemy_vel += 1
            wave_length += 5
            for i in range(wave_length):
                enemy = Enemy(random.randrange(50, width - 100), random.randrange(-1500, -100),
                              random.choice(
                                  ["cat_invader", "cat_brawler", "cat_devil", "cat_ultimato", "cat_airforce"]))
                enemies.append(enemy)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_a] and player.x - player_vel > 0:  # left
            player.x -= player_vel
        if keys[pygame.K_d] and player.x + player_vel + player.get_width() < width:  # right
            player.x += player_vel
        if keys[pygame.K_w] and player.y - player_vel > 0:  # up
            player.y -= player_vel
        if keys[pygame.K_s] and player.y + player_vel + player.get_height() + 15 < height:  # down
            player.y += player_vel

        if keys[pygame.K_SPACE]:
            missle_sound = mixer.Sound("laser.wav")
            missle_sound.play()
            player.shoot()

        for enemy in enemies[:]:
            enemy.move(enemy_vel)
            enemy.moveLasers(laser_vel, player)

            if random.randrange(0, 250) == 1:
                # enemy_shooting = mixer.Sound("laser.wav")
                # enemy_shooting.play()
                enemy.shoot()

            if collide(enemy, player):
                player.health -= 10
                explosion = mixer.Sound("explosion.wav")
                explosion.play()

                enemies.remove(enemy)

            elif enemy.y + enemy.get_height() > height:
                lives -= 1
                enemies.remove(enemy)

        player.moveLasers(-laser_vel, enemies)


def main_menu():
    t_font = pygame.font.SysFont("comicsans", 70)
    title_font = pygame.font.SysFont("comicsans", 50)
    run = True
    while run:
        win.blit(bg, (0, 0))
        title_label = title_font.render("Invasion Of The Space Cats", 1, (255, 0, 0))
        t_label = t_font.render("Press the Mouse to begin", 1, (255, 255, 255))
        win.blit(title_label, (width / 2 - title_label.get_width() / 2, 250))
        win.blit(t_label, (width / 2 - t_label.get_width() / 2, 350))
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                main()

    pygame.quit()


main_menu()

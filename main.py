from pygame import *

# time - дає кількість секунд, що пройшла з 1970р
from time import time as time_count
from random import randint

init()
mixer.init()
window = display.set_mode((700, 600))
display.set_caption("SpaceShooter")
background = transform.scale(image.load("res/galaxy.jpg"), (700, 600))
window.blit(background, (0, 0))
mixer.music.load('res/space.ogg')
# mixer.music.play()
clock = time.Clock()


class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, size, player_speed=0):
        super().__init__()
        # (65, 65)
        self.image = transform.scale(image.load(player_image), size)
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y

    def draw_sprite(self):
        window.blit(self.image, (self.rect.x, self.rect.y))


start_time = time_count()  # засікти час


class Player(GameSprite):

    def update(self, bullets):  # bullets - список куль
        global start_time
        pressed_keys = key.get_pressed()  # Отримати клавіші, які натиснуті
        if pressed_keys[K_a]:
            self.rect.x -= self.speed  # переміститися вгору
        if pressed_keys[K_d]:
            self.rect.x += self.speed
        if pressed_keys[K_SPACE] and time_count() - start_time >= 1:  # якщо пробіл і якщо пройшла секунда
            bullets.add(Bullet('res/bullet.png', self.rect.x + 25, self.rect.y, (10, 20), 10))
            start_time = time_count()  # засікти час


class Bullet(GameSprite):

    def update(self):
        self.rect.y -= self.speed
        self.draw_sprite()


class Enemy(GameSprite):

    def update(self):  # ця функція буде для руху і обробки чогось
        global life
        self.rect.y += self.speed
        self.draw_sprite()
        if self.rect.y > 600:  # якщо монстр вийшов за межі екрану
            self.kill()  # вбити його


def draw_label(score):
    image = font.SysFont("Century Gothic", 20).render("Ворогів вбито " + str(score), True, (255, 255, 255))
    window.blit(image, (20, 50))
lives = 3

def draw_heart():
    global lives
    x = 50
    for i in range(lives):
        heart = transform.scale(image.load('res/IMG_4587.PNG'), (20, 20))
        window.blit(heart, x, 20)
        x += 30
rocket = Player('res/rocket.png', 250, 480, (60, 100), 5)

game = True

bullets = sprite.Group()
enemies_group = sprite.Group()  # Група працює лише зі спрайтами, заснованими на вбудованому Sprite

# створюю ворогів
score = 0
life = 3
# len(enemies_group) - дізнатись кількість ворогів у групі
while game:
    if len(enemies_group) < 7:
        new_enemy = Enemy('res/ufo.png', randint(0, 600), -100, (80, 50), 1)
        for s in enemies_group.sprites():
            if s.rect.colliderect(new_enemy.rect):
                new_enemy = Enemy('res/ufo.png', randint(0, 600), -100, (80, 50), 1)
        enemies_group.add(new_enemy)

    for e in event.get():
        if e.type == QUIT:
            game = False

    sprite.groupcollide(bullets, enemies_group, True, True)
    window.blit(background, (0, 0))
    bullets.update()

    rocket.update(bullets)
    rocket.draw_sprite()
    enemies_group.update()
    draw_label(score)
    display.update()
    clock.tick(60)



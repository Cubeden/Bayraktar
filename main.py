from pygame import *
from random import uniform
from random import randint, random
from time import time as timer

init()
font.init()
mixer.init()

W_mw = 1000
H_mw = 1000

mw = display.set_mode((W_mw, H_mw))
back = ((52, 162, 35))
mw.fill(back)
clock = time.Clock()

fire = mixer.Sound('sounds/fire.mp3')

class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, player_speed, w, h):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (w, h))
        # self.color = color
        # self.image = Surface((w, h))
        # self.image.fill(self.color)
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y

    def reset(self):
        mw.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def move(self):
        key_p = key.get_pressed()
        if key_p[K_LEFT] and self.rect.x > 0:
            self.rect.x -= self.speed

        if key_p[K_RIGHT] and self.rect.x < 1000:
            self.rect.x += self.speed

        if key_p[K_UP] and self.rect.y > 0:
            self.rect.y -= self.speed

        if key_p[K_DOWN] and self.rect.y < 1000:
            self.rect.y += self.speed

    def fire(self):
        bullet = Bullet('img/tank.png', self.rect.x + 21, self.rect.y, 0, 100, 100)
        bullets.add(bullet)

class Bullet(GameSprite):
    def update(self):
        # if time_after - last_shoot = 5:
        #     self.kill()
        if kill_bullet == True:
            self.kill()


class Object(sprite.Sprite):
    def __init__(self, x, y, W, H, color):
        super().__init__()
        self.color = color
        self.image = Surface((W, H))
        self.image.fill(self.color)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def draw_object(self):
        mw.blit(self.image, (self.rect.x, self.rect.y))

class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y >= 1000:
            self.speed = 2
            self.rect.y = -80
            self.x = randint(1, 2)
            if self.x == 1:
                self.rect.x = 310
            else:
                self.rect.x = 610

    def reset(self):
        mw.blit(self.image, (self.rect.x, self.rect.y))

objects = sprite.Group()
enemys = sprite.Group()
bullets = sprite.Group()

road_left = Object(300, 0, 100, 1000, (60, 60, 60))
road_right = Object(600, 0, 100, 1000, (60, 60, 60))
post_left = Object(250,  950, 200, 50, (80, 80, 80))
post_right = Object(550,  950, 200, 50, (80, 80, 80))

for i in range(8):
    random_side_x = randint(1, 2)
    if random_side_x == 1:
        side = 310
    else:
        side = 610

    e1 = Enemy("img/tank.png", side, -80, 2, 80, 160)
    enemys.add(e1)

objects.add(road_left, road_right, post_left, post_right)

p = Player("img/player.png", 100, 416, 10, 230, 175) 

num_fire = 0
rel_time = False
kill_bullet = False

game = True
while game:
    for e in event.get():
        if e.type == QUIT:
            game = False

        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                if num_fire <= 1 and rel_time == False:
                    num_fire += 1
                    fire.play()
                    p.fire()
                    kill_bullet = False

                if num_fire >= 1 and rel_time == False:
                    rel_time = True
                    last_shoot = timer()

    mw.fill(back)
    enemys.draw(mw)
    enemys.update()
    for o in objects:
        o.draw_object()
    objects.update()
    for e in enemys:
        e.reset()
    bullets.draw(mw)
    bullets.update()
    p.move()
    p.reset()

    if rel_time:
        now_time = timer()
        if now_time - last_shoot < 3:
            reload_shoot = font.Font(None, 36).render('RELOADING...', True, (255, 0, 0))
            mw.blit(reload_shoot, (W_mw - 290, 440))

        else:
            num_fire = 0
            rel_time = False
            kill_bullet = True


    key_p = key.get_pressed()
    
    if sprite.spritecollide(p, enemys, False) and key_p[K_SPACE]: 
        collides = sprite.spritecollide(p, enemys, True)
        e1 = Enemy("img/tank.png", side, -80, 2, 80, 160)
        enemys.add(e1)
        

    display.update()
    clock.tick(60)
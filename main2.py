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
back =  transform.scale(image.load('img/background.png'), (W_mw, H_mw))
clock = time.Clock()

fire = mixer.Sound('sounds/fire.mp3')

class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, player_speed, w, h):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (w, h))
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
        bullet = Bullet('img/fire.png', self.rect.x, self.rect.y, 0, 230, 175)
        bullets.add(bullet)

class Bullet(GameSprite):
    def update(self):
        if kill_bullet == True:
            self.kill()


class Object(sprite.Sprite):
    def __init__(self, object_image, x, y, W, H):
        super().__init__()
        self.image = transform.scale(image.load(object_image), (W, H))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def draw_object(self):
        mw.blit(self.image, (self.rect.x, self.rect.y))

class Enemy(GameSprite):
    # def update(self):
    #     self.rect.y += self.speed
    #     if self.rect.y >= 1000:
    #         self.speed = 2
    #         self.rect.y = -80
    #         self.x = randint(1, 2)
    #         if self.x == 1:
    #             self.rect.x = 310
    #         else:
    #             self.rect.x = 610

    def update(self):
        if self.rect.y < 1000:
            self.rect.y += self.speed

        if self.rect.y >= 800:
            self.kill()

    def reset(self):
        mw.blit(self.image, (self.rect.x, self.rect.y))

objects = sprite.Group()
enemys = sprite.Group()
bullets = sprite.Group()

road_left = Object("img/road.png", 275, 0, 150, 1000)
road_right = Object("img/road.png" , 575, 0, 150, 1000)
post_left = Object("img/kpp.png" , 275,  925, 250, 75)
post_right = Object("img/kpp.png" , 575,  925, 250, 75)

# for i in range(8):
#     random_side_x = randint(1, 2)
#     if random_side_x == 1:
#         side = 310
#     else:
#         side = 610

#     e1 = Enemy("img/tank.png", side, -80, 2, 80, 160)
#     enemys.add(e1)

def gen_start():
    global spawn_time
    global spawn_timer
    e1 = Enemy("img/tank2.png", 310, -200, 1, 80, 200)
    e2 = Enemy("img/tank2.png", 610, -200, 1, 80, 200)
    enemys.add(e1, e2)
    spawn_time = True
    spawn_timer = timer()

def gen2():
    global spawn_time
    global spawn_timer
    e1 = Enemy("img/tank2.png", 310, -200, 1, 80, 200)
    e2 = Enemy("img/tank2.png", 610, -200, 1, 80, 200)
    enemys.add(e1, e2)
    spawn_time = True
    spawn_timer = timer()

def spawn_random():
    global spawn_time
    global spawn_timer
    r_s = randint(1, 3)
    
    if r_s == 1:
        e1 = Enemy("img/tank2.png", 310, -200, 1, 80, 200)
        e2 = Enemy("img/tank2.png", 610, -200, 1, 80, 200)
        enemys.add(e1, e2)
        spawn_time = True
        spawn_timer = timer()

    if r_s == 2:
        e1 = Enemy("img/tank2.png", 310, -200, 1, 80, 200)
        e2 = Enemy("img/barak.png", 610, -440, 1, 80, 200)
        enemys.add(e1, e2)
        spawn_time = True
        spawn_timer = timer()

    if r_s == 3:
        e1 = Enemy("img/tank2.png", 310, -440, 1, 80, 200)
        e2 = Enemy("img/tank2.png", 610, -200, 1, 80, 200)
        enemys.add(e1, e2)
        spawn_time = True
        spawn_timer = timer()


# e1 = Enemy("img/tank.png", 310, -80, 2, 80, 160)
# enemys.add(e1)

objects.add(road_left, road_right, post_left, post_right)

p = Player("img/player.png", 100, 416, 3, 230, 175) 

num_fire = 0
score = 0
rel_time = False
kill_bullet = False
spawn_time = False
score_time = False

def score_plus():
    global score_timer
    global score_time
    score_time = True
    score_timer = timer()

gen_start()
score_plus()



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

    mw.blit(back, (0,0))
    score_txt = font.Font(None, 36).render('Очки: ' + str(score), True, (0, 255, 0))
    mw.blit(score_txt, (10, 10))
    # enemys.draw(mw)
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
        if now_time - last_shoot > 3:
            reload_shoot = font.Font(None, 36).render('RELOADING...', True, (255, 0, 0))
            mw.blit(reload_shoot, (W_mw - 290, 440))

        else:
            num_fire = 0
            rel_time = False
            kill_bullet = True

    if spawn_time:
        spawn_now = timer()
        if spawn_now - spawn_timer > 8:
            spawn_random()

    if score_time:
        score_now = timer()
        if score_now - score_timer > 1:
            score += 5
            score_plus()



    key_p = key.get_pressed()
    
    if sprite.spritecollide(p, enemys, False) and key_p[K_SPACE]:
        collides = sprite.spritecollide(p, enemys, True)
        if collides:
            score += 50
        

    display.update()
    clock.tick(60)
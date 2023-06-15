#Создай собственный Шутер!

from pygame import *
from random import randint
from time import time as timer
mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()
fire_sound = mixer.Sound("fire.ogg")
window = display.set_mode((700,500))
clock=time.Clock()
FPS = 120
display.set_caption('Космос')
background = transform.scale(image.load('aaaa.jpg'),(700,500))
game = True

class GameSprite(sprite.Sprite):
   def __init__(self,player_image,player_x,player_y,player_speed,width,height):
       
      super().__init__()
      self.image = transform.scale(image.load(player_image),(width,height))
      self.speed =  player_speed
      self.rect = self.image.get_rect()
      self.rect.x = player_x
      self.rect.y = player_y
   def reset(self):
      window.blit(self.image,(self.rect.x, self.rect.y))

class Player(GameSprite):
    def update(self):
        keys_pressed = key.get_pressed()
        if keys_pressed[K_LEFT] and self.rect.x :
            self.rect.x -= self.speed
        if keys_pressed[K_RIGHT] and self.rect.x < 700 -65:
            self.rect.x += self.speed
        if keys_pressed[K_RIGHT] and self.rect.x < width:
            self.rect.x += self.speed

    def fire(self):
        fire_sound.play()
        bullet = Bullet('bullet.png',self.rect.centerx,self.rect.top,10,12,24)
        bullets.add(bullet)

class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global missed, missed_text
        if self.rect.y >500:
            self.rect.y = -40
            self.rect.x = randint(10,650)
            missed = missed + 1
            missed_text = font1.render(f'Missed:{missed}',True,(255,255,255))
class Asteroids(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global missed, missed_text
        if self.rect.y >500:
            self.rect.y = -40
            self.rect.x = randint(10,650)
            missed = missed + 1
            missed_text = font1.render(f'Missed:{missed}',True,(255,255,255))
class Bullet(GameSprite):
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y < -10:
            self.kill()
bullets = sprite.Group()
monsters = sprite.Group()
asteroids = sprite.Group()
for i in range(3):
    s = Enemy("asteroid.png",  randint(0,650),0, randint(2,8),75,100)
    asteroids.add(s)
for i in range(5):
    m = Enemy ("1111.png",  randint(0,650),0, randint(2,8),75,100)
    monsters.add(m)

missed = 0 
font.init()
font1 = font.SysFont('jokerman',20)
score_text = font1.render(f'Score:{0}',True,(255,255,255))
font2 = font.SysFont('jokerman',20)
missed_text = font2.render(f'Missed:{missed}',True,(255,255,255))

hero = Player('rocket.png',0,300,75-65, 45,125)
enemy = Enemy('1111.png',0,0,500-65,55,130)
score = 0
finish = False
num_fires = 0
rel_time = False
while game:
    for e in event.get():
        if e.type == QUIT:
            game=False
        if e.type == KEYDOWN and e.key == K_SPACE:
            if rel_time == False and num_fires < 15:
                player.fire()
                num_fires += 1
            if num_fires > 5 and rel_time == False:
                rel_time = True
                last_time = timer()
    if not finish:
        if rel_time == True:
            now_time = timer()
            if now_time - last_time < 1:
                reload = font2.render('Reloading ...',1,(150,0,0))
                window.blit(reload,(260,460))
            else:
                num_fires = 0
                rel_time = False
        bullets_monsters = sprite.groupcollide(bullets,monsters,True,True)
        for i in bullets_monsters:
            m = Enemy ("1111.png",  randint(0,650),-40, randint(2,8),75,100)
            monsters.add(m)
            score += 1
            score_text = font2.render(f'Score:{score}',True,(255,255,255))
            window.blit(score_text,(0,0))
        player_monsters = sprite.spritecollide(hero,monsters,False)
        if player_monsters:
            window.blit(font2.render('YOU DIED!!!',True,(255,0,0)),(250,250))
            finish = True
        if missed > 45:
            finish = True            
        window.blit(background, (0,0))
        asteroids.draw(window)
        asteroids.update()
        hero.update()
        hero.reset()
        bullets.update()
        bullets.draw(window)
        monsters.update()
        monsters.draw(window)
        window.blit(score_text,(10,10))
        window.blit(missed_text,(10,50))
    clock.tick(FPS)
    display.update()

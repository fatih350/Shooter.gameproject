from pygame import *
from random import randint
from time import \
    time as timer

#Arka Plan Müziği
mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()
fire_sound = mixer.Sound('fire.ogg')

#Yazı
font.init()
font1 = font.Font(None, 80)
win = font1.render('YOU WIN!!!!   :)', True, (255,255,255)) #beyaz renk
lose = font1.render('YOU LOSE!!!!  :(', True, (180,0,0)) #bordu renk
font2 = font.Font(None, 36)

#Görseller
img_back = "galaxy.jpg" #arkaplan
img_hero = "rocket.png" #kahraman
img_bullet = "bullet.png" #mermi
img_enemy = "ufo.png" #düşman
img_ast = "asteroid.png" #engel

score = 0 #vurulan gemiler
lost = 0 #kaçırılan ufolar
goal = 10 #kazanmak için vurulması gerekilen düşman sayısı
max_lost = 3 #kaçırılabilecek maximum ufo sayısı
life = 3 #kahramanın can sayısı


#Sprite Sınıfı
class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        sprite.Sprite.__init__(self)

        self.image = transform.scale(image.load(player_image),(size_x,size_y))
        self.speed = player_speed

        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y

    def reset(self):
        window.blit(self.image,(self.rect.x,self.rect.y))

#Kahraman (ana oyuncu) Sınıfı
class Player(GameSprite):
    #Ok tuşları ile kontrol sağlama
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < win_width - 80:
            self.rect.x += self.speed

    #Atış yöntemi
    def fire(self):
        bullet = Bullet(img_bullet, self.rect.centerx, self.rect.top,15,20,-15)
        bullets.add(bullet)

class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost

        #ekranın en alt kısmına gelince kaybolması için
        if self.rect.y > win_height:
            self.rect.x = randint(80, win_width - 80)
            self.rect.y = 0
            lost = lost + 1

#Mermi sınıfı
class Bullet(GameSprite):
    def update(self):
        self.rect.y += self.speed
        #Ekranın üst kısmına ulaşan mermileri yok etme
        if self.rect.y < 0:
            self.kill()


#Pencere oluşturuyorum
win_width = 700
win_height = 500
display.set_caption("Shooter - Mizgin DURĞUN")
window = display.set_mode((win_width,win_height))
background = transform.scale(image.load(img_back),(win_width,win_height))

#sprite oluştuduk
ship = Player(img_hero, 5, win_height - 100, 80, 100, 10)

#bir grup halinde aprite oluşturuyorum
monsters = sprite.Group()

for i in range(1, 6):
    monster = Enemy(img_enemy, randint(80, win_width - 80), -40, 80, 50, randint(1,5))
    monsters.add(monster)
bullets = sprite.Group()

asteroids = sprite.Group()
for i in range(1,3):
    asteroid = Enemy(img_ast, randint(30, win_width-30),-40,80,50,randint(1,7))
    asteroids.add(asteroid)

finish = False
run = True
rel_time = False
num_fire = 0

while run:
    for e in event.get():
        if e.type == QUIT:
            run = False
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                if num_fire < 5 and rel_time == False:
                    num_fire = num_fire + 1
                    fire_sound.play()
                    ship.fire()

                if num_fire >= 5 and rel_time == False:
                    last_time = timer()
                    rel_time = True


        if not finish:
            window.blit(background,(0,0))

            ship.update()
            monsters.update()
            bullets.update()
            asteroids.update()

            ship.reset()
            monsters.draw(window)
            bullets.draw(window)
            asteroids.draw(window)

            if rel_time == True:
                now_time = timer()

                if now_time - last_time < 3:
                    reload = font2.render("Wait, reload ...",1,(150,0,0))
                    window.blit(reload,(260,460))

                else:
                    num_fire = 0
                    rel_time = False

            collides = sprite.groupcollide(monsters, bullets, True, True)

            for c in collides:
                score = score + 1
                monster = Enemy(img_enemy, randint(80, win_width - 80), -40, 80, 50, randint(1,5))
                monsters.add(monster)

    if sprite.spritecollide(ship, monsters, False) or sprite.spritecollide(ship,asteroids,False):
        sprite.spritecollide(ship,monsters,True)
        sprite.spritecollide(ship,asteroids,True)
        life = life - 1

    if life == 0 or lost >= max_lost:
        finish = True
        window.blit(lose,(200,200))

    if score >= goal:
        finish = True
        window.blit(win,(200,200))

    text = font2.render("Skor: " + str(score), 1, (255, 255, 255))
    window.blit(text, (10, 20))

    text_lose = font2.render("Kaybetme: " + str(lost), 1, (255, 255, 255))
    window.blit(text_lose, (10, 50))

    if life == 3:
        life_color = (0,150, 0)
    if life == 2:
        life_color = (150, 150, 0)
    if life == 1:
        life_color = (150, 150, 0)

    text_life = font1.render(str(life),1,life_color)
    window.blit(text_life,(650,10))

    display.update()

else:
    finish = False
score = 0
lost = 0
num_fire = 0
life = 3
for b in bullets:
    b.kill()
for m in monsters:
    m.kill()
for a in asteroids:
    a.kill()

time.delay(3000)
for i in range(1,6):
    monster = Enemy(img_enemy, randint(80, win_width-80),-40, 80, 50, randint(1,5))
    monsters.add(monster)
for i in range(1,3):
    asteroid = Enemy(img_ast, randint(30,win_width-30),-40,80,50,randint(1,7))
    asteroids.add(asteroid)

time.delay(50)

import pygame
import pygame.freetype
import sys
import os

'''
Variables
'''
worldx = 960
worldy = 720
fps = 40
ani = 4
tx = 64
ty = 64
world = pygame.display.set_mode([worldx, worldy])
forwardx = 600
backwardx = 230
size = worldx, worldy
screen = pygame.display.set_mode(size)

BLUE  = (25, 25, 200)
BLACK = (23, 23, 23)
WHITE = (254, 254, 254)
ALPHA = (0, 255, 0)

font_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "fonts", "serif.otf")
font_size = tx
pygame.freetype.init()
myfont = pygame.freetype.Font(font_path, font_size)

'''
Objects
'''
def stats(score,health):
   myfont.render_to(world, (4, 4), "Powercubes:"+str(score), BLUE, None, size=35)
   myfont.render_to(world, (4, 50), "Health:"+str(health), BLUE, None, size=35)

class Platform(pygame.sprite.Sprite):
   def __init__(self, xloc, yloc, imgw, imgh, img):
       pygame.sprite.Sprite.__init__(self)
       self.image = pygame.image.load(os.path.join('images', img)).convert()
       self.image.convert_alpha()
       self.image.set_colorkey(ALPHA)
       self.rect = self.image.get_rect()
       self.rect.y = yloc
       self.rect.x = xloc
       self.imgw = imgw
       self.imgh = imgh

class Player(pygame.sprite.Sprite):
   def __init__(self):
       pygame.sprite.Sprite.__init__(self)
       self.movex = 0
       self.movey = 0
       self.frame = 0
       self.images = []
       self.frame = 0
       self.health = 10
       self.damage = 0
       self.score = 0
       self.is_jumping = True
       self.is_falling = False

       for i in range(1, 5):
           img = pygame.image.load(os.path.join('images', 'hero' + str(i) + '.png')).convert()
           img.convert_alpha()  # optimise alpha
           img.set_colorkey(ALPHA)  # set alpha
           self.images.append(img)
           self.image = self.images[0]
           self.rect = self.image.get_rect()

   def gravity(self):
       if self.is_jumping:
           self.movey += 3.2

   def jump(self):
       if self.is_jumping is False:
           self.is_falling = False
           self.is_jumping = True

   def control(self,x,y):
       self.movex += x

   def update(self):
       if self.movex < 0:
           self.is_jumping = True
           self.frame += 1
           if self.frame > 3 * ani:
               self.frame = 0
           self.image = pygame.transform.flip(self.images[self.frame // ani], True, False)

       # moving right
       if self.movex > 0:
           self.is_jumping = True
           self.frame += 1
           if self.frame > 3 * ani:
               self.frame = 0
           self.image = self.images[self.frame // ani]

       # collisions
       enemy_hit_list = pygame.sprite.spritecollide(self, enemy_list, False)
       if self.damage == 0:
           for enemy in enemy_hit_list:
               if not self.rect.contains(enemy):
                   self.damage = self.rect.colliderect(enemy)
       if self.damage == 1:
           idx = self.rect.collidelist(enemy_hit_list)
           if idx == -1:
               self.damage = 0
               self.health -= 1

       ground_hit_list = pygame.sprite.spritecollide(self, ground_list, False)
       for g in ground_hit_list:
           self.movey = 0
           self.rect.bottom = g.rect.top
           self.is_jumping = False

       # fall off the world
       if self.rect.y > worldy:
           self.health -=1
           print(self.health)
           self.rect.x = tx
           self.rect.y = ty

       plat_hit_list = pygame.sprite.spritecollide(self, plat_list, False)
       for p in plat_hit_list:
           self.is_jumping = False
           self.movey = 0
           if self.rect.bottom <= p.rect.bottom:
              self.rect.bottom = p.rect.top
           else:
              self.movey += 3.2

       if self.is_jumping and self.is_falling is False:
           self.is_falling = True
           self.movey -= 33  # how high to jump

       loot_hit_list = pygame.sprite.spritecollide(self, loot_list, False)
       for loot in loot_hit_list:
           loot_list.remove(loot)
           self.score += 1

       self.rect.x += self.movex
       self.rect.y += self.movey


class Enemy(pygame.sprite.Sprite):
   def __init__(self, x, y, speed, movement, img):
       pygame.sprite.Sprite.__init__(self)
       self.image = pygame.image.load(os.path.join('images', img))
       self.image.convert_alpha()
       self.image.set_colorkey(ALPHA)
       self.rect = self.image.get_rect()
       self.rect.x = x
       self.rect.y = y
       self.counter = 0
       self.speed = speed
       self.movement = movement
       self.increment = 0

   def move(self):
       '''
       enemy movement
       '''
       if self.movement == 'sidefast1':
           distance = 80
           speed = self.speed

           if 0 <= self.counter < distance:
               self.rect.x += speed
           elif self.counter == distance:
               self.image = pygame.transform.flip(self.image, True, False)
           elif distance < self.counter < distance*2:
               self.rect.x -= speed
           elif self.counter == distance*2:
               self.image = pygame.transform.flip(self.image, True, False)
           else:
               self.counter = 0
           self.counter += 1

       if self.movement == 'sidefast2':
           distance = 100
           speed = self.speed

           if 0 <= self.counter < distance:
               self.rect.x += speed
           elif self.counter == distance:
               self.image = pygame.transform.flip(self.image, True, False)
           elif distance < self.counter < distance*2:
               self.rect.x -= speed
           elif self.counter == distance*2:
               self.image = pygame.transform.flip(self.image, True, False)
           else:
               self.counter = 0
           self.counter += 1

       elif self.movement == 'sideslow':
           distance = 40
           speed = self.speed

           if 0 <= self.counter <= distance:
               self.rect.x += speed
           elif distance <= self.counter <= distance * 2:
               self.rect.x -= speed
           else:
               self.counter = 0
           self.counter += 1

       elif self.movement == 'updownshort':
           distance = 50
           speed = self.speed

           if 0 <= self.counter <= distance:
               self.rect.y += speed
           elif distance <= self.counter <= distance * 2:
               self.rect.y -= speed
           else:
               self.counter = 0
           self.counter += 1

       elif self.movement == 'updownmed':
           distance = 75
           speed = self.speed

           if 0 <= self.counter <= distance:
               self.rect.y += speed
           elif distance <= self.counter <= distance * 2:
               self.rect.y -= speed
           else:
               self.counter = 0
           self.counter += 1

       elif self.movement == 'updownlong':
           distance = 100
           speed = self.speed

           if 0 <= self.counter <= distance:
               self.rect.y += speed
           elif distance <= self.counter <= distance * 2:
               self.rect.y -= speed
           else:
               self.counter = 0
           self.counter += 1

       elif self.movement == 'zigzag':
           distance = 150
           speed = self.speed

           if self.counter % 2 == 0 and self.counter < distance:
               self.rect.x += speed
           elif self.counter % 2 != 0 and self.counter < distance:
               self.rect.y += speed
           elif self.counter == distance:
               self.image = pygame.transform.flip(self.image, True, False)
           elif self.counter % 2 == 0 and self.counter < distance*2:
               self.rect.x -= speed
           elif self.counter % 2 != 0 and self.counter < distance*2:
               self.rect.y -= speed
           elif self.counter == distance*2:
               self.image = pygame.transform.flip(self.image, True, False)
           else:
               self.counter = 0
           self.counter += 1

       elif self.movement == 'swirl':
           distance = 100

           #forward
           if 0 <= self.counter < distance/4:
               self.rect.x += 4
               self.rect.y += 5
           elif distance/4 <= self.counter < distance/2:
               self.rect.x += 4
               self.rect.y -= 5
           elif distance/2 <= self.counter < 0.75*distance:
               self.rect.x += 4
               self.rect.y += 5
           elif 0.75*distance <= self.counter < distance:
               self.rect.x += 4
               self.rect.y -= 5
           elif distance <= self.counter < 1.25*distance:
               self.rect.x += 4
               self.rect.y += 5
           #backward
           elif self.counter == 1.25*distance:
               self.image = pygame.transform.flip(self.image, True, False)
           elif 1.25*distance < self.counter < 1.5*distance:
               self.rect.x -= 4
               self.rect.y -= 5
           elif 1.5*distance <= self.counter < 1.75*distance:
               self.rect.x -= 4
               self.rect.y += 5
           elif 1.75*distance <= self.counter < 2*distance:
               self.rect.x -= 4
               self.rect.y -= 5
           elif 2*distance <= self.counter < 2.25*distance:
               self.rect.x -= 4
               self.rect.y += 5
           elif 2.25*distance <= self.counter < 2.5*distance:
               self.rect.x -= 4
               self.rect.y -= 5
           elif self.counter == 2.5*distance:
               self.image = pygame.transform.flip(self.image, True, False)
           else:
               self.counter = 0
           self.counter += 1

       elif self.movement == 'swirl1':
           distance = 200

           #forward
           if 0 <= self.counter < distance/4:
               self.rect.x += 4
               self.rect.y += 6
           elif distance/4 <= self.counter < distance/2:
               self.rect.x += 4
               self.rect.y -= 6
           elif distance/2 <= self.counter < 0.75*distance:
               self.rect.x += 4
               self.rect.y += 6
           elif 0.75*distance <= self.counter < distance:
               self.rect.x += 4
               self.rect.y -= 6
           elif distance <= self.counter < 1.25*distance:
               self.rect.x += 4
               self.rect.y += 6
           #backward
           elif self.counter == 1.25*distance:
               self.image = pygame.transform.flip(self.image, True, False)
           elif 1.25*distance < self.counter < 1.5*distance:
               self.rect.x -= 4
               self.rect.y -= 6
           elif 1.5*distance <= self.counter < 1.75*distance:
               self.rect.x -= 4
               self.rect.y += 6
           elif 1.75*distance <= self.counter < 2*distance:
               self.rect.x -= 4
               self.rect.y -= 6
           elif 2*distance <= self.counter < 2.25*distance:
               self.rect.x -= 4
               self.rect.y += 6
           elif 2.25*distance <= self.counter < 2.5*distance:
               self.rect.x -= 4
               self.rect.y -= 6
           elif self.counter == 2.5*distance:
               self.image = pygame.transform.flip(self.image, True, False)
           else:
               self.counter = 0
           self.counter += 1

       elif self.movement == None:
           pass

class Level():
   def bad(lvl,eloc):
       if lvl == 1:
           enemy1 = Enemy(eloc[0],eloc[1], 2, 'sideslow', 'seadragon.png') # spawn enemy
           enemy2 = Enemy(100, 250, 8, 'sidefast1', 'flyingmon.png')
           enemy3 = Enemy(1010, 595, 1, None, 'spike.png')
           enemy4 = Enemy(1080, 595, 1, None, 'spike.png')
           enemy5 = Enemy(1150, 595, 1, None, 'spike.png')
           enemy6 = Enemy(1325, 200, 1, None, 'spike.png')
           enemy7 = Enemy(1395, 200, 1, None, 'spike.png')
           enemy8 = Enemy(1465, 200, 1, None, 'spike.png')
           enemy9 = Enemy(1535, 200, 1, None, 'spike.png')
           enemy10 = Enemy(150, 300, 10, 'sidefast2', 'flyingmon.png')
           enemy11 = Enemy(700, 350, 5, 'sidefast1', 'flyingmon.png')
           enemy12 = Enemy(1350, 125, 5, 'updownmed', 'blade.png')
           enemy13 = Enemy(1440, 150, 3, 'updownlong', 'blade.png')
           enemy14 = Enemy(1520, 175, 3, 'updownmed', 'blade.png')
           enemy15 = Enemy(1590, 150, 4, 'updownlong', 'blade.png')
           enemy16 = Enemy(1850, 250, 4, 'zigzag', 'ghost.png')
           enemy17 = Enemy(1950, 125, 5, 'sideslow', 'brownbird.png')
           enemy18 = Enemy(2580, 25, 7, 'sidefast1', 'red.png')
           enemy19 = Enemy(2600, 25, 6, 'updownlong', 'brownbird.png')
           enemy20 = Enemy(2790, 50, 6, 'updownshort', 'brownbird.png')
           enemy21 = Enemy(2970, 35, 6, 'updownmed', 'brownbird.png')
           enemy22 = Enemy(3200, 50, 9, 'zigzag', 'ghost.png')
           enemy23 = Enemy(3300, 155, 5, 'swirl', 'fairy.png')
           enemy24 = Enemy(3500, 105, 5, 'swirl1', 'fairy.png')

           enemy_list = pygame.sprite.Group() # create enemy group
           enemy_list.add(enemy1, enemy2, enemy3, enemy4, enemy5, enemy6, enemy7, enemy8, enemy9, enemy10, enemy11, enemy12, enemy13, enemy14, enemy15, enemy16, enemy17, enemy18, enemy19, enemy20, enemy21, enemy22, enemy23, enemy24)

       if lvl == 2:
           print("Level " + str(lvl) )

       return enemy_list

   def ground(lvl, gloc, tx, ty):
       ground_list = pygame.sprite.Group()
       i = 0
       if lvl == 1:
           while i < len(gloc):
               ground = Platform(gloc[i], worldy - ty, tx, ty, 'iceplatform.png')
               ground_list.add(ground)
               i = i + 1

       if lvl == 2:
           print("Level " + str(lvl))

       return ground_list

   def platform(lvl, tx, ty):
       plat_list = pygame.sprite.Group()
       ploc = []
       i = 0
       if lvl == 1:
           ploc.append((200, worldy - ty - 128, 3, 'iceground.png'))
           ploc.append((300, worldy - ty - 256, 3, 'iceground.png'))
           ploc.append((750, worldy - ty - 256, 3, 'iceground.png'))
           ploc.append((750, worldy - ty - 200, 1, 'dirt.png'))
           ploc.append((1200, worldy - ty - 256, 1, 'iceground.png'))
           ploc.append((1264.5, worldy - ty - 286, 0.5, 'iceground.png'))
           ploc.append((1264, worldy - ty - 460, 0.5, 'iceground.png'))
           ploc.append((1325, worldy - ty - 286, 8, 'iceground.png'))
           ploc.append((1325, worldy - ty - 400, 6, 'iceground.png'))
           ploc.append((1700, 425, 0.5, 'dirt.png'))
           ploc.append((1700, 485, 0.5, 'dirt.png'))
           ploc.append((1700, 545, 0.5, 'dirt.png'))
           ploc.append((1700, 595, 0.5, 'dirt.png'))
           ploc.append((2000, 300, 3, 'iceground.png'))
           ploc.append((2150, 200, 0.5, 'iceground.png'))
           ploc.append((2400, 150, 0.5, 'iceground.png'))
           ploc.append((2600, 220, 9, 'iceground.png'))
           ploc.append((2600, 350, 9, 'iceground.png'))
           ploc.append((3470, 400, 9, 'iceground.png'))
           ploc.append((3550, 280, 3, 'iceground.png'))
           ploc.append((3950, 280, 3, 'iceground.png'))
           ploc.append((3470, 150, 9, 'iceground.png'))
           ploc.append((4000, 175, 7, 'iceground.png'))
           ploc.append((4300, 280, 0.5, 'iceground.png'))
           ploc.append((4450, 280, 0.5, 'iceground.png'))
           ploc.append((4775, 280, 2, 'win.png'))
           ploc.append((2805, 25, 0.5, 'iceground.png'))

           while i < len(ploc):
               j = 0
               while j <= ploc[i][2]:
                   plat1 = Platform((ploc[i][0] + (j * tx)), ploc[i][1], tx, ty, ploc[i][3])
                   plat_list.add(plat1)
                   j += 1
               i += 1
       if lvl == 2:
           print("Level " + str(lvl))

       return plat_list

   def loot(lvl):
       if lvl == 1:
           loot_list = pygame.sprite.Group()

           loot1 = Platform(tx * 5, ty * 3.5, tx, ty, 'gem.png')
           loot2 = Platform(tx * 6, ty * 3.5, tx, ty, 'gem.png')
           loot3 = Platform(tx * 7, ty * 3.5, tx, ty, 'gem.png')
           loot4 = Platform(tx * 8, ty * 3.5, tx, ty, 'gem.png')
           loot5 = Platform(1525, 105, tx, ty, 'redgem.png')
           loot6 = Platform(1525, 105, tx, ty, 'redgem.png')
           loot7 = Platform(1525, 105, tx, ty, 'redgem.png')
           loot8 = Platform(2000, 200, tx, ty, 'gem.png')
           loot9 = Platform(2400, 100, tx, ty, 'gem.png')
           loot10 = Platform(2750, 295, tx, ty, 'gem.png')
           loot11 = Platform(2870, 295, tx, ty, 'gem.png')
           loot12 = Platform(2990, 295, tx, ty, 'gem.png')
           loot13 = Platform(4837, 100, tx, ty, 'won.png')
           loot14 = Platform(4837, 100, tx, ty, 'won.png')
           loot15 = Platform(4837, 100, tx, ty, 'won.png')
           loot16 = Platform(4837, 100, tx, ty, 'won.png')
           loot17 = Platform(4837, 100, tx, ty, 'won.png')
           loot18 = Platform(4837, 100, tx, ty, 'won.png')

           loot_list.add(loot1, loot2, loot3, loot4, loot5, loot6, loot7, loot8, loot9, loot10, loot11, loot12, loot13, loot14, loot15, loot16, loot17, loot18)

       if lvl == 2:
           print(lvl)

       return loot_list

'''
Setup
'''
backdrop = pygame.image.load(os.path.join('images', 'icebg.png'))
clock = pygame.time.Clock()
pygame.init()
backdropbox = world.get_rect()
main = True

player = Player()
player.rect.x = 0
player.rect.y = 30
player_list = pygame.sprite.Group()
player_list.add(player)
steps = 10

red_loc = [450, 450]

gloc = []

i = 0
while i <= (worldx / tx) + tx:
   gloc.append(i * tx)
   i = i + 1

ground_list = Level.ground(1, gloc, tx, ty)
plat_list = Level.platform(1, tx, ty)
enemy_list = Level.bad(1, red_loc)
loot_list = Level.loot(1)
'''
Main Loop
'''

while main:
   for event in pygame.event.get():
       if event.type == pygame.QUIT:
           pygame.quit(); sys.exit()
           main = False

       if event.type == pygame.KEYDOWN:
           if event.key == ord('q'):
               pygame.quit()
               try:
                   sys.exit()
               finally:
                   main = False
           if event.key == pygame.K_LEFT or event.key == ord('a'):
               player.control(-steps, 0)
           if event.key == pygame.K_RIGHT or event.key == ord('d'):
               player.control(steps, 0)
           if event.key == pygame.K_UP or event.key == ord('w') or event.key == pygame.K_SPACE:
               player.jump()

       if event.type == pygame.KEYUP:
           if event.key == pygame.K_LEFT or event.key == ord('a'):
               player.control(steps, 0)
           if event.key == pygame.K_RIGHT or event.key == ord('d'):
               player.control(-steps, 0)
   #scroll world forward
   if player.rect.x >= forwardx:
       scroll = player.rect.x - forwardx
       player.rect.x = forwardx
       for p in plat_list:
           p.rect.x -= scroll
       for e in enemy_list:
           e.rect.x -= scroll
       for l in loot_list:
           l.rect.x -= scroll

   # scroll the world backward
   if player.rect.x <= backwardx:
       scroll = backwardx - player.rect.x
       player.rect.x = backwardx
       for p in plat_list:
           p.rect.x += scroll
       for e in enemy_list:
           e.rect.x += scroll
       for l in loot_list:
           l.rect.x += scroll

   if player.health == 0:
       player.kill()
       print('YOU LOST')
       main = False

   if 3 <= player.score <6:
       player.score -= 3
       player.health += 1
   if player.score >= 6:
       print('YOU WON')
       main = False

   world.blit(backdrop, backdropbox)
   player.gravity()
   player.update()
   player_list.draw(world)
   enemy_list.draw(world)
   loot_list.draw(world)
   ground_list.draw(world)
   plat_list.draw(world)
   for e in enemy_list:
       e.move()
   stats(player.score, player.health)
   pygame.display.flip()
   clock.tick(fps)



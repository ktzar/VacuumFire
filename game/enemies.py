import pygame
from . import utils
import random
import math
from .laser import EnemyLaser

class Alien(pygame.sprite.Sprite):
    #bomb sound
    sound_bomb = None
    ratio_powerup = 3 
    images_files = ('alien1.gif', 'alien2.gif', 'alien3.gif', 'alien4.gif', 'alien5.gif')
    images = False

    def __init__(self, top = -1):
        pygame.sprite.Sprite.__init__(self) #call Sprite intializer
        if Alien.sound_bomb == None:
            Alien.sound_bomb = utils.load_sound('bomb-02.wav')
        self.age = 0
        self.cycle = 0
        self.cycle_2 = 0

        #Cache in the class static
        if Alien.images == False:
            images = []
            for image_file in Alien.images_files: 
                image, rect = utils.load_image(image_file, -1)
                images.append((image,rect))
            Alien.images = images
        else:
            images = Alien.images

        self.value = random.randint(0,len(self.images)-1)
        self.image, self.rect = images[self.value]
        self.contains_powerup = (random.randint(1,Alien.ratio_powerup) == 1)
        if top == -1:
            self.rect.top = random.randint(0,480)
        else:
            self.rect.top = top
        self.rect.left = 640
        #Plane, fast forward
        if self.value == 4:
            self.move           = -random.randint(2,7)
            self.agressivity    = random.randint(1,2)
            self.amplitude      = 0
            self.amplitude_2    = 0
            self.frequency      = 0
            self.frequency_2    = 0
        else:
            self.move           = -random.randint(2,7)
            self.agressivity    = random.randint(1,5)
            self.amplitude      = random.randint(1,5)
            self.amplitude_2    = random.randint(0,5)
            self.frequency      = random.random()*0.1+0.05
            self.frequency_2    = random.random()*0.2
        self.target = None

    def set_target(self, target):
        self.target = target 

    def has_powerup(self):
        #Once every 5 enemies will generate a powerup
        return self.contains_powerup

    def update(self):
        self.age += 1
        if self.value == 3:
            self.image, rect = utils.load_image_sprite("alien4.gif", rect=pygame.Rect(self.age%12*58,0,58,34))
        self.cycle+=self.frequency
        self.cycle_2+=self.frequency_2
        self.rect = self.rect.move((self.move, self.amplitude_2*math.sin(self.cycle_2)+self.amplitude*math.sin(self.cycle)))
        if self.rect.left < 0:
            self.kill()
        #move vertically towards the target
        if self.target != None:
            self.rect = self.rect.move((0, -(self.rect.top-self.target.rect.top)*(self.agressivity/10)))

    def kill(self):
        pygame.sprite.Sprite.kill(self)
        Alien.sound_bomb.play()

class Miniboss(pygame.sprite.Sprite):
    def __init__(self, top = -1, stage=False):

        pygame.sprite.Sprite.__init__(self) #call Sprite intializer
        self.stage = stage
        self.image, self.rect = utils.load_image("miniboss.png")
        self.image_reference = self.image
        if top == -1:
            self.rect.top = random.randint(200,300)
        else:
            self.rect.top = top

        self.rect.top   = self.rect.top - self.rect.height / 2
        self.rect.left  = 640
        self.move       = -2
        self.age        = 0
        self.life       = 20
        self.value      = 1
        self.status     = 0 #0:alive, 1:dying, 2:dead
        self.dead_time  = 0 #the age when the object died, to create certain explosions
        self.explosions = 60
        self.target = None
        #0:no laser, 1: top, 2: bottom
        self.shooting_sequence = [\
               0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,\
               0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,\
               1,\
               0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,\
               0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,\
               2,\
               0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,\
               0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,\
               1,\
               0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,\
               0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,\
               0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,\
               1,2,\
               0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,\
               0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,\
               1,\
               0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,\
               0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,\
               2\
               ]

    def has_powerup(self):
        return False
         
    def set_target(self, target):
        self.target = target 

    def hit(self):
        self.life -= 1

    def update(self):
        self.age += 1
        #If the sprite is dying, create one explosion per frame
        if self.status == 1:
            if self.dead_time == 0:
                self.dead_time = self.age
            if self.age - self.dead_time > self.explosions:
                self.status = 2
            if self.rect.left< 640:
                self.image = pygame.transform.rotate(self.image_reference,self.age - self.dead_time)
                self.rect.top   += 1
                self.rect.left  += 1
                self.add_explosion()
                self.add_explosion()
                self.add_explosion()
                self.add_explosion()
                self.add_explosion()
                self.add_explosion()
            #The first update when dead, store the age when dead, to create a limited number of explosions
            new_opacity = max(0,255-(self.age - self.dead_time)*10)
            self.image.set_alpha(new_opacity)
            #don't shoot
            return

        if self.status == 2:
            self.kill();
            return

        if self.life < 0:
            self.status = 1

        if self.rect.left > 400:
            self.rect = self.rect.move((-2, 0))

        #Determine if the enemy shoots or not
        current_sequence = self.shooting_sequence[self.age%len(self.shooting_sequence)]
        if current_sequence > 0:
            laser_pos = self.rect.copy()
            if current_sequence == 1:
                laser_pos.left += laser_pos.width/2
            if current_sequence == 2:
                laser_pos.left += laser_pos.width/2
                laser_pos.top += laser_pos.height
            laser = EnemyLaser(laser_pos, self.stage.ship.rect.copy())
            self.stage.add_enemylaser(laser)



    def add_explosion(self):
        #Random explosion position
        explosion_point = pygame.Rect(\
                random.randint(self.rect.left, self.rect.left + self.rect.width), \
                random.randint(self.rect.top, self.rect.top + self.rect.height), \
                10,10
                )
        self.stage.add_explosion(explosion_point)


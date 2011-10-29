import pygame
import utils
import random
import math

class Alien(pygame.sprite.Sprite):
    #bomb sound
    sound_bomb = None
    ratio_powerup = 3 

    def __init__(self, top = -1):
        pygame.sprite.Sprite.__init__(self) #call Sprite intializer
        if Alien.sound_bomb == None:
            Alien.sound_bomb = utils.load_sound('bomb-02.wav')
        self.images = ('alien1.gif', 'alien2.gif', 'alien3.gif', 'alien4.gif')
        self.age = 0
        self.cycle = 0
        self.cycle_2 = 0
        self.value = random.randint(0,len(self.images)-1)
        if self.value == 3:
            self.image, self.rect = utils.load_image_sprite("alien4.gif", rect=pygame.Rect(0,0,58,34))
        else:
            self.image, self.rect = utils.load_image(self.images[self.value], -1)
        self.contains_powerup = (random.randint(1,Alien.ratio_powerup) == 1)
        if top == -1:
            self.rect.top = random.randint(0,480)
        else:
            self.rect.top = top
        self.rect.left = 640
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
    def __init__(self, top = -1):
        pygame.sprite.Sprite.__init__(self) #call Sprite intializer
        self.image, self.rect = utils.load_image("miniboss.png")
        if top == -1:
            self.rect.top = random.randint(200,300)
        else:
            self.rect.top = top

        self.rect.top   = self.rect.top - self.rect.height / 2
        self.rect.left  = 640
        self.move       = -2
        self.age        = 0
        self.life       = 5
        self.value      = 40
        self.target = None

    def has_powerup(self):
        return False
         
    def set_target(self, target):
        self.target = target 

    def hit(self):
        self.life -= 1
        print "Life:{0}".format(self.life)

    def update(self):
        print self.rect
        print self.life
        self.age += 1
        if self.life < 0:
            self.kill()

        if self.rect.left > 400:
            self.rect = self.rect.move((-2, 0))

    def kill(self):
        pygame.sprite.Sprite.kill(self)


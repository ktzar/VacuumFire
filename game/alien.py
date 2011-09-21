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
        self.cycle = 0
        self.cycle_2 = 0
        self.value = random.randint(0,len(self.images)-1)
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


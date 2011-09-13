import pygame
import utils
import random
import math

class Alien(pygame.sprite.Sprite):
    #bomb sound
    sound_bomb = None

    def __init__(self, top = -1):
        pygame.sprite.Sprite.__init__(self) #call Sprite intializer
        if Alien.sound_bomb == None:
            Alien.sound_bomb = utils.load_sound('bomb-02.wav')
        self.images = ('alien1.gif', 'alien2.gif', 'alien3.gif', 'alien4.gif')
        self.cycle = 0
        self.value = random.randint(0,len(self.images)-1)
        self.image, self.rect = utils.load_image(self.images[self.value], -1)
        self.contains_powerup = (random.randint(1,15) == 1)
        if top == -1:
            self.rect.top = random.randint(0,480)
        else:
            self.rect.top = top
        self.rect.left = 640
        self.move = -random.randint(2,4)
        self.amplitude = random.randint(1,5)
        self.frequency = random.random()*0.1+0.05
        self.target = None

    def set_target(self, target):
        self.target = target 

    def has_powerup(self):
        #Once every 5 enemies will generate a powerup
        return self.contains_powerup

    def update(self):
        self.cycle+=self.frequency
        self.rect = self.rect.move((self.move, self.amplitude*math.sin(self.cycle)))
        if self.rect.left < 0:
            self.kill()
        if self.target != None:
            self.rect = self.rect.move((0, -(self.rect.top-self.target.rect.top)/100))

    def kill(self):
        pygame.sprite.Sprite.kill(self)
        Alien.sound_bomb.play()


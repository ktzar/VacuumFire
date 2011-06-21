import pygame
import utils
import random
import math

class Alien(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self) #call Sprite intializer
        self.images = ('alien1.gif', 'alien2.gif', 'alien3.gif')
        self.cycle = 0
        self.value = random.randint(0,len(self.images)-1)
        self.image, self.rect = utils.load_image(self.images[self.value], -1)
        self.rect.top = random.randint(0,480)
        self.rect.left = 640
        self.move = -random.randint(2,4)
        self.amplitude = random.randint(1,5)
        self.frequency = random.random()*0.1+0.05

    def update(self):
        self.cycle+=self.frequency
        self.rect = self.rect.move((self.move, self.amplitude*math.sin(self.cycle)))
        if self.rect.left < 0:
            self.kill()


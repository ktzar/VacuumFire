import pygame
import utils
import random
import math

class LifeMeter(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self) #call Sprite intializer
        self.life = 10
        self.rect = pygame.Rect(0,0,20,20)
        self.rect.top = 10
        self.rect.left = 350

    def update(self):
        pos = pygame.Rect(0,(self.life-1)*20,140,20)
        self.image, foo = utils.load_image_sprite('life.gif', rect=pos)


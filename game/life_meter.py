import pygame
import utils
import random
import math

class LifeMeter(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self) #call Sprite intializer
        self.life = 10
        self.rect = pygame.Rect(0,0,20,20)
        self.rect.top = 460 
        self.rect.left = 490
        #If self.status > 0 is shaking
        self.status = 0

    def shake(self):
        self.status =49 

    def update(self):
        if self.life > 0:
            pos = pygame.Rect(0,(self.life-1)*20,140,20)
        else:
            pos = pygame.Rect(0,0,140,20)
        self.image, foo = utils.load_image_sprite('life.gif', rect=pos)
        #reduce status until 0 to shake
        if self.status>0:
            if self.status % 2 == 0:
                self.rect = self.rect.move((0,2))
            else:
                self.rect = self.rect.move((0,-2))
            self.status-=1
        else:
            self.rect.top = 460 


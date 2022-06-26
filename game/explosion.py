import pygame
from . import utils
import random

class Explosion(pygame.sprite.Sprite):

    images_1 = False    
    images_2 = False    
    images_3 = False    
    images_4 = False    

    def __init__(self, rect):
        pygame.sprite.Sprite.__init__(self) #call Sprite intializer

        self.life = 10
        self.rect = pygame.Rect(0,0,64,64)
        self.rect.top = rect.top
        self.rect.left = rect.left
        self.status = 0
        self.max_status = 40
        #Cache in the class static
        if Explosion.images_1 == False:
            self.images = []
            for i in range(self.max_status):
                pos = pygame.Rect((i%8)*64,int(i/8)*64,64,64)
                image, foo = utils.load_image_sprite('explosion_1.png', rect=pos)
                self.images.append(image)
            Explosion.images_1 = self.images
            self.images = []
            for i in range(self.max_status):
                pos = pygame.Rect((i%8)*64,int(i/8)*64,64,64)
                image, foo = utils.load_image_sprite('explosion_2.png', rect=pos)
                self.images.append(image)
            Explosion.images_2 = self.images
            self.images = []
            for i in range(self.max_status):
                pos = pygame.Rect((i%8)*64,int(i/8)*64,64,64)
                image, foo = utils.load_image_sprite('explosion_3.png', rect=pos)
                self.images.append(image)
            Explosion.images_3 = self.images
            self.images = []
            for i in range(self.max_status):
                pos = pygame.Rect((i%8)*64,int(i/8)*64,64,64)
                image, foo = utils.load_image_sprite('explosion_4.png', rect=pos)
                self.images.append(image)
            Explosion.images_4 = self.images
        else:
            self.images = eval("Explosion.images_{0}".format(random.randint(1,4)))

    def update(self):
        self.image = self.images[self.status]
        self.status+=1
        if self.status == self.max_status:
            self.kill()


import pygame
import utils

class Explosion(pygame.sprite.Sprite):
    def __init__(self, rect):
        pygame.sprite.Sprite.__init__(self) #call Sprite intializer
        self.life = 10
        self.rect = pygame.Rect(0,0,64,52)
        self.rect.top = rect.top
        self.rect.left = rect.left
        self.status = 0
        self.max_status = 9

    def update(self):
        pos = pygame.Rect(0,(self.status)*52,64,52)
        self.image, foo = utils.load_image_sprite('explosion.gif', rect=pos)
        self.status+=1
        if self.status == self.max_status:
            self.kill()


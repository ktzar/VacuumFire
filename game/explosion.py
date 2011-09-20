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
        self.images = []
        for i in range(self.max_status):
            pos = pygame.Rect(0,(i)*52,64,52)
            image, foo = utils.load_image_sprite('explosion.gif', rect=pos)
            image.set_alpha(60)
            self.images.append(image)

    def update(self):
        self.image = self.images[self.status]
        self.status+=1
        if self.status == self.max_status:
            self.kill()


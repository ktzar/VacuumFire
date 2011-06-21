import pygame
import utils

class Laser(pygame.sprite.Sprite):
    num = 0

    def __init__(self, owner):
        pygame.sprite.Sprite.__init__(self) #call Sprite intializer

        Laser.num+=1
        self.owner = owner
        self.images = ('laser.gif', 'laser.gif', 'laser2.gif', 'laser2.gif', 'laser.gif', 'laser2.gif')
        self.image_anim_counter = 0
        self.image, self.rect = utils.load_image(self.images[0], -1)
        self.rect = owner.rect.copy()
        self.rect.top+= owner.rect.height/2-10
        self.rect.left+= owner.rect.width*0.5
        self.move = 5
        print Laser.num," lasers in screen"

    def kill(self):
        pygame.sprite.Sprite.kill(self)
        Laser.num-=1

    def update(self):
        self.image, dummy_rect = utils.load_image(self.images[self.image_anim_counter])
        self.image_anim_counter = (self.image_anim_counter+1)%len(self.images)
        self.rect = self.rect.move((self.move, 0))
        if self.rect.left > 600:
            self.kill()

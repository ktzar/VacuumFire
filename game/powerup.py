import pygame
import utils

#Power up. It "ages" and TODO have a type to choose form a spritesheet. It moves backwards once created TODO with a nice bouncing effect
class Powerup(pygame.sprite.Sprite):

    def __init__(self, rect, value):
        pygame.sprite.Sprite.__init__(self) #call Sprite intializer
        self.rect = pygame.Rect(0,0,26,26)
        self.rect.top = rect.top
        self.rect.left = rect.left
        self.age = 0
        self.status = 0
        self.max_status = 3
        self.type = value % 3
        self.value = 1000 #score it gives to the player

    def update(self):
        self.age = self.age+1
        self.rect = self.rect.move((-(self.age/2-10), 0))

        if self.rect.left < 0:
            self.kill()
            return
        pos = pygame.Rect((self.status)*28, self.type*28, 26,26)
        self.image, foo = utils.load_image_sprite('powerups.png', rect=pos)
        if self.age % 4 != 0:
            return
        self.status = self.status + 1
        if self.status == self.max_status:
            self.status = 0
            #self.rect = self.rect.move(((self.age-30)*(self.age-30)+10, 0))



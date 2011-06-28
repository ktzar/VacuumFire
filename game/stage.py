import pygame
import utils

class Grass(pygame.sprite.Sprite):
    def __init__(self, pos):
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = utils.load_image('stage_grass.png')
        self.rect.top   = pos.top
        self.rect.left  = pos.left 

class Powerup(pygame.sprite.Sprite):
    def __init__(self, pos):
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = utils.load_image('item.png')
        self.rect.top   = pos.top 
        self.rect.left  = pos.left


"""Stage"""
class Stage(pygame.sprite.Group):

    def __init__(self):
        pygame.sprite.Group.__init__(self)
        self.image, self.rect = utils.load_image('level_1.gif')
        self.count = 0

    def update(self):
        self.count = (self.count+1)%8

        if self.count%2 == 0:
            for sprite in self.sprites():
                sprite.rect = sprite.rect.move((-1,0))

        if self.count == 0:
            self.empty()
            self.rect = self.rect.move((1,0))
            for x in range(self.rect.left, self.rect.left+41):
                for y in range(self.rect.height):
                    if self.image.get_at((x,y)) == (0,0,0,255):
                        grass = Grass(pygame.Rect((x-self.rect.left)*16,y*16, 16, 16))
                        #print("Grass in {0},{1},{2},{3}").format((x-self.rect.left)*16,y*16, 16, 16)
                        self.add(grass)
                    if self.image.get_at((x,y)) == (255,0,0,255):
                        powerup = Powerup(pygame.Rect(x*16,y*16, 16, 16))
                        #print("Powerup in {0},{1},{2},{3}").format(x*16,y*16, 16, 16)
                        self.add(powerup)
        

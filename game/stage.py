import pygame
import utils

class Grass(pygame.sprite.Sprite):
    def __init__(self, pos):
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = utils.load_image('stage_grass.png')
        self.rect.top   = pos.top
        self.rect.left  = pos.left 

    def update(self):
        self.rect = self.rect.move((-1,0))

class Powerup(pygame.sprite.Sprite):
    def __init__(self, pos):
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = utils.load_image('item.png')
        self.rect.top   = pos.top 
        self.rect.left  = pos.left

    def update(self):
        self.rect = self.rect.move((-1,0))


"""Stage"""
class Stage(pygame.sprite.Group):

    def __init__(self):
        pygame.sprite.Group.__init__(self)
        image, rect = utils.load_image('level_1.gif')

        for x in range(rect.width):
            for y in range(rect.height):
                if image.get_at((x,y)) == (0,0,0,255):
                    grass = Grass(pygame.Rect(x*16,y*16, 16, 16))
                    self.add(grass)
                if image.get_at((x,y)) == (255,0,0,255):
                    powerup = Powerup(pygame.Rect(x*16,y*16, 16, 16))
                    self.add(powerup)
        

import pygame
from game.utils import *
from . import utils

#Powerup dash, it gets a "value from zero to five and represents it in a meter that can be placed somewhere
#It should be inherited to specify the self.image_file. When the max state is reached it alternates between sprite
#5 and 6 to produce a blinking effect
class Meter(pygame.sprite.Sprite):

    def __init__(self, rect):
        pygame.sprite.Sprite.__init__(self) #call Sprite intializer
        self.status = 0
        self.image_file = ''
        self.rect = pygame.Rect(0,0,40,60)
        self.rect.top = rect.top
        self.rect.left = rect.left
        self.age = 0

    def set_status(self, new_status):
        self.status = new_status

    def update(self):
        self.age += 1
        if self.age %3 == 0:
            if self.status == 5:
                self.status = 6
            elif self.status == 6:
                self.status = 5
        try:	
            pos = pygame.Rect((self.status)*40, 0, 40,60)
            self.image, foo = utils.load_image_sprite(self.image_file, rect=pos)
        except ValueError:
            print("Error loading image ", self.image_file)

class BuddyMeter(Meter):
    def __init__(self, rect):
        Meter.__init__(self, rect)
        self.image_file = 'dash_powerup_buddy.png'

class WeaponMeter(Meter):
    def __init__(self, rect):
        Meter.__init__(self, rect)
        self.image_file = 'dash_powerup_weapon.png'

class SpeedMeter(Meter):
    def __init__(self, rect):
        Meter.__init__(self, rect)
        self.image_file = 'dash_powerup_speed.png'

    def update(self):
        Meter.update(self)




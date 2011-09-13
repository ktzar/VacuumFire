import pygame
import utils
from math import *

"""This class represents the ship that the player controls"""
class Ship(pygame.sprite.Sprite):

    LEFT = 0
    RIGHT = 1
    UP = 3
    DOWN = 4

    decceleration = 0.90
    topleft = 10, 10
    #User interactions modify this, current speed of movement (positive->up or negative->down)
    momentum = 0
    #Max speed of the ship
    max_momentum = 20
    #User interactions modify this, current speed of movement (positive->up or negative->down)
    x_momentum = 0

    #speed of the ship
    momentum_delta = 2
    #Max speed of the ship
    max_x_momentum = 20
    #Initial life counter
    life = 10
    #'up' or 'down' (for the animation)
    status = ''
    #Ship.LEFT or Ship.RIGHT (for the animation)
    x_status = ''

    #TODO change status for constants for perfrmance
    def __init__(self):
        pygame.sprite.Sprite.__init__(self) #call Sprite intializer
        self.image, self.rect = utils.load_image_sprite('spaceship.gif', rect=pygame.Rect(0,0,64,64))
        screen = pygame.display.get_surface()
        self.area = screen.get_rect()
        #Initial position
        self.powerup = { 'penetrate' : False, 'speedup' : 1 }

    def update(self):
        if self.x_status==Ship.LEFT and self.x_momentum < self.max_x_momentum:
            self.x_momentum-=self.momentum_delta

        if self.x_status==Ship.RIGHT and self.x_momentum > -self.max_x_momentum:
            self.x_momentum+=self.momentum_delta

        if (self.x_momentum < 0 and self.rect.left > 0) or (self.x_momentum > 0 and self.rect.left < 640-self.rect.width):
            self.rect = self.rect.move((self.x_momentum/5, 0))

        self.x_momentum *= self.decceleration

        if abs(self.momentum) < 1:
            self.momentum = 0

        if self.status==Ship.DOWN and self.momentum < self.max_momentum:
            self.momentum+=self.momentum_delta

        if self.status==Ship.UP and self.momentum > -self.max_momentum:
            self.momentum-=self.momentum_delta

        if (self.momentum < 0 and self.rect.top > 0) or (self.momentum > 0 and self.rect.top < 480-self.rect.height):
            self.rect = self.rect.move((0, self.momentum/5))

        self.momentum *= self.decceleration

        if abs(self.momentum) < 1:
            self.momentum = 0

        #change image depending on momentum
        if self.momentum > 4:
            self.image, foo = utils.load_image_sprite('spaceship.gif', rect=pygame.Rect(0,128,64,64))
        elif self.momentum < -4:
            self.image, foo = utils.load_image_sprite('spaceship.gif', rect=pygame.Rect(0,64,64,64))
        else:
            self.image, foo = utils.load_image_sprite('spaceship.gif', rect=pygame.Rect(0,0,64,64))

    def damage(self):
        self.life-=1

    def stop_move_left(self):
        self.x_status = ''

    def stop_move_right(self):
        self.x_status = ''

    def move_left(self):
        self.x_status = Ship.LEFT 

    def move_right(self):
        self.x_status = Ship.RIGHT 

    def stop_move_up(self):
        self.status = ''

    def stop_move_down(self):
        self.status = ''

    def move_up(self):
        self.status = Ship.UP

    def move_down(self):
        self.status = Ship.DOWN

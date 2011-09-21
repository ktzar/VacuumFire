import pygame
import utils
from math import *

"""This class represents the ship that the player controls"""
class Ship(pygame.sprite.Sprite):

    LEFT = 0
    RIGHT = 1
    UP = 3
    DOWN = 4

    decceleration = 0.93
    topleft = 10, 10
    #User interactions modify this, current speed of movement (positive->up or negative->down)
    y_momentum = 0
    #Max speed of the ship
    max_y_momentum = 20
    #User interactions modify this, current speed of movement (positive->up or negative->down)
    x_momentum = 0

    #speed of the ship
    momentum_delta = 2
    #Max speed of the ship
    max_x_momentum = 10
    #Initial life counter
    life = 10
    #'up' or 'down' (for the animation)
    status = ''
    #Ship.LEFT or Ship.RIGHT (for the animation)
    x_status = ''

    def __init__(self):
        pygame.sprite.Sprite.__init__(self) #call Sprite intializer
        self.image, self.rect = utils.load_image_sprite('spaceship.png', rect=pygame.Rect(0,0,54,43))
        screen = pygame.display.get_surface()
        self.area = screen.get_rect()
        self.rect.top = self.area.height / 2 - self.rect.height / 2
        #Initial position
        self.powerup = { 'penetrate' : False, 'speedup' : 0 }

    def update(self):
        if self.x_status==Ship.LEFT and self.x_momentum < self.max_x_momentum:
            self.x_momentum-=self.momentum_delta
        if self.x_status==Ship.RIGHT and self.x_momentum > -self.max_x_momentum:
            self.x_momentum+=self.momentum_delta
        if (self.x_momentum < 0 and self.rect.left > 0) or (self.x_momentum > 0 and self.rect.left < 640-self.rect.width):
            self.rect = self.rect.move((self.x_momentum/(6-self.powerup['speedup']), 0))
        self.x_momentum *= self.decceleration - (self.powerup['speedup'] * 0.04)
        if abs(self.x_momentum) < 1:
            self.x_momentum = 0

        if self.status==Ship.UP and self.y_momentum > -self.max_y_momentum:
            self.y_momentum-=self.momentum_delta
        if self.status==Ship.DOWN and self.y_momentum < self.max_y_momentum:
            self.y_momentum+=self.momentum_delta
        if (self.y_momentum < 0 and self.rect.top > 0) or (self.y_momentum > 0 and self.rect.top < 480-self.rect.height):
            self.rect = self.rect.move((0, self.y_momentum/(6-self.powerup['speedup'])))
        self.y_momentum *= self.decceleration - (self.powerup['speedup'] * 0.04)
        if abs(self.y_momentum) < 1:
            self.y_momentum = 0

        #change image depending on vertical momentum
        if self.y_momentum > 4:
            self.image, foo = utils.load_image_sprite('spaceship.png', rect=pygame.Rect(0,86,54,43))
        elif self.y_momentum < -4:
            self.image, foo = utils.load_image_sprite('spaceship.png', rect=pygame.Rect(0,43,54,43))
        else:
            self.image, foo = utils.load_image_sprite('spaceship.png', rect=pygame.Rect(0,0,54,43))

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

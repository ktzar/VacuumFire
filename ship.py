import pygame
import utils
from math import *

"""This class represents the ship that the player controls"""
class Ship(pygame.sprite.Sprite):
    #TODO change status for constants for perfrmance
    def __init__(self):
        pygame.sprite.Sprite.__init__(self) #call Sprite intializer
        self.image, self.rect = utils.load_image_sprite('spaceship.gif', rect=pygame.Rect(0,0,64,64))
        screen = pygame.display.get_surface()
        self.area = screen.get_rect()
        #Initial position
        self.rect.topleft = 10, 10
        #User interactions modify this, current speed of movement (positive->up or negative->down)
        self.momentum = 0
        #Max speed of the ship
        self.max_momentum = 20
        #User interactions modify this, current speed of movement (positive->up or negative->down)
        self.x_momentum = 0
        #Max speed of the ship
        self.max_x_momentum = 20
        #Initial life counter
        self.life = 10
        #'up' or 'down' (for the animation)
        self.status = ''
        #'left' or 'right' (for the animation)
        self.x_status = ''

    def update(self):
        if self.x_status=='left' and self.x_momentum < self.max_x_momentum:
            self.x_momentum-=2

        if self.x_status=='right' and self.x_momentum > -self.max_x_momentum:
            self.x_momentum+=2

        if (self.x_momentum < 0 and self.rect.left > 0) or (self.x_momentum > 0 and self.rect.left < 640-self.rect.width):
            self.rect = self.rect.move((self.x_momentum/5, 0))

        self.x_momentum *= 0.95

        if abs(self.momentum) < 1:
            self.momentum = 0

        if self.status=='down' and self.momentum < self.max_momentum:
            self.momentum+=2

        if self.status=='up' and self.momentum > -self.max_momentum:
            self.momentum-=2

        if (self.momentum < 0 and self.rect.top > 0) or (self.momentum > 0 and self.rect.top < 480-self.rect.height):
            self.rect = self.rect.move((0, self.momentum/5))

        self.momentum *= 0.95

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
        self.x_status = 'left'

    def move_right(self):
        self.x_status = 'right'

    def stop_move_up(self):
        self.status = ''

    def stop_move_down(self):
        self.status = ''

    def move_up(self):
        self.status = 'up'

    def move_down(self):
        self.status = 'down'

import pygame
import utils

"""Class that represents the laser that the player shoots"""
class Laser(pygame.sprite.Sprite):
    #number of lasers in the screen
    num = 0
    #max number of lasers in the screen
    max_lasers = 1
    sound_laser = 0
    move = 15

    def __init__(self, owner):
        if Laser.sound_laser == 0:
            Laser.sound_laser = utils.load_sound('laser-01.wav')
        pygame.sprite.Sprite.__init__(self) #call Sprite intializer

        Laser.sound_laser.play()
        Laser.num+=1
        self.owner = owner
        #this makes the animation
        self.images = ('laser.gif', 'laser-2.gif', 'laser-3.gif', 'laser-4.gif', 'laser-3.gif', 'laser-2.gif')
        self.image_anim_counter = 0
        self.image, self.rect = utils.load_image(self.images[0], -1)
        self.rect = owner.rect.copy()
        self.rect.top+= owner.rect.height/2-10
        self.rect.left+= owner.rect.width*0.5

    def kill(self):
        #Remove the laser from the groups and decrease the lasers on screen
        if Laser.num > 0:
            Laser.num-=1
        pygame.sprite.Sprite.kill(self)

    def update(self):
        self.image, dummy_rect = utils.load_image(self.images[self.image_anim_counter])
        self.image.set_colorkey((0,0,0))
        self.image_anim_counter = (self.image_anim_counter+1)%len(self.images)
        self.rect = self.rect.move((self.move, 0))
        if self.rect.left > 1000:
            self.kill()

class EnemyLaser(pygame.sprite.Sprite):

    def __init__(self, source, target):
        pygame.sprite.Sprite.__init__(self) #call Sprite intializer
        self.image, self.rect = utils.load_image('laserbeam.png')
        self.target     = target.copy()
        self.rect.top   = source.top
        self.rect.left  = source.left
        self.a_y = (self.rect.top - self.target.top ) / 20
        self.a_x = (self.rect.left - self.target.left ) / 20

    def update(self):
        self.rect.left -= self.a_x
        self.rect.top -= self.a_y

        if self.rect.left < 0:
            self.kill()
        



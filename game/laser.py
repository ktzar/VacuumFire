import pygame
import random
import math
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
        self.images_files = ('laser.gif', 'laser-2.gif', 'laser-3.gif', 'laser-4.gif', 'laser-3.gif', 'laser-2.gif')
        self.images = []
        for image_file in self.images_files:
            temp_image, self.rect = utils.load_image(image_file)
            temp_image.set_colorkey((0,0,0))
            self.images.append(temp_image)
        self.image = self.images[0]
        self.image_anim_counter = 0
        self.rect = owner.rect.copy()
        self.rect.top+= owner.rect.height/2-10
        self.rect.left+= owner.rect.width*0.5

    def kill(self):
        #Remove the laser from the groups and decrease the lasers on screen
        if Laser.num > 0:
            Laser.num-=1
        pygame.sprite.Sprite.kill(self)

    def update(self):
        self.image = self.images[self.image_anim_counter]
        self.image_anim_counter = (self.image_anim_counter+1)%len(self.images)
        self.rect = self.rect.move((self.move, 0))
        if self.rect.left > 1000:
            self.kill()

class EnemyLaser(pygame.sprite.Sprite):

    def __init__(self, source, target):
        pygame.sprite.Sprite.__init__(self) #call Sprite intializer
        self.image, self.rect = utils.load_image('laserbeam.png')
        self.target     = target.copy()
        source = source.copy()
        self.rect.top   = source.top
        self.rect.left  = source.left
        #30 and 40 are the min/max boundaries for the random speed 
        self.a_y = (self.rect.top - self.target.top ) / random.randint(30,40)
        self.a_x = (self.rect.left - self.target.left ) / random.randint(30,40)
        if self.a_y == 0:
            angle = 0
        else:
            angle = math.atan( (self.rect.left - self.target.left ) / (self.rect.top - self.target.top))
            angle = 90 + angle * 57.32 #from radians
        self.image = pygame.transform.rotozoom(self.image,angle,1)

    def update(self):
        self.rect.left -= self.a_x
        self.rect.top -= self.a_y

        if self.rect.left < 0:
            self.kill()
        
class DiagonalLaser(Laser):
    def __init__(self, owner, direction):
        pygame.sprite.Sprite.__init__(self) #call Sprite intializer
        self.owner = owner
        #this makes the animation
        self.images_files = ('laser.gif', 'laser-2.gif', 'laser-3.gif', 'laser-4.gif', 'laser-3.gif', 'laser-2.gif')
        self.images = []
        for image_file in self.images_files:
            temp_image, self.rect = utils.load_image(image_file)
            temp_image.set_colorkey((0,0,0))
            self.images.append(temp_image)
        self.image = self.images[0]
        self.image_anim_counter = 0
        self.rect = owner.rect.copy()
        self.rect.top+= owner.rect.height/2-10
        self.rect.left+= owner.rect.width*0.5
        self.move = 15

        if direction == "up":
            self.xmove = self.move
            self.ymove = -self.move
        if direction == "down":
            self.xmove = self.move
            self.ymove = self.move
        if direction == "back":
            self.xmove = -self.move
            self.ymove = 0

    def update(self):
        self.image = self.images[self.image_anim_counter]
        self.image_anim_counter = (self.image_anim_counter+1)%len(self.images)
        self.rect = self.rect.move((self.xmove, self.ymove))
        if self.rect.left > 1000:
            self.kill()




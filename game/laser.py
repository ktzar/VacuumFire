import pygame
import utils

"""Class that represents the laser that the player shoots"""
class Laser(pygame.sprite.Sprite):
    #number of lasers in the screen
    num = 0
    #max number of lasers in the screen
    max_lasers = 3
    sound_laser = 0

    def __init__(self, owner):
        if Laser.sound_laser == 0:
            Laser.sound_laser = utils.load_sound('laser-01.wav')
        pygame.sprite.Sprite.__init__(self) #call Sprite intializer

        Laser.sound_laser.play()
        Laser.num+=1
        self.owner = owner
        #this makes the animation
        self.images = ('laser.gif', 'laser.gif', 'laser2.gif', 'laser2.gif', 'laser.gif', 'laser2.gif')
        self.image_anim_counter = 0
        self.image, self.rect = utils.load_image(self.images[0], -1)
        self.rect = owner.rect.copy()
        self.rect.top+= owner.rect.height/2-10
        self.rect.left+= owner.rect.width*0.5
        self.move = 5
        print Laser.num," lasers in screen"

    def kill(self):
        #Remove the laser from the groups and decrease the lasers on screen
        pygame.sprite.Sprite.kill(self)
        Laser.num-=1

    def update(self):
        self.image, dummy_rect = utils.load_image(self.images[self.image_anim_counter])
        self.image_anim_counter = (self.image_anim_counter+1)%len(self.images)
        self.rect = self.rect.move((self.move, 0))
        if self.rect.left > 600:
            self.kill()
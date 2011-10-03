#Import Modules
import os, pygame, time
import random
from pygame.locals import *
import utils

class Intro():

    def __init__(self, screen):
        #sounds
        self.screen = screen
        self.age = 0
        self.font = utils.load_font('4114blasterc.ttf', 36)
        self.size = self.screen.get_size()
        self.menu_finished = False

        self.background, self.background_rect    = utils.load_image('intro_bg_1.jpg')
        self.parallax, self.parallax_rect        = utils.load_image('intro_bg_2.png')
        self.logo, foo          = utils.load_image('intro_logo.png')

        self.screen.blit(self.background, (0, 0))
        pygame.display.flip()


    #Main Loop
    def loop(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                #exit
                return
            elif event.type == KEYDOWN:
                self.menu_finished = True


        init_text = 'Press any key'

        if self.age%8 == 0 or self.age%8 == 1:
            text_color = (0,0,0)
        else:
            text_color = (255, 255, 255)
        text = self.font.render(init_text, 1, text_color)

        if self.age%2 == 0:
            self.background_rect = self.background_rect.move((-1,0))
        if self.age%3 == 0:
            self.parallax_rect = self.parallax_rect.move((-1,0))
        #rotate background
        if -self.background_rect.left > self.background_rect.width - self.size[0] :
            self.background_rect.left = 0
        if -self.parallax_rect.left > self.parallax_rect.width - self.size[0] :
            self.parallax_rect.left = 0
        
        self.screen.blit(self.background, self.background_rect)
        self.screen.blit(self.parallax, self.parallax_rect)
        self.screen.blit(self.logo, (0, 0))
        self.screen.blit(text, (200, 300))

        pygame.display.flip()
        self.age += 1

    #Game Over



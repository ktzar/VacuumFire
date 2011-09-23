#Import Modules
import os, pygame, time
import random
from pygame.locals import *
import utils

class Intro():

    def __init__(self):
        if not pygame.font: print 'Warning, fonts disabled'
        if not pygame.mixer: print 'Warning, sound disabled'
        self.initialise()
        self.loop()

    def initialise(self):
        """this function is called when the program starts.
           it initializes everything it needs, then runs in
           a loop until the function returns."""
        #Initialize Everything
        pygame.init()
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode((640, 480), pygame.DOUBLEBUF)
        self.size = self.screen.get_size()
        self.font = utils.load_font('4114blasterc.ttf', 36)
        pygame.display.set_caption('VacuumFire')
        pygame.mouse.set_visible(0)
        #icon
        icon, foo = utils.load_image('icon.png')
        pygame.display.set_icon(icon)

        self.age = 0

        #sounds
        self.music = utils.load_sound('intro.ogg')
        self.music.play()

        self.background, self.background_rect    = utils.load_image('intro_bg_1.jpg')
        self.parallax, self.parallax_rect        = utils.load_image('intro_bg_2.png')
        self.logo, foo          = utils.load_image('intro_logo.png')

        self.screen.blit(self.background, (0, 0))
        pygame.display.flip()


    #Main Loop
    def loop(self):
        while 1:
            for event in pygame.event.get():
                if event.type == QUIT:
                    #exit
                    return
                elif event.type == KEYDOWN and event.key == K_ESCAPE:
                    pygame.quit()
                    quit()

            self.clock.tick(50)

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



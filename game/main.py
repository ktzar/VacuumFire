#Import Modules
import os, pygame, time
import random
import utils
from pygame.locals import *
from intro       import Intro
from vacuum      import Vacuum

class Main():

    def __init__(self):
        if not pygame.font: print 'Warning, fonts disabled'
        if not pygame.mixer: print 'Warning, sound disabled'
        """this function is called when the program starts.
           it initializes everything it needs, then runs in
           a loop until the function returns."""
        #Initialize Everything
        pygame.init()
        #self.screen = pygame.display.set_mode((640, 480), pygame.FULLSCREEN | pygame.DOUBLEBUF)
        self.screen = pygame.display.set_mode((640, 480), pygame.DOUBLEBUF)
        pygame.display.set_caption('VacuumFire')
        #pygame.display.toggle_fullscreen()
        pygame.mouse.set_visible(0)
        #icon
        icon, foo = utils.load_image('icon.png')
        pygame.display.set_icon(icon)

        intro = Intro(self.screen)
        vacuum = Vacuum(self.screen)
        self.clock = pygame.time.Clock()

        #Load musics
        self.music = {}
        self.music['game'] = utils.load_sound('level_1.ogg')
        self.music_game_playing = False
        self.music['intro'] = utils.load_sound('intro.ogg')
        self.music['intro'].play()


        #Loop intro or game depending on intro's state
        while 1:
            self.clock.tick(50)
            if intro.menu_finished == False:
                intro.loop()
            else:
                self.music['intro'].stop()
                if self.music_game_playing == False:
                    self.music['game'].play()
                    self.music_game_playing = True
                vacuum.loop()
            pygame.display.flip()

    #Game Over



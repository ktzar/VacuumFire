import pygame
import utils

class Background(pygame.Surface):

    IDLE = 0
    WARNING = 1

    def __init__(self, screen):
        pygame.Surface.__init__(self, screen) #call Sprite intializer
        self.convert()
        self.screen = screen
        self.fill((250, 250, 250))
        self.back_image, self.back_rect = utils.load_image('background.jpg');
        self.back_image_alpha, self.back_rect_alpha = utils.load_image('background_alpha.png');
        self.warning_image, self.warning_rect = utils.load_image('warning.png');
        self.back_rect_init = self.back_rect.copy()
        self.status = Background.IDLE
        #counter to switch warning on and off
        self.status_count = 0
        self.status_count_max = 50
        self.counter = 0

    def warning(self):
        self.status = Background.WARNING
        self.status_count = self.status_count_max

    def update(self):

        self.counter = self.counter + 1
        if self.counter%3 ==0:
            self.back_rect = self.back_rect.move((-1,0))
        if self.counter%2 ==0:
            self.back_rect_alpha = self.back_rect_alpha.move((-1,0))
        self.blit(self.back_image, self.back_rect)
        self.blit(self.back_image_alpha, self.back_rect_alpha)

        if self.status == Background.WARNING:
            if self.status_count % 2 == 0:
                self.blit(self.warning_image, self.warning_rect)
            self.status_count -= 1
            if self.status_count <= 0:
                self.status = Background.IDLE

        #Repeat the background
        if -self.back_rect.left > self.back_rect_init.width-self.screen[0]:
            self.back_rect = self.back_rect_init.copy()


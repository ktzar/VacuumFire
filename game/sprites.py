import pygame
import utils, random
from math import *


class Flying_Score(pygame.sprite.Sprite):

    def __init__(self, position, score):
        self.age = 0
        pygame.sprite.Sprite.__init__(self)
        font = utils.load_font('4114blasterc.ttf', 20)
        score = '{0}'.format(score)
        surf_text = font.render(score, 2, (255,255,255))
        self.image = pygame.Surface(font.size(score))
        self.image.blit(surf_text, (0,0))
        self.rect = position
        self.image.set_colorkey((0,0,0))

    def update(self):
        new_alpha = max(0,255-self.age * 25)
        self.image.set_alpha (new_alpha)
        self.age += 1
        self.rect.top -= self.age/3 + random.randint(1,5)
        if self.age > 11:
            self.kill()

class Score_Meter(pygame.sprite.Sprite):

    def __init__(self, position):
        pygame.sprite.Sprite.__init__(self)
        self.score = 0
        self.target_score = 0
        self.rect = position
        self.font = utils.load_font('4114blasterc.ttf', 36)
        self.reload_image()

    def reload_image(self):
        score_text = 'Score: {0}'.format((self.score))
        text = self.font.render(score_text, 1, (255, 255, 255))
        text_shadow = self.font.render(score_text, 1, (0,0,0))
        self.image = pygame.Surface(self.font.size(score_text))
        self.image.blit(text_shadow, (0,0))
        self.image.blit(text, (0,0))
        self.image.set_colorkey((0,0,0))

    def add_score(self, score):
        self.target_score += score

    def update(self):
        if self.target_score > self.score:
            self.score += (self.target_score - self.score ) / 10 + random.randint(5,9)
            if self.score > self.target_score:
                self.score = self.target_score
            self.reload_image()


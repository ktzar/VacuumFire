import pygame
from . import utils
import random, math

class Dummy(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self) #call Sprite intializer
        self.image, self.rect = utils.load_image('dummy.png')

class Flying_Label(pygame.sprite.Sprite):

    def __init__(self, position, score):
        self.age = 0
        pygame.sprite.Sprite.__init__(self)
        font = utils.load_font('4114blasterc.ttf', 20)
        score = '{0}'.format(score)
        surf_text = font.render(score, 2, (255,255,255))
        self.image = pygame.Surface(font.size(score))
        self.image.blit(surf_text, (0,0))
        self.rect = position.copy()
        self.image.set_colorkey((0,0,0))

    def update(self):
        new_alpha = max(0,255-self.age * 20)
        self.image.set_alpha (new_alpha)
        self.age += 1
        self.rect.top -= (self.age/6)**3
        if self.age > 15:
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
        score_text = 'Score: {0}'.format(int(self.score))
        text = self.font.render(score_text, 1, (255, 255, 255))
        text_shadow = self.font.render(score_text, 1, (0,0,0))
        self.image = pygame.Surface(self.font.size(score_text))
        self.image.blit(text_shadow, (5,5))
        self.image.blit(text, (0,0))
        self.image.set_colorkey((0,0,0))

    def add_score(self, score):
        self.target_score += score

    def update(self):
        if self.target_score > self.score:
            self.score += int((self.target_score - self.score ) / 10) + random.randint(5,9)
            if self.score > self.target_score:
                self.score = self.target_score
            self.reload_image()

class Buddy(pygame.sprite.Sprite):
    def __init__(self, ship):
        pygame.sprite.Sprite.__init__(self)
        self.ship = ship
        self.image, self.rect = utils.load_image_sprite('buddy.png', rect=pygame.Rect(0,0,14,14))
        self.image.set_colorkey((0,0,0))
        self.phase = self.ship.buddies * 2.09 #(2/3)*pi

    def update(self):
        self.rect.top = self.ship.rect.top + self.ship.rect.height /2 + 2*(self.rect.height) * math.sin(self.phase + self.ship.age)
        self.rect.left = -20 + self.ship.rect.left + self.ship.rect.width /2 + 2*(self.rect.width) * math.cos(self.phase + self.ship.age)

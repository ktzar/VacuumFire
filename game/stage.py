import random
import pygame
import utils


"""Stage"""
class Stage(pygame.Surface):
    def __init__(self, stage_file='level_1'):
        self.level_data, self.rect = utils.load_image('{0}.gif'.format(stage_file))
        self.ratio = 16 #ratio of pixel in stage file / pixel in game
        pygame.Surface.__init__(self, (self.rect.width*self.ratio, self.rect.height*self.ratio))
        self.counter = 0
        self.scrolled = 0
        self.fill((0,0,0))
        self.set_colorkey((0,0,0))
        self.limits = []


        self.image_grass_bl, self.rect_grass = utils.load_image('stage_grass_bl.png')
        self.image_grass_br, self.rect_grass = utils.load_image('stage_grass_br.png')
        self.image_grass_tl, self.rect_grass = utils.load_image('stage_grass_tl.png')
        self.image_grass_tr, self.rect_grass = utils.load_image('stage_grass_tr.png')
        self.image_grass_t, self.rect_grass = utils.load_image('stage_grass_t.png')


        self.colors = { \
            "grass":(0,0,0,255), \
            "enemies":(255,0,0,255), \
            'bg':(229,229,229,255) \
        }

        self.rect = self.rect.move((1,0))
        for x in range(0, self.rect.width-1):
            #will store top and bottom limits and append it to self.limits
            #to control the ship not getting over this
            x_limits = [0,0]
            for y in range(self.rect.height-1):
                #Calculate top and bottom limits
                if y>0 and self.level_data.get_at((x,y)) == self.colors["grass"] and \
                self.level_data.get_at((x,y+1)) == self.colors["bg"]:
                    x_limits[0] = y+1

                if y<self.rect.height and self.level_data.get_at((x,y)) == self.colors["bg"] and \
                self.level_data.get_at((x,y+1)) == self.colors["grass"]:
                    x_limits[1] = y-1

                if self.level_data.get_at((x,y)) == self.colors["grass"]:
                    try:
                        sprite_chosen = "center"
                        if y == 0 or x == 0:
                            sprite_chosen = "center"
                        #Grass surrounded by grass
                        elif self.level_data.get_at((x-1, y)) == self.colors["grass"] and \
                        self.level_data.get_at((x+1, y)) == self.colors["grass"] and \
                        self.level_data.get_at((x, y-1)) == self.colors["grass"] and \
                        self.level_data.get_at((x, y+1)) == self.colors["grass"]:
                            sprite_chosen = "center"

                        #Corner
                        elif self.level_data.get_at((x-1, y)) != self.colors["grass"] and\
                        self.level_data.get_at((x-1, y-1)) != self.colors["grass"] and \
                        self.level_data.get_at((x, y-1)) != self.colors["grass"]:
                            sprite_chosen = self.image_grass_tl

                        #Corner
                        elif self.level_data.get_at((x+1, y)) != self.colors["grass"] and\
                        self.level_data.get_at((x+1, y-1)) != self.colors["grass"] and \
                        self.level_data.get_at((x, y-1)) != self.colors["grass"]:
                            sprite_chosen = self.image_grass_tr

                        #Corner
                        elif self.level_data.get_at((x-1, y)) != self.colors["grass"] and\
                        self.level_data.get_at((x-1, y+1)) != self.colors["grass"] and \
                        self.level_data.get_at((x, y+1)) != self.colors["grass"]:
                            sprite_chosen = self.image_grass_bl

                        #Corner
                        elif self.level_data.get_at((x+1, y)) != self.colors["grass"] and\
                        self.level_data.get_at((x+1, y+1)) != self.colors["grass"] and \
                        self.level_data.get_at((x, y+1)) != self.colors["grass"]:
                            sprite_chosen = self.image_grass_br

                        #Side
                        elif self.level_data.get_at((x+1, y-1)) == self.colors["grass"] and \
                        self.level_data.get_at((x+1, y-1)) == self.colors["grass"] and \
                        self.level_data.get_at((x-1, y)) == self.colors["bg"] and \
                        self.level_data.get_at((x+1, y)) == self.colors["grass"]:
                            sprite_chosen = self.get_grass_l()

                        #Side
                        elif self.level_data.get_at((x-1, y-1)) == self.colors["grass"] and \
                        self.level_data.get_at((x-1, y-1)) == self.colors["grass"] and \
                        self.level_data.get_at((x+1, y)) == self.colors["bg"] and \
                        self.level_data.get_at((x-1, y)) == self.colors["grass"]:
                            sprite_chosen = self.get_grass_r()

                        #Side
                        elif self.level_data.get_at((x, y-1)) == self.colors["grass"] and \
                        self.level_data.get_at((x+1, y-1)) == self.colors["grass"] and \
                        self.level_data.get_at((x-1, y-1)) == self.colors["grass"]:
                            sprite_chosen = self.get_grass_b()

                        #Side
                        elif self.level_data.get_at((x, y+1)) == self.colors["grass"] and \
                        self.level_data.get_at((x+1, y+1)) == self.colors["grass"] and \
                        self.level_data.get_at((x-1, y+1)) == self.colors["grass"]:
                            sprite_chosen = self.image_grass_t


                    except:
                        print "Out of range in {0},{1}".format(x,y)

                    if sprite_chosen == "center":
                        #Choose one random grass sprite
                        grass_choice = (x + y + random.randint(0,50)  ) % 4
                        sprite_chosen = self.get_grass_center()
                    self.blit(sprite_chosen, (x*self.ratio, y*self.ratio))

            self.limits.append(x_limits)

    def update(self):
        self.scroll(-1,0)
        self.scrolled+=1

    def checkcollide(self, rect):
        if rect.width > self.ratio:
            the_limits = self.limits[1+int(self.scrolled/self.ratio) + int(rect.left/self.ratio)]
        else:
            the_limits = self.limits[int(self.scrolled/self.ratio) + int(rect.left/self.ratio)]

        if the_limits[0] != 0 and the_limits[0]*self.ratio > rect.top:
            return True

        if the_limits[1] != 0 and the_limits[1]*self.ratio < rect.top:
            return True

        return False

    def get_grass_center(self):
        image_grass, rect_grass = utils.load_image('stage_grass_{0}.png'.format(random.randint(1,4)))
        return image_grass

    def get_grass_b(self):
        image_grass, rect_grass = utils.load_image('stage_grass_b_{0}.png'.format(random.randint(1,4)))
        return image_grass

    def get_grass_r(self):
        image_grass, rect_grass = utils.load_image('stage_grass_r_{0}.png'.format(random.randint(1,4)))
        return image_grass

    def get_grass_l(self):
        image_grass, rect_grass = utils.load_image('stage_grass_l_{0}.png'.format(random.randint(1,4)))
        return image_grass

#return the enemies in the current scroll position (self.scrolled + self.ratio).
#only return enemies if self.scrolled%self.ratio == 0 (each pixel in the stage is one enemy, not self.ratio
    def getenemies(self):
        enemies = []
        surf = pygame.display.get_surface()
        screen_width = int(surf.get_width() / self.ratio)

        if (self.scrolled%self.ratio == 0 ):
            for y in range(self.rect.height-1):
                x = int(self.scrolled/self.ratio)+screen_width
                if self.level_data.get_at((x, y)) == self.colors["enemies"]:
                    enemies.append(y*self.ratio)
        return enemies
        


        

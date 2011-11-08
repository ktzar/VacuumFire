import random
import pygame
import utils


"""Stage"""
class Stage(pygame.Surface):
    #TODO Load the cached image if present, and calculate its limits
    def __init__(self, stage_file='level_1'):
        self.level_data, self.rect = utils.load_image('{0}.gif'.format(stage_file))
        self.ratio = 16 #ratio of pixel in stage file / pixel in game
        self.limits_ratio = 8 #ratio of pixel in limits caculation
        pygame.Surface.__init__(self, (self.rect.width*self.ratio, self.rect.height*self.ratio))
        self.counter = 0
        self.scrolled = 0
        self.fill((0,0,0))
        self.set_colorkey((0,0,0))
        self.limits = []

        cached_image = False
        self.colors = { \
            "grass":(0,0,0,255), \
            "enemies":(255,0,0,255), \
            "miniboss":(0,0,255,255), \
            "boss":(0,255,0,255), \
            'bg':(229,229,229,255) \
        }
        #Using the previously generated image for the stage
        #TODO, create hash of the source image for the level, to detect changes in it
        try:
            cached_image, temp_rect = utils.load_image('level_1_processed.png')
            #To calculate averages
            accum = 0
            height = self.get_height()
            self.blit(cached_image, (0,0))
            for x in range(0,self.get_width(), self.limits_ratio):
                #find min and max limits every self.ratio pixels
                limit_top = False
                limit_bottom = False
                for y in range(height-1):
                    #search top limit
                    if limit_top == False and y > 0 and y < height - 30 and self.get_at((x,y)) == (0,0,0) and self.get_at((x,y-1)) != (0,0,0):
                        limit_top = int( y / self.ratio )+1
                    #search bottom limit
                    if limit_bottom == False and y < height and self.get_at((x,y)) == (0,0,0) and self.get_at((x,y+1)) != (0,0,0):
                        limit_bottom = int( y / self.ratio )-1
                    #both limits found, break to next column
                    if limit_top != False and limit_bottom != False:
                        break
                if limit_top == False:
                    limit_top = 0
                if limit_bottom == False:
                    limit_bottom = height / self.ratio
                self.limits.append([limit_top, limit_bottom])

                
        except pygame.error, message:
            print message
        except IndexError, message:
            print "{0},{1}".format(x,y)
            print message
        except :
            print 'No cached image, generating it'

        if cached_image == False:
            self.overimage, self.overrect = utils.load_image('lava.png')

            self.image_grass_bl, self.rect_grass = utils.load_image('stage_grass_bl.png')
            self.image_grass_br, self.rect_grass = utils.load_image('stage_grass_br.png')
            self.image_grass_tl, self.rect_grass = utils.load_image('stage_grass_tl.png')
            self.image_grass_tr, self.rect_grass = utils.load_image('stage_grass_tr.png')
            self.image_grass_t, self.rect_grass = utils.load_image('stage_grass_t.png')



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
            for x in range(self.get_width()):
                for y in range(self.get_height()):
                    if self.get_at((x,y)) != (0,0,0,255):
                        new_colour = self.get_at((x,y))
                        new_over = self.overimage.get_at((x%self.overrect.width,y%self.overrect.height))
                        new_colour.r = min(new_colour.r + new_over.r,200)
                        new_colour.g = min(new_colour.g + new_over.g,200)
                        new_colour.b = min(new_colour.b + new_over.b,200)
                        self.set_at((x,y), new_colour)
            utils.save_image('level_1_processed.png', self)

    def update(self):
        self.scroll(-1,0)
        self.scrolled+=1

    #returns 0 if no colission, 1 if colission on bottom, -1 if colission on top
    def checkcollide(self, rect):
        if rect.width > self.ratio:
            the_limits = self.limits[1+int(self.scrolled/self.limits_ratio) + int(rect.left/self.limits_ratio)]
        else:
            the_limits = self.limits[int(self.scrolled/self.limits_ratio) + int(rect.left/self.limits_ratio)]

        if the_limits[0] != 0 and the_limits[0]*self.ratio > rect.top:
            return -1

        if the_limits[1] != 0 and the_limits[1]*self.ratio < rect.top:
            return 1

        return 0

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
        enemies     = []
        minibosses  = []
        bosses      = []
        surf = pygame.display.get_surface()
        screen_width = int(surf.get_width() / self.ratio)

        if (self.scrolled%self.ratio == 0 ):
            for y in range(self.rect.height-1):
                x = int(self.scrolled/self.ratio)+screen_width
                if self.level_data.get_at((x, y)) == self.colors["enemies"]:
                    enemies.append(y*self.ratio)
                if self.level_data.get_at((x, y)) == self.colors["miniboss"]:
                    #So we don't load it again (when there's a miniboss present the stage doesn't scroll
                    self.level_data.set_at((x, y), self.colors["bg"])
                    minibosses.append(y*self.ratio)
                if self.level_data.get_at((x, y)) == self.colors["boss"]:
                    bosses.append(y*self.ratio)
        return (enemies,minibosses, bosses)

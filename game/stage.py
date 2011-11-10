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

        self.colors = { \
            "grass":(0,0,0,255), \
            "enemies":(255,0,0,255), \
            "miniboss":(0,0,255,255), \
            "boss":(0,255,0,255), \
            'bg':(229,229,229,255) \
        }

        cached_image = False
        #Using the previously generated image for the stage
        #TODO, create hash of the source image for the level, to detect changes in it
        
        self.rect = self.rect.move((1,0))
        try:
            #Load the cached image
            cached_image, temp_rect = utils.load_image('{0}_processed.png'.format(stage_file))
            self.blit(cached_image, (0,0))
            #Detect limits
            self.calculate_limits()

                
        except pygame.error, message:
            print message
        except IndexError, message:
            print message
        except Exception, message:
            print message
            print 'No cached image, generating it'
        except:
            print 'No cached image, generating it'

        level_md5 = utils.file_md5('{0}.gif'.format(stage_file))
        print "MD5 of level ",level_md5
        level_old_md5 = utils.get_option('{0}_hash'.format(stage_file))
        print "Old MD5 of level ",level_old_md5
        if level_md5 != level_old_md5:
            print "Level has changed, process it again"
            cached_image = False 

        if cached_image == False:
            self.overimage_lava, self.overrect_lava = utils.load_image('lava.png')
            self.overimage_rocks, self.overrect_rocks = utils.load_image('rocks.png')

            self.image_grass_bl, self.rect_grass = utils.load_image('stage_grass_bl.png')
            self.image_grass_br, self.rect_grass = utils.load_image('stage_grass_br.png')
            self.image_grass_tl, self.rect_grass = utils.load_image('stage_grass_tl.png')
            self.image_grass_tr, self.rect_grass = utils.load_image('stage_grass_tr.png')
            self.image_grass_t, self.rect_grass = utils.load_image('stage_grass_t.png')


                
            for x in range(0, self.rect.width-1):
                #will store top and bottom limits and append it to self.limits
                #to control the ship not getting over this
                for y in range(self.rect.height-1):

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

            self.calculate_limits()
            for x in range(self.get_width()):
                for y in range(self.get_height()):
                    if self.get_at((x,y)) != (0,0,0,255):
                        new_colour = self.get_at((x,y))
                        over_lava = self.overimage_lava.get_at((x%self.overrect_lava.width,y%self.overrect_lava.height))
                        over_rock = self.overimage_rocks.get_at((x%self.overrect_rocks.width,y%self.overrect_rocks.height))
                        #Processed colours should be between 1 and 250 (if it's 0,0,0 it'll be keyed)
                        new_colour.r = max(1,min(new_colour.r + over_lava.r*2 - over_rock.r/2,250))
                        new_colour.g = max(1,min(new_colour.g - over_lava.r - over_rock.r/2,250))
                        new_colour.b = max(1,min(new_colour.b - over_lava.r - over_rock.r/2,250))
                        """
                        this draws a ratio*ratio grid in the level, useful for some debugging
                        if x % self.ratio == 0 or y % self.ratio == 0:
                            new_colour = (0,0,255)
                            """
                        self.set_at((x,y), new_colour)
            utils.save_image('{0}_processed.png'.format(stage_file), self)
            level_md5 = utils.file_md5('{0}.gif'.format(stage_file))
            print "MD5 of stage: {0}".format(level_md5)
            utils.set_option('{0}_hash'.format(stage_file), level_md5)

    def calculate_limits(self):
        #TODO: cache limits, it takes a while to process them
        for x in range(self.rect.width-1):
            #will store top and bottom limits and append it to self.limits
            #to control the ship not getting over this
            x_limits = [-1,-1]
            for y in range(self.rect.height):
                #Calculate top and bottom limits
                if x_limits[0] == -1 and self.level_data.get_at((x,y)) != self.colors["grass"]:
                    x_limits[0] = y
                if x_limits[0] != -1 and x_limits[1] == -1 and self.level_data.get_at((x,y)) == self.colors["grass"]:
                    x_limits[1] = y
                """
                if y>0 and self.level_data.get_at((x,y)) == self.colors["grass"] and \
                self.level_data.get_at((x,y+1)) == self.colors["bg"]:
                    x_limits[0] = y+1
                if y<self.rect.height and self.level_data.get_at((x,y)) == self.colors["bg"] and \
                self.level_data.get_at((x,y+1)) == self.colors["grass"]:
                    x_limits[1] = y-1"""
            if x_limits[0] == -1:
                x_limits[0] = 0
            if x_limits[1] == -1:
                x_limits[1] = self.rect.height
            self.limits.append(x_limits)


    def update(self):
        self.scroll(-1,0)
        self.scrolled+=1

    def the_limits(self, rect):
        the_limits = self.limits[int(2*self.scrolled/self.ratio) + int(rect.left/self.ratio)]
        return the_limits

    #returns 0 if no colission, 1 if colission on bottom, -1 if colission on top
    def checkcollide(self, rect):
        the_limits = self.limits[int(2*self.scrolled/self.ratio) + int(rect.left/self.ratio)]
        if the_limits[0] != 0 and the_limits[0]*self.ratio > rect.top:
            collision_type = -1
        elif the_limits[1] != 31 and the_limits[1]*self.ratio < rect.top + rect.height:
            collision_type = 1
        else:
            collision_type = 0
        return collision_type

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
                    #So we don't load it again
                    self.level_data.set_at((x, y), self.colors["bg"])
                    enemies.append(y*self.ratio)
                if self.level_data.get_at((x, y)) == self.colors["miniboss"]:
                    #So we don't load it again (when there's a miniboss present the stage doesn't scroll
                    self.level_data.set_at((x, y), self.colors["bg"])
                    minibosses.append(y*self.ratio)
                if self.level_data.get_at((x, y)) == self.colors["boss"]:
                    #So we don't load it again (when there's a miniboss present the stage doesn't scroll
                    self.level_data.set_at((x, y), self.colors["bg"])
                    bosses.append(y*self.ratio)
        return (enemies,minibosses, bosses)
        


        

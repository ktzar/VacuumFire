import pygame
import utils

class Grass(pygame.sprite.Sprite):
    def __init__(self, pos):
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = utils.load_image('stage_grass.png')
        self.rect.top   = pos.top
        self.rect.left  = pos.left 

class Powerup(pygame.sprite.Sprite):
    def __init__(self, pos):
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = utils.load_image('item.png')
        self.rect.top   = pos.top 
        self.rect.left  = pos.left


"""Stage"""
class Stage(pygame.Surface):
    def __init__(self):
        self.level_data, self.rect = utils.load_image('level_1.gif')
        pygame.Surface.__init__(self, (self.rect.width*16, self.rect.height*16))
        self.counter = 0
        self.fill((0,0,0))
        self.set_colorkey((0,0,0))

        self.images_grass = []
        self.image_grass, self.rect_grass = utils.load_image('stage_grass_1.png')
        self.images_grass.append(self.image_grass)
        self.image_grass, self.rect_grass = utils.load_image('stage_grass_2.png')
        self.images_grass.append(self.image_grass)
        self.image_grass, self.rect_grass = utils.load_image('stage_grass_3.png')
        self.images_grass.append(self.image_grass)
        self.image_grass, self.rect_grass = utils.load_image('stage_grass_4.png')
        self.images_grass.append(self.image_grass)

        self.image_grass_bl, self.rect_grass = utils.load_image('stage_grass_bl.png')
        self.image_grass_br, self.rect_grass = utils.load_image('stage_grass_br.png')
        self.image_grass_tl, self.rect_grass = utils.load_image('stage_grass_tl.png')
        self.image_grass_tr, self.rect_grass = utils.load_image('stage_grass_tr.png')
        self.image_grass_b, self.rect_grass = utils.load_image('stage_grass_b.png')
        self.image_grass_r, self.rect_grass = utils.load_image('stage_grass_r.png')
        self.image_grass_l, self.rect_grass = utils.load_image('stage_grass_l.png')
        self.image_grass_t, self.rect_grass = utils.load_image('stage_grass_t.png')

        self.image_powerup, self.rect_grass = utils.load_image('item.png')

        colors = {"grass":(0,0,0,255), "powerup":(255,0,0,255)}

        self.rect = self.rect.move((1,0))
        for x in range(0, self.rect.width):
            for y in range(self.rect.height):
                if self.level_data.get_at((x,y)) == colors["powerup"]:
                    self.blit(self.image_powerup, (x*16, y*16))
                elif self.level_data.get_at((x,y)) == colors["grass"]:
                    try:
                        sprite_chosen = "center"
                        if y == 0 or x == 0:
                            sprite_chosen = "center"
                        #Grass surrounded by grass
                        elif self.level_data.get_at((x-1, y)) == colors["grass"] and \
                        self.level_data.get_at((x+1, y)) == colors["grass"] and \
                        self.level_data.get_at((x, y-1)) == colors["grass"] and \
                        self.level_data.get_at((x, y+1)) == colors["grass"]:
                            sprite_chosen = "center"

                        #Corner
                        elif self.level_data.get_at((x-1, y)) != colors["grass"] and\
                        self.level_data.get_at((x-1, y-1)) != colors["grass"] and \
                        self.level_data.get_at((x, y-1)) != colors["grass"]:
                            sprite_chosen = self.image_grass_tl

                        #Corner
                        elif self.level_data.get_at((x+1, y)) != colors["grass"] and\
                        self.level_data.get_at((x+1, y-1)) != colors["grass"] and \
                        self.level_data.get_at((x, y-1)) != colors["grass"]:
                            sprite_chosen = self.image_grass_tr

                        #Corner
                        elif self.level_data.get_at((x-1, y)) != colors["grass"] and\
                        self.level_data.get_at((x-1, y+1)) != colors["grass"] and \
                        self.level_data.get_at((x, y+1)) != colors["grass"]:
                            sprite_chosen = self.image_grass_bl

                        #Corner
                        elif self.level_data.get_at((x+1, y)) != colors["grass"] and\
                        self.level_data.get_at((x+1, y+1)) != colors["grass"] and \
                        self.level_data.get_at((x, y+1)) != colors["grass"]:
                            sprite_chosen = self.image_grass_br

                        #Side
                        elif self.level_data.get_at((x, y-1)) == colors["grass"] and \
                        self.level_data.get_at((x+1, y-1)) == colors["grass"] and \
                        self.level_data.get_at((x-1, y-1)) == colors["grass"]:
                            sprite_chosen = self.image_grass_b

                        #Side
                        elif self.level_data.get_at((x, y+1)) == colors["grass"] and \
                        self.level_data.get_at((x+1, y+1)) == colors["grass"] and \
                        self.level_data.get_at((x-1, y+1)) == colors["grass"]:
                            sprite_chosen = self.image_grass_t

                        #Side
                        elif self.level_data.get_at((x+1, y-1)) == colors["grass"] and \
                        self.level_data.get_at((x+1, y-1)) == colors["grass"] and \
                        self.level_data.get_at((x+1, y)) == colors["grass"]:
                            sprite_chosen = self.image_grass_l

                        #Side
                        elif self.level_data.get_at((x-1, y-1)) == colors["grass"] and \
                        self.level_data.get_at((x-1, y-1)) == colors["grass"] and \
                        self.level_data.get_at((x-1, y)) == colors["grass"]:
                            sprite_chosen = self.image_grass_r

                    except:
                        print "Out of range in {0},{1}".format(x,y)

                    if sprite_chosen == "center":
                        #Choose one random grass sprite
                        grass_choice = (x + y ) % 4
                        sprite_chosen = self.images_grass[grass_choice]
                    self.blit(sprite_chosen, (x*16, y*16))


    def update(self):
        self.scroll(-1,0)
        

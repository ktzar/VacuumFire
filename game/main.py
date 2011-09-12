#Import Modules
import os, pygame, time
import random
from pygame.locals import *
import utils
from ship import Ship
from laser import Laser
from alien import Alien
from stage import Stage
from explosion import Explosion
from life_meter import LifeMeter
from background import Background


class Vacuum():

    def __init__(self):
        if not pygame.font: print 'Warning, fonts disabled'
        if not pygame.mixer: print 'Warning, sound disabled'
        self.init()
        self.loop()

    def init(self):
        """this function is called when the program starts.
           it initializes everything it needs, then runs in
           a loop until the function returns."""
    #Initialize Everything
        pygame.init()
        self.screen = pygame.display.set_mode((640, 480))
        pygame.display.set_caption('Ships')
        pygame.mouse.set_visible(0)

    #sounds
        self.music = utils.load_sound('archivo.ogg')
        self.warning = utils.load_sound('warning.ogg')
        #music.play()

    #Create The Backgound
        self.background = Background(self.screen.get_size())

    #game variables
        self.score = 0

    #Display The Background
        self.screen.blit(self.background, (0, 0))
        pygame.display.flip()


    #The player's ship
        self.ship = Ship()
    #The player's ship
        self.lifemeter = LifeMeter()

        self.player    = pygame.sprite.RenderPlain((self.ship))
    #group that stores all enemies
        self.enemies    = pygame.sprite.Group()
    #group that stores all the lasers the player shoots
        self.fire        = pygame.sprite.Group()
    #group for information sprites in the screen, should be rendered the last one
        self.hud         = pygame.sprite.Group()
        self.explosions  = pygame.sprite.Group()
        self.hud.add(self.lifemeter)
        self.level = Stage()
        self.font = utils.load_font('4114blasterc.ttf', 36)


        self.clock = pygame.time.Clock()

        self.game_started = False
        self.game_finished = False


    def loop(self):
    #Main Loop
        count = 0
        while 1:
            count = (count+1)%50
            self.clock.tick(50)


    #Handle Input Events
            for event in pygame.event.get():
                if event.type == QUIT:
    #exit
                    return
                elif event.type == KEYDOWN and event.key == K_ESCAPE and self.game_finished == True:
                    pygame.quit()
                    quit()
                    
                if event.type == KEYDOWN:
                    self.game_started = True
                    if event.key == K_ESCAPE:
                        return    #exit
                    elif event.key == K_SPACE:
        #shoot a laser if the max number is not reached
                        if Laser.num < Laser.max_lasers:
                            self.laser = Laser(self.ship)
                        self.fire.add(self.laser)
                    elif event.key == K_LEFT:
                        self.ship.move_left()
                    elif event.key == K_RIGHT:
                        self.ship.move_right()
                    elif event.key == K_UP:
                        self.ship.move_up()
                    elif event.key == K_DOWN:
                        self.ship.move_down()

                if event.type == KEYUP:
                    if event.key == K_LEFT:
                        self.ship.stop_move_left()
                    elif event.key == K_RIGHT:
                        self.ship.stop_move_right()
                    elif event.key == K_UP:
                        self.ship.stop_move_up()
                    elif event.key == K_DOWN:
                        self.ship.stop_move_down()

            if self.game_started == False:
                start_text = self.font.render('Press any key to start', 2, (0,0,0))
                self.screen.blit(start_text, (150, 200))
                pygame.display.flip()
                continue

            new_enemies = self.level.getenemies() 

            for enemy_y in new_enemies:
            #if random.randint(0,50) == 0:
                alien = Alien(enemy_y)
                alien.set_target(self.ship)
                self.enemies.add(alien)

    #aliens damaging the player, remove them
            damage  = pygame.sprite.spritecollide(self.ship, self.enemies, True)

    #check colisions with stage
            if self.level.checkcollide(self.ship.rect):
    #add some fancy explosions in the damage area
                self.explosions.add(Explosion(pygame.Rect(self.ship.rect.x,self.ship.rect.y,0,0)))
                damage.append(1)

            if len(damage) > 0:
                self.background.warning()
                self.ship.damage()
                self.lifemeter.shake()
                self.warning.play()
                self.lifemeter.life = self.ship.life
                if self.lifemeter.life < 1:
                    self.game_finished = True
                    self.warning.stop()

            #print (pygame.sprite.spritecollide(ship, level, True))

    #aliens hit by the fire, remove them
            for fireball in self.fire:
                hit = pygame.sprite.spritecollide(fireball, self.enemies, True)
                for dead in hit:
                    self.explosions.add(Explosion(pygame.Rect(dead.rect.x,dead.rect.y,0,0)))
                    self.score+=dead.value*1000

    #draw the level

            all_sprites = pygame.sprite.Group()
            all_sprites.add(self.player.sprites())
            all_sprites.add(self.enemies.sprites())
            all_sprites.add(self.fire.sprites())
            all_sprites.add(self.hud.sprites())
            all_sprites.add(self.explosions.sprites())
            all_sprites.update()
            self.level.update()
            self.background.update()

    #Move and draw the background

            score_text = 'Score: {0}'.format((self.score))

            text = self.font.render(score_text, 1, (255, 255, 255))

            self.screen.blit(self.background, (0, 0))
            self.screen.blit(self.level, (0, 0))
            self.screen.blit(text, (10, 10))

            if self.game_finished == True:
                gameover_text = self.font.render("Game Over", 2, (255, 255, 255))
                self.screen.blit(gameover_text, (280, 200))
                gameover_text = self.font.render("Press Esc", 2, (255, 255, 255))
                self.screen.blit(gameover_text, (280, 230))
            else:
                all_sprites.draw(self.screen)

    #draw all the groups of sprites

            pygame.display.flip()

    #Game Over



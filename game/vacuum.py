#Import Modules
import os, pygame, time
import random
from pygame.locals import *
from . import utils
from .ship       import Ship
from .laser      import *
from .powerup    import Powerup
from .enemies    import *
from .stage      import Stage
from .explosion  import Explosion
from .life_meter import LifeMeter
from .background import Background
from .meters     import *
from .sprites    import *

show_dummies = False

class Vacuum():

    def __init__(self, screen):
        self.screen = screen

        self.game_paused = False
        #sounds
        self.sounds = {};
        self.sounds['warning'] = utils.load_sound('warning.wav')
        self.sounds['powerup'] = utils.load_sound('powerup.wav')
        #Load explosions
        a = Explosion(pygame.Rect(0,0,10,10))
        #Create The Backgound
        self.background = Background(self.screen.get_size())
        #game variables
        self.score = Score_Meter((10,10))
        #Display The Background
        self.screen.blit(self.background, (0, 0))

        font = utils.load_font('4114blasterc.ttf', 36)
        text_color = (255,255,255)
        text = font.render("Initialising", 1, text_color)
        self.screen.blit(text, (200, 300))
        pygame.display.flip()

        if show_dummies:
            self.dummy = Dummy()
            self.dummy2 = Dummy()

        #The player's ship
        self.ship = Ship()
        #The dash indicators
        self.lifemeter = LifeMeter()
        self.powerup_speed  = SpeedMeter(pygame.Rect(500,400,0,0))
        self.powerup_weapon = WeaponMeter(pygame.Rect(540,400,0,0))
        self.powerup_buddy  = BuddyMeter(pygame.Rect(580,400,0,0))

        self.player    = pygame.sprite.RenderPlain((self.ship))
        self.buddies   = pygame.sprite.Group()
        #self.buddies.add(Buddy(self.ship)) # add a testing buddy
        #self.ship.buddies += 1
        #group that stores all enemies
        self.enemies    = pygame.sprite.Group()
        self.minibosses = pygame.sprite.Group()
        #group that stores all powerups
        self.powerups   = pygame.sprite.Group()
        #group that stores all the lasers the player shoots
        self.fire       = pygame.sprite.Group()
        #group for information sprites in the screen, should be rendered the last one
        self.hud         = pygame.sprite.Group()
        self.explosions  = pygame.sprite.Group()
        self.enemylasers = pygame.sprite.Group()
        self.hud.add(self.lifemeter)
        self.hud.add(self.score)
        self.hud.add((self.powerup_speed, self.powerup_weapon, self.powerup_buddy))
        if show_dummies:
            self.hud.add(self.dummy)
            self.hud.add(self.dummy2)
        #The level
        self.level = Stage('level_1')
        self.font = utils.load_font('4114blasterc.ttf', 36)

        self.game_started       = True
        self.game_finished      = False
        self.level_finished     = False
        self.scene_finished     = False

    def handle_keys(self):
        #Handle Input Events
        for event in pygame.event.get():
            if event.type == QUIT:
                #exit
                return
            elif event.type == KEYDOWN and event.key == K_ESCAPE and self.game_finished == False:
                self.game_finished = True
            elif event.type == KEYDOWN and event.key == K_ESCAPE and self.game_finished == True:
                self.scene_finished = True

            if event.type == KEYDOWN:
                self.game_started = True
                if event.key == K_ESCAPE:
                    return False   #exit
                elif event.key == K_SPACE:
                    #shoot a laser if the max number is not reached
                    if Laser.num < Laser.max_lasers:
                        #print "There's {0} lasers in the screen and the max is {1}".format(Laser.num, Laser.max_lasers)
                        laser = Laser(self.ship)
                        self.fire.add(laser)
                        if self.ship.buddies > 0:
                            self.fire.add(DiagonalLaser(self.ship, "up"))
                        if self.ship.buddies > 1:
                            self.fire.add(DiagonalLaser(self.ship, "down"))
                        if self.ship.buddies > 2:
                            self.fire.add(DiagonalLaser(self.ship, "back"))
                elif event.key == K_LEFT:
                    self.ship.move_left()
                elif event.key == K_RIGHT:
                    self.ship.move_right()
                elif event.key == K_UP:
                    self.ship.move_up()
                elif event.key == K_DOWN:
                    self.ship.move_down()
                elif event.key == K_p:
                    self.game_paused = not self.game_paused

            if event.type == KEYUP:
                if event.key == K_LEFT:
                    self.ship.stop_move_left()
                elif event.key == K_RIGHT:
                    self.ship.stop_move_right()
                elif event.key == K_UP:
                    self.ship.stop_move_up()
                elif event.key == K_DOWN:
                    self.ship.stop_move_down()

        return True

    def process_powerups(self):
        #powerups got by the player, remove them, play a sound and apply them
        powerups_obtained  = pygame.sprite.spritecollide(self.ship, self.powerups, True)
        for powerup_obtained in powerups_obtained:
            #play powerup sound
            self.sounds['powerup'].play()
            self.score.add_score(powerup_obtained.value)
            #TODO powerup should be processed in ship
            print('powerup:',powerup_obtained.type)
            label_pos = self.ship.rect.copy()
            label_pos.top -= 20
            if powerup_obtained.type == 0:
                self.ship.life_up()
                self.hud.add(Flying_Label( label_pos, 'Energy'))
                self.lifemeter.life = self.ship.life
            elif powerup_obtained.type == 1 and self.ship.powerup['speedup'] < 5:
                self.ship.powerup['speedup'] += 1 
                self.powerup_speed.set_status(self.ship.powerup['speedup'])
                self.hud.add(Flying_Label( label_pos, 'Speed up'))
                #print "Increase speed to {0}".format(self.ship.powerup['speedup'])
            elif powerup_obtained.type == 2 and Laser.max_lasers < 5:
                Laser.max_lasers += 1 
                Laser.move += 2 
                self.powerup_weapon.set_status(Laser.max_lasers)
                print("Increase lasers to {0}".format(Laser.max_lasers))
                self.hud.add(Flying_Label( label_pos, 'Lasers'))

            elif powerup_obtained.type == 3 and self.ship.powerup['penetrate'] == False:
                print("Activate penetration")
                self.hud.add(Flying_Label( label_pos, 'Penetration'))
                self.ship.powerup['penetrate'] = True
            elif powerup_obtained.type == 4:
                print("Activate buddy")
                self.buddies.add(Buddy(self.ship))
                self.ship.buddies += 1
                self.powerup_buddy.set_status(self.ship.buddies)
            else:
                print("No more powerups available")
            del label_pos

    def add_explosion(self, rect):
        self.explosions.add(Explosion(rect.copy()))

    def add_enemylaser(self, laser):
        self.enemylasers.add(laser)

    def process_stagecollisions(self):
        damage = []
        #check colisions with stage
        side = self.level.checkcollide(self.ship.rect)
        if side != 0:
            #add some fancy explosions in the damage area
            self.explosions.add(Explosion(pygame.Rect(self.ship.rect.x,self.ship.rect.y + side *self.ship.rect.height,0,0)))
            damage.append(1)
        return damage

    def process_damage(self, damage):
        #Apply damages to the player
        if len(damage) > 0:
            self.background.warning()
            self.ship.damage()
            self.lifemeter.shake()
            self.add_explosion(self.ship.rect)
            self.sounds['warning'].play()
            self.lifemeter.life = self.ship.life
            if self.lifemeter.life < 1:
                self.game_finished = True
                self.sounds['warning'].stop()

    def process_killedaliens(self):
        #aliens hit by the fire, remove them
        penetration = self.ship.powerup['penetrate']
        for fireball in self.fire:
            hit     = pygame.sprite.spritecollide(fireball, self.enemies, True)
            #Check collisions with masks since the minibosses can have funny shapes
            enemies_hit = []
            for miniboss in self.minibosses:
                if pygame.sprite.collide_mask(fireball, miniboss):
                    fireball.kill()
                    enemies_hit.append(miniboss)

            for strike in enemies_hit:
                strike.hit()

            hit.extend(enemies_hit)
            for dead in hit:
                if dead.has_powerup():
                    powerup = Powerup(dead.rect, dead.value)
                    self.powerups.add(powerup)
                self.add_explosion(fireball.rect)
                scored = (1+dead.value)*1000
                self.score.add_score(scored)
                self.hud.add(Flying_Label( fireball.rect, scored))
                if penetration == False:
                    fireball.kill()

    #Main Loop
    def loop(self):
        count = 0
        count = (count+1)%50

        #handle input events
        ok = self.handle_keys()
        if ok == False:
            return

        if self.game_started == False:
            start_text = self.font.render('Press any key to start', 2, (0,0,0))
            self.screen.blit(start_text, (150, 200))
            pygame.display.flip()
            return

        if self.game_paused == 1:
            start_text = self.font.render('Game paused', 2, (255,255,255))
            self.screen.blit(start_text, (150, 200))
            pygame.display.flip()
            return

        try:
            (new_enemies, new_minibosses, new_bosses, end) = self.level.getenemies() 
            for enemy_y in new_enemies:
                alien = Alien(enemy_y)
                alien.set_target(self.ship)
                self.enemies.add(alien)

            for enemy_y in new_minibosses:
                miniboss = Miniboss(enemy_y, self)
                miniboss.set_target(self.ship)
                self.minibosses.add(miniboss)
            if end:
                self.level_finished = True

        except ValueError:
            self.level_finished = True

        #aliens damaging the player, remove them
        damage  = pygame.sprite.spritecollide(self.ship, self.enemies, True)
        damage.extend(pygame.sprite.spritecollide(self.ship, self.enemylasers, True))
        for miniboss in self.minibosses:
            if pygame.sprite.collide_mask(self.ship, miniboss):
                damage.append(miniboss)
        self.process_powerups()
        collisions = self.process_stagecollisions()
        for collision in collisions:
            damage.append(1)
        self.process_damage(damage)
        self.process_killedaliens()


        #Dummy lines to show the ship's current limits
        if show_dummies:
            the_limits = self.level.the_limits(self.ship.rect)
            self.dummy.rect.top = the_limits[0]*self.level.ratio
            self.dummy2.rect.top = the_limits[1]*self.level.ratio
            self.dummy.rect.height = 2
            self.dummy2.rect.height = 2
            self.dummy.rect.left = self.ship.rect.left
            self.dummy2.rect.left = self.ship.rect.left

        #draw the level
        all_sprites = pygame.sprite.Group()
        all_sprites.add(self.player.sprites())
        all_sprites.add(self.enemies.sprites())
        all_sprites.add(self.minibosses.sprites())
        all_sprites.add(self.powerups.sprites())
        all_sprites.add(self.buddies.sprites())
        all_sprites.add(self.fire.sprites())
        all_sprites.add(self.enemylasers.sprites())
        all_sprites.add(self.hud.sprites())
        all_sprites.add(self.explosions.sprites())
        all_sprites.update()
        if len(self.minibosses.sprites()) == 0:
            self.level.update()
        self.background.update()

        #Move and draw the background

        self.screen.blit(self.background, (0, 0))
        self.screen.blit(self.level, (-self.level.scrolled, 0))

        if self.level_finished == True:
            level_text = self.font.render("Level finished", 2, (255, 255, 255))
            self.screen.blit(level_text, (280, 200))
        elif self.game_finished == True:
            gameover_text = self.font.render("Game Over", 2, (255, 255, 255))
            self.screen.blit(gameover_text, (280, 200))
            gameover_text = self.font.render("Press Esc", 2, (255, 255, 255))
            self.screen.blit(gameover_text, (280, 230))
        else:
            all_sprites.draw(self.screen)
            all_sprites.empty()

        #draw all the groups of sprites

    #Game Over



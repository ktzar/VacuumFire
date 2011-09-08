#Import Modules
import os, pygame
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

if not pygame.font: print 'Warning, fonts disabled'
if not pygame.mixer: print 'Warning, sound disabled'

def gameover():
    print "Game Over"
    pygame.quit()
    quit()


def main():
    """this function is called when the program starts.
       it initializes everything it needs, then runs in
       a loop until the function returns."""
#Initialize Everything
    pygame.init()
    screen = pygame.display.set_mode((640, 480))
    pygame.display.set_caption('Ships')
    pygame.mouse.set_visible(0)

#sounds
    music = utils.load_sound('archivo.ogg')
    warning = utils.load_sound('warning.ogg')
    music.play()

#Create The Backgound
    background = Background(screen.get_size())

#game variables
    score = 0

#Display The Background
    screen.blit(background, (0, 0))
    pygame.display.flip()

#The player's ship
    ship = Ship()
#The player's ship
    lifemeter = LifeMeter()

    player    = pygame.sprite.RenderPlain((ship))
#group that stores all enemies
    enemies    = pygame.sprite.Group()
#group that stores all the lasers the player shoots
    fire        = pygame.sprite.Group()
#group for information sprites in the screen, should be rendered the last one
    hud         = pygame.sprite.Group()
    explosions  = pygame.sprite.Group()
    hud.add(lifemeter)
    level = Stage()
    font = utils.load_font('4114blasterc.ttf', 36)

    clock = pygame.time.Clock()

    game_started = False

#Main Loop
    count = 0
    while 1:
        count = (count+1)%50
        clock.tick(100)

#Handle Input Events
        for event in pygame.event.get():
            if event.type == QUIT:
#exit
                return
            elif event.type == KEYDOWN and event.key == K_ESCAPE:
#exit
                return
            elif event.type == KEYDOWN and event.key == K_SPACE:
#shoot a laser if the max number is not reached
                if Laser.num < Laser.max_lasers:
                    laser = Laser(ship)
                fire.add(laser)
            elif event.type == KEYDOWN and event.key == K_LEFT:
                ship.move_left()
            elif event.type == KEYDOWN and event.key == K_RIGHT:
                ship.move_right()
            elif event.type == KEYUP and event.key == K_LEFT:
                ship.stop_move_left()
            elif event.type == KEYUP and event.key == K_RIGHT:
                ship.stop_move_right()
            elif event.type == KEYDOWN and event.key == K_UP:
                ship.move_up()
            elif event.type == KEYDOWN and event.key == K_DOWN:
                ship.move_down()
            elif event.type == KEYUP and event.key == K_UP:
                ship.stop_move_up()
            elif event.type == KEYUP and event.key == K_DOWN:
                ship.stop_move_down()
            elif event.type == KEYDOWN:
                game_started = True

        if game_started == False:
            continue

        if random.randint(0,50) == 0:
            alien = Alien()
            alien.set_target(ship)
            enemies.add(alien)

#aliens damaging the player, remove them
        damage  = pygame.sprite.spritecollide(ship, enemies, True)
        if len(damage) > 0:
            background.warning()
            ship.damage()
            lifemeter.shake()
            warning.play()
            lifemeter.life = ship.life
            if lifemeter.life == 0:
                gameover()

        #print (pygame.sprite.spritecollide(ship, level, True))

#aliens hit by the fire, remove them
        for fireball in fire:
            hit = pygame.sprite.spritecollide(fireball, enemies, True)
            for dead in hit:
                explosions.add(Explosion(pygame.Rect(dead.rect.x,dead.rect.y,0,0)))
                score+=dead.value*1000

#draw the level

        all_sprites = pygame.sprite.Group()
        all_sprites.add(player.sprites())
        all_sprites.add(enemies.sprites())
        all_sprites.add(fire.sprites())
        all_sprites.add(hud.sprites())
        all_sprites.add(explosions.sprites())
        all_sprites.update()
        level.update()
        background.update()

#Move and draw the background

        score_text = 'Score: {0}'.format((score))

        text = font.render(score_text, 1, (255, 255, 255))

        screen.blit(background, (0, 0))
        screen.blit(level, (0, 0))
        screen.blit(text, (10, 10))

#draw all the groups of sprites
        all_sprites.draw(screen)

        pygame.display.flip()

#Game Over



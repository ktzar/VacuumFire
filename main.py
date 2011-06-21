#Import Modules
import os, pygame
import random
from pygame.locals import *
import utils
from ship import Ship
from laser import Laser
from alien import Alien
from explosion import Explosion
from life_meter import LifeMeter

if not pygame.font: print 'Warning, fonts disabled'
if not pygame.mixer: print 'Warning, sound disabled'

""" TODO 
Add better collisions
Add subclasses of Alien with different damage
Add explosions to Alien dying
Add image for the background with walls
Add laser limit
Add gameover
Add sprites for the ship moving up and down
"""

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
    sound_bomb = utils.load_sound('bomb-02.wav')
    sound_laser = utils.load_sound('laser-01.wav')
    music = utils.load_sound('archivo.ogg')
    music.play()

#Create The Backgound
    background = pygame.Surface(screen.get_size())
    background = background.convert()
    background.fill((250, 250, 250))
    back_image, back_rect = utils.load_image('background.jpg');
    back_rect_init = back_rect.copy()
    background.blit(back_image, back_rect)

#game variables
    score = 0

#Display The Background
    screen.blit(background, (0, 0))
    pygame.display.flip()

    ship = Ship()
    lifemeter = LifeMeter()

    good_guy    = pygame.sprite.RenderPlain((ship))
    bad_guys    = pygame.sprite.Group()
    fire        = pygame.sprite.Group()
    hud         = pygame.sprite.Group()
    explosions  = pygame.sprite.Group()
    hud.add(lifemeter)
    font = utils.load_font('4114blasterc.ttf', 36)

    clock = pygame.time.Clock()

    game_started = False

#Main Loop
    while 1:
        clock.tick(50)

        #Handle Input Events
        for event in pygame.event.get():
            if event.type == QUIT:
                return
            elif event.type == KEYDOWN and event.key == K_ESCAPE:
                return
            elif event.type == KEYDOWN and event.key == K_SPACE:
                laser = Laser(ship)
                fire.add(laser)
                sound_laser.play()
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
            bad_guys.add(alien)


        #aliens damaging the player, remove them
        damage  = pygame.sprite.spritecollide(ship, bad_guys, True)
        if len(damage) > 0:
            ship.damage()
            lifemeter.life = ship.life

        #aliens hit by the fire, remove them
        for fireball in fire:
            hit = pygame.sprite.spritecollide(fireball, bad_guys, True)
            for dead in hit:
                explosions.add(Explosion(pygame.Rect(dead.rect.x,dead.rect.y,0,0)))
                print 'Win {0}'.format((dead.value*1000))
                score+=dead.value*1000
                sound_bomb.play()

        all_sprites = pygame.sprite.Group()
        all_sprites.add(good_guy.sprites())
        all_sprites.add(bad_guys.sprites())
        all_sprites.add(fire.sprites())
        all_sprites.add(hud.sprites())
        all_sprites.add(explosions.sprites())
        all_sprites.update()

        #Draw Everything
        back_rect = back_rect.move((-1,0))
        background.blit(back_image, back_rect)
        score_text = 'Score: {0}'.format((score))

        text = font.render(score_text, 1, (255, 255, 255))
        background.blit(text, (10, 10))

        #Repeat the background
        if -back_rect.left > back_rect_init.width-screen.get_size()[0]:
            back_rect = back_rect_init.copy()
        screen.blit(background, (0, 0))

        #draw all the groups of sprites
        all_sprites.draw(screen)

        pygame.display.flip()

#Game Over


#this calls the 'main' function when this script is executed
if __name__ == '__main__': main()

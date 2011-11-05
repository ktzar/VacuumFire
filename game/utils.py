import os, pygame
from pygame.locals import *

data_directory = 'data'

#loads an image and returns it with the Rect
def load_image(name, colorkey=None):
    fullname = os.path.join(data_directory, name)
    try:
        image = pygame.image.load(fullname)
    except pygame.error, message:
        print 'Cannot load image:', fullname
        raise SystemExit, message
    image = image.convert_alpha()
    if colorkey is not None:
        if colorkey is -1:
            colorkey = image.get_at((0,0))
        image.set_colorkey(colorkey, RLEACCEL)
    return image, image.get_rect()

def save_image(name, surface):
    fullname = os.path.join(data_directory, name)
    print fullname
    try:
        pygame.image.save(surface, fullname)
    except pygame.error, message:
        print 'cannot save image: ',pygame.error, message

#loads a part of an image and returns it with the Rect
def load_image_sprite(name, colorkey=None, rect=pygame.Rect(0,0,10,10)):
    fullname = os.path.join(data_directory, name)
    try:
        image = pygame.image.load(fullname)
    except pygame.error, message:
        print 'Cannot load image:', fullname
        raise SystemExit, message
    image = image.convert_alpha()
    if colorkey is not None:
        if colorkey is -1:
            colorkey = image.get_at((0,0))
        image.set_colorkey(colorkey, RLEACCEL)
    return image.subsurface(rect), rect

#Loads a sound from the directory
def load_sound(name):
    class NoneSound:
        def play(self): pass
    if not pygame.mixer or not pygame.mixer.get_init():
        return NoneSound()
    fullname = os.path.join(data_directory, name)
    try:
        sound = pygame.mixer.Sound(fullname)
    except pygame.error, message:
        print 'Cannot load sound:', fullname
        raise SystemExit, message
    return sound

def load_font(name, size=36):
    if not pygame.font:
        print 'Fonts not available'
    fullname = os.path.join(data_directory, name)
    font = pygame.font.Font(fullname, size)
    return font

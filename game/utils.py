import os, pygame, hashlib, pickle
from functools import partial

from pygame.locals import *

def file_md5(filename):
    md5 = hashlib.md5()
    with open(os.path.join(data_directory,filename), mode='rb') as f: 
        for chunk in iter(partial(f.read, 128), b''): 
            md5.update(chunk)
    return md5.digest()

data_directory = 'data'


def get_option(key):
    try:
        options = pickle.load( open( os.path.join(data_directory,"options.p"), "rb" ) )
    except IOError:
        options = {}
        pickle.dump( options, open( os.path.join(data_directory,"options.p"), "wb" ) )

    if key in options:
        return options[key]
    else:
        return False

def set_option(key, value):
    try:
        options = pickle.load( open( os.path.join(data_directory,"options.p"), "rb" ) )
    except IOError:
        options = {}
        pickle.dump( options, open( os.path.join(data_directory,"options.p"), "wb" ) )
    options[key] = value
    pickle.dump( options, open( os.path.join(data_directory,"options.p"), "wb" ) )



#loads an image and returns it with the Rect
def load_image(name, colorkey=None):
    fullname = os.path.join(data_directory, name)
    try:
        image = pygame.image.load(fullname)
    except pygame.error as message:
        print('Cannot load image:', fullname)
        raise SystemExit(message)
    image = image.convert_alpha()
    if colorkey != None:
        if colorkey == -1:
            colorkey = image.get_at((0,0))
        image.set_colorkey(colorkey, RLEACCEL)
    return image, image.get_rect()

def save_image(name, surface):
    fullname = os.path.join(data_directory, name)
    print(fullname)
    try:
        pygame.image.save(surface, fullname)
    except pygame.error as message:
        print('cannot save image: ',pygame.error, message)

#loads a part of an image and returns it with the Rect
def load_image_sprite(name, colorkey=None, rect=pygame.Rect(0,0,10,10)):
    fullname = os.path.join(data_directory, name)
    try:
        image = pygame.image.load(fullname)
    except pygame.error as message:
        print('Cannot load image:', fullname)
        raise SystemExit(message)
    image = image.convert_alpha()
    if colorkey != None:
        if colorkey == -1:
            colorkey = image.get_at((0,0))
        image.set_colorkey(colorkey, RLEACCEL)
    return image.subsurface(rect), rect

#Loads a sound from the directory
def load_sound(name):
    class NoneSound:
        def play(self): pass
        def stop(self): pass
    if not pygame.mixer or not pygame.mixer.get_init():
        return NoneSound()
    fullname = os.path.join(data_directory, name)
    try:
        sound = pygame.mixer.Sound(fullname)
    except pygame.error as message:
        print('Cannot load sound:', fullname)
        raise SystemExit(message)
    return sound

def load_font(name, size=36):
    if not pygame.font:
        print('Fonts not available')
    fullname = os.path.join(data_directory, name)
    font = pygame.font.Font(fullname, size)
    return font

import pygame
import sys

# Default Sizes and Values
_BORDER = 0
_DEFAULT_XMIN = 0.0
_DEFAULT_XMAX = 1.0
_DEFAULT_YMIN = 0.0
_DEFAULT_YMAX = 1.0
_DEFAULT_SIZE = 512

_xmin = None
_ymin = None
_xmax = None
_ymax = None

_width = _DEFAULT_SIZE
_height = _DEFAULT_SIZE
_keysTyped = []

#-----------------------------------------------------------------------
# Private functions to scale and factor X and Y values
def _scaleX(x):
    return _width * (x - _xmin) / (_xmax - _xmin)

def _scaleY(y):
    return _height * (_ymax - y) / (_ymax - _ymin)

def _factorX(w):
    return w * _width / abs(_xmax - _xmin)

def _factorY(h):
    return h * _height / abs(_ymax - _ymin)

#-----------------------------------------------------------------------
def create_window(w=_DEFAULT_SIZE, h=_DEFAULT_SIZE):
    """
    Create the stddraw window.
    """
    pygame.init()
    global _surface
    global _width
    global _height
    if (w < 1) or (h < 1):
        raise Exception('width and height must be positive')
    _width = w
    _height = h
    _background = pygame.display.set_mode([w, h])
    pygame.display.set_caption('pygame window')
    _surface = pygame.Surface((w, h))
    _surface.fill(pygame.Color(255, 255, 255))
    #clear()

def setXscale(min=_DEFAULT_XMIN, max=_DEFAULT_XMAX):
    """
    Set the x-scale of the surface such that the minimum x value is
    min and the maximum x value is max.
    """
    global _xmin
    global _xmax
    size = max - min
    _xmin = min - _BORDER * size
    _xmax = max + _BORDER * size

def setYscale(min=_DEFAULT_YMIN, max=_DEFAULT_YMAX):
    """
    Set the y-scale of the surface such that the minimum y value is
    min and the maximum y value is max.
    """
    global _ymin
    global _ymax
    size = max - min
    _ymin = min - _BORDER * size
    _ymax = max + _BORDER * size

def sleep(t):
    """
    Sleep for t milliseconds.
    """
    time.sleep(float(t) / 1000.0)

def poll():
    """
    Show the surface on the window.
    """
    pygame.display.flip()
    _checkForEvents()

def wait():
    """
    Wait for the user to close the window.
    """
    while True:
        _checkForEvents()

def _checkForEvents():
    """
    Check if any new event has occured (such as a key typed or button
    pressed).  If a key has been typed, then put that key in a queue.
    """
    global _surface
    global _keysTyped
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            _keysTyped = [event.unicode] + _keysTyped

#-----------------------------------------------------------------------
# Functions for retrieving keys
def has_next_key_typed():
    """
    Return True iff the queue of keys the user typed is not empty.
    """
    global _keysTyped
    return _keysTyped != []

def next_key_typed():
    """
    Remove the first key from the queue of keys that the the user typed,
    and return that key.
    """
    global _keysTyped
    return _keysTyped.pop()

#-----------------------------------------------------------------------
# Initialize the x scale and the y scale.
setXscale()
setYscale()
#-----------------------------------------------------------------------


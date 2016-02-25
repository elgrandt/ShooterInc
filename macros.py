__author__ = 'dylan'

import pygame
from random import randrange as RR
from math import *

def KEY(*arg): #Key detection
    for x in arg:
        if not pygame.key.get_pressed()[x]:
            return False
    return True

def MPOS(): ### Mouse position
    return pygame.mouse.get_pos()

def CLICK():
    return pygame.mouse.get_pressed()[0]

def RD(x):
    return radians(x)

def RS(max):
    return str(RR(max))
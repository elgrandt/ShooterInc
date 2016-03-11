__author__ = 'dylan'

import OGL
import pygame
import base
from config import *


def main():
    pygame.init()
    app = base.Base( SCREEN_WIDTH , SCREEN_HEIGHT , WINDOW_CAPTION )

    while app.on:
        app.refresh()


if __name__ == "__main__":
    main()



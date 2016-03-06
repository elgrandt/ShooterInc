__author__ = 'dylan'

from random import randrange as RR

### We'll use random sizes for deveolopment proposes
SCREEN_WIDTH = 800# RR(800 , 1024)
SCREEN_HEIGHT = 600# RR(600,800)

WINDOW_CAPTION = "Shooter test 0.1"

SmithAndWesson = {
    "Standby Pos": [.5, -1.1, -3],
    "Pointing Pos": [0, -.6, -3],
    "Transition to pointing time": 5.0,
    "Shoot animation time": 3,
    "Standby rotation Y": 35,
    "Standby rotation Z": -10
}
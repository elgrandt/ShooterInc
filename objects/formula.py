from math import *

def Point( ax , ay , d=1):
	ax = radians(ax)
	ay = radians(ay)
	z = d * cos(ax) * sin(ay)
	x = d * sin(ax) * sin(ay)
	y = d * cos(ay)

	return [x,y,z]


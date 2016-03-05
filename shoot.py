import pygame


### In this file thorically there will be the math to calculate if a shoot hits some cube or sphere.

### First we'll try to analise 2d collsions

class Point:
	def __init__(self,x,y,z):
		self.x = x
		self.y = y
		self.z = z

def GetRange(s1,s2,e1,e2):
	start = max(s1,s2)
	end = min(e1,e2)
	if start > end:
		return False
	else:
		return [start,end]

def Collide(init , direction , start_prism , end_prism):
	
	### get increases
	dx = direction.x - init.x
	dy = direction.y - init.y
	dz = direction.z - init.z

	### T * dx = start_prism.x -> T = start_prism.x / dx
	### T * dx = end_prism.x -> T = end_prism.x / dy

	txs = float(start_prism.x) / float(dx) #target x start
	txe = float(end_prism.x) / float(dx) #start x end

	tys = float(start_prism.y) / float(dy)
	tye = float(end_prism.y) / float(dy)

	tzs = float(start_prism.z) / float(dz)
	tze = float(end_prism.z) / float(dz)


	range_1 = GetRange(txs,tys,txe,tye)
	if range_1 == False:
		return False

	range_2 = GetRange(range_1[0],tzs,range_1[1],tze)

	if range_2 == False:
		return False
	if range_2[1] < 0:
		return False #the collision is on the back. Not valid	
	return True
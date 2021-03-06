import pygame


### In this file thorically there will be the math to calculate if a shoot hits some cube or sphere.

### First we'll try to analise 2d collsions

class Point:
	def __init__(self,x,y,z):
		self.x = x
		self.y = y
		self.z = z

def GetRange(s1,s2,e1,e2):
	if s2 > e1:
		return False
	if s1 > e2:
		return False

	start = max(s1,s2)
	end = min(e1,e2)
	
	if start > end:
		return False
	else:
		return [start,end]

def EasyCollide(init , direction , start_prism ,end_prism):
	return Collide(Point(init[0],init[1],init[2]) , Point(direction[0],direction[1],direction[2]) ,Point(start_prism[0],start_prism[1],start_prism[2]),Point(end_prism[0],end_prism[1],end_prism[2]))

def Collide(init , direction , start_prism , end_prism):
	###  TEST: [0, 0, 0] (-0.4363267749186886, 0, -49.998096153208564) (-1.5, -4.0, -21.0) (1.5, 4.0, -19.0)
	#print init.x , init.y , init.z , direction.x , direction.y , direction.z
	### get increases
	dx = direction.x - init.x
	dy = direction.y - init.y
	dz = direction.z - init.z

	#print dx , dy , dz
	### ix + T * dx = start_prism.x -> T = (start_prism.x-ix) / dx
	### ix + T * dx = end_prism.x -> T = (end_prism.x-ix) / dx

	if dx == 0:
		dx += 0.0000000000001
	if dy == 0:
		dy += 0.0000000000001
	if dz == 0:
		dz += 0.0000000000001
	#print dx,dy,dz
	txs = float(start_prism.x + init.x) / float(dx) #target x start
	txe = float(end_prism.x + init.x) / float(dx) #start x end

	tys = float(start_prism.y - init.y) / float(dy)
	tye = float(end_prism.y - init.y) / float(dy)

	tzs = float(start_prism.z - init.z) / float(dz)
	tze = float(end_prism.z - init.z) / float(dz)

	a = min(txs,txe)
	b = max(txs,txe)
	txs = a 
	txe = b

	a = min(tys,tye)
	b = max(tys,tye)
	tys = a
	tye = b

	a = min(tzs,tze)
	b = max(tzs,tze)
	tzs = a
	tze = b

	#print "[",txs , txe,"] [" , tys , tye ,"] [" , tzs , tze , "]"
	range_1 = GetRange(txs,tys,txe,tye)
	if range_1 == False:
		return False
	range_2 = GetRange(range_1[0],tzs,range_1[1],tze)
	#print range_2
	if range_2 == False:
		return False
	#f range_2[1] < 0:
		#return False #the collision is on the back. Not valid
	return range_2

def main():
	data = EasyCollide([0, 0, 0],(-0.4363267749186886, 0, -49.998096153208564),(-1.5, -4.0, -21.0),(1.5, 4.0, -19.0))
	#print data
if __name__ == "__main__":
	main()
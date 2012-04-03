from Weapon import *
from Blast import Blast

class Blaster(Weapon):
	'''
	A blaster class
	'''
	def __init__(self, tank):

		maxVel = 100  #Condition ??
		posDelta = Vec3(0,0,0) #Incorrect currently
		barrelLength = 2 # Incorrect currently

		print (tank.getPos() + posDelta)

		Weapon.__init__(self, tank, tank.getPos() + posDelta, barrelLength, maxVel)

		

	def fire(self, amt = 1):
		'''
		Fires a blaster bullet
		'''
		x = Blast(self, amt * self.maxVel)
		return x

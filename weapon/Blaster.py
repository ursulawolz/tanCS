import sys
sys.path.append("..")
from Weapon import *
from projectile.Blast import Blast

class Blaster(Weapon):
	'''
	A blaster class
	'''
	def __init__(self, tank):

		maxVel = 100  #Condition ??
		posDelta = Vec3(0,0,1) #Incorrect currently
		barrelLength = 2 # Incorrect currently

		Weapon.__init__(self, posDelta, barrelLength, maxVel)

		

	def fire(self, amt = 1):
		'''
		Fires a blaster bullet
		'''
		x = Blast(self, amt * self.maxVel)
		return x

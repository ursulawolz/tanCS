from Weapon import *
from Blast import Blast

class Blaster(Weapon):
	'''
	A blaster class
	'''
	def __init__(self, tank):
		Weapon.__init__(self, tank)

		self.maxVel = 100  #Condition ??

	def fire(self, amt = 1):
		'''
		Fires a blaster bullet
		'''
		x = Blast(self, amt * maxVel)
		return x

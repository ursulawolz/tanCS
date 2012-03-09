from Weapon import *


class Blaster(Weapon):
	'''
	A blaster class
	'''
	def __init__(self, tank):
		Weapon.__init__(tank)

	def fire(self, amt = 1):
		'''
		Fires a blaster bullet
		'''

		x = Blast(self, amt)

		print "fire the bullet here"

		return x

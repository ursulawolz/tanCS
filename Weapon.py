from TankWorld import *

class Weapon(object):

	def __init__(self):
		'''
		Base class for weapons
		'''
		self._direction = Vec3(0,0,0);
		
	def fire(self):
		'''
		fire using the current turret direction
		'''
	def setHp(self, heading, pitch):
		'''
		Aims the turret to the direction
		float heading
		float pitch
		'''
		self._direction = Vec3(heading, pitch, 0)
	def getDirection(self):
		'''
		Gets the direction that the turret
		Returns Vec3 of direction
		'''
		return self._direction;	

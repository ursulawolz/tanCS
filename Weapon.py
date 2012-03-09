from TankWorld import *

class Weapon(object):

	def __init__(self, tank):
		'''
		Base class for weapons
		'''
		self._direction = Vec3(0,0,0);
		self.tank = tank

	def fire(self, power = 1):
		'''
		fire using the current turret direction
		'''
		pass

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

	def getTank(self):
		return self.tank

	###Methods to add
	def setPitchVel(self, amt = 1):
		pass

	def setPitch(self,goal):
		pass

	def setHeadingVel(self,amt=1):
		pass

	def setHeading(self,goal):
		pass
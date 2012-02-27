from DynamicWorldObject import *

	
class Projectile(DynamicWorldObject):
	"""Child of DynamicWorldObject, fired by a Weapon, has a certain damage that it gives on impact
	"""

	def __init__(self, world, attach,  name = '', xCoord = 0, yCoord = 0, zCoord = 0, shape = BulletBoxShape(Vec3(.1, .1, .1)), heading = 0, pitch = 0, roll = 0, xVel = 0, yVel = 0, zVel = 0, mass = 0.1, damageGiven = 0):
		
		WorldObject.__init__(self, world, attach, name, xCoord, yCoord, zCoord, shape, heading, pitch, roll, xVel, yVel, zVel, mass)
		self._weapon = weapon
		self._damage = damageGiven

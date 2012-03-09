from DynamicWorldObject import *
from panda3d.bullet import BulletSphereShape

	
class Projectile(DynamicWorldObject):
	"""Child of DynamicWorldObject, fired by a Weapon, has a certain damage that it gives on impact
	"""

	def __init__(self, weapon,  name = '', shape = BulletSphereShape(.2), vel, mass = 0.1, damageGiven = 0):
		
		tank = weapon.getTank()

		direction = weapon.getDirection()
		world = tank.getTankWorld()
		attach = tank().getTankWorld().render

		pos = tank._nodePath.getPos() #Adjusted somehow for the Weapon pos?

		WorldObject.__init__(self, world, attach, name, pos[0], pos[1], pos[2], shape, direction[0], direction[1], direction[2], vel[0], vel[1], vel[2], mass)
		self._weapon = weapon
		self._damage = damageGiven



	def getDamage(self):
		return self._damage
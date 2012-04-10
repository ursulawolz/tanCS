import sys

sys.path.append("..")
from DynamicWorldObject import *
from panda3d.bullet import BulletSphereShape

	
class Projectile(DynamicWorldObject):
	"""Child of DynamicWorldObject, fired by a Weapon, has a certain damage that it gives on impact
	"""

	def __init__(self, weapon, pos, name = '', shape = BulletSphereShape(.2), vel = Vec3(0,0,0), mass = 0.1, damageGiven = 0):
		
		tank = weapon.getTank()

		direction = weapon.getDirection()
		world = tank.getTankWorld()
		attach = tank.getTankWorld().render


		DynamicWorldObject.__init__(self, world, attach, name, pos, shape, direction, vel, mass)
		self._weapon = weapon
		self._damage = damageGiven



	def getDamage(self):
		return self._damage

	def handleCollision(self, collide, taskName):
		self._collisionCounter += 1

		#Always in called twice in succession

		if (self._collisionCounter % 2 == 0):
			print "Projectile.handleCollision:(pos) ", self.getPos()

			self._tankWorld.taskMgr.remove(taskName)
			x = self._nodePath.node()

			self._tankWorld.removeRigidBody(x)
			self._nodePath.removeNode()
	

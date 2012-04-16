
import sys

sys.path.append("..")
from DynamicWorldObject import *
from panda3d.bullet import BulletSphereShape
import pdb
	
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
		self._nodePath.node().removeShape(shape)
		self.shape = shape
		self._tankWorld.doMethodLater(.2, self.startCollide, 'turn collide on')
		#self._nodePath.setFromCollideMask(BitMask32.allOff())
		#self._tankWorld.doMethodLater(1, self.startCollide, 'turn collide on') #attempt to make collisions turn on able. 
		#Something odd with collide masks
		
		self._nodePath.node().setCcdMotionThreshold(1e-7)
		self._nodePath.node().setCcdSweptSphereRadius(0.40)
	def getDamage(self):
		return self._damage
	
	def startCollide(self, task):
		if not self._nodePath.is_empty():
			self._nodePath.node().addShape(self.shape)
			#self._nodePath.setCollideMask(BitMask32.allOn())
		return task.done
	def deleteAfter(self, task):
		print "Projectile.deleteAfter: 1",
		if not self._nodePath.is_empty():
			x = self._nodePath.node()

			self._tankWorld.removeRigidBody(x)
			self._nodePath.removeNode()
			print '2'

	def handleCollision(self, collide, taskName):
		self._collisionCounter += 1

		#Always in called twice in succession

		#if (self._collisionCounter % 2 == 0):
		if not self._nodePath.is_empty():
			print "Projectile.handleCollision:(pos) ", self.getPos(), 'obj 1', collide.getNode0().getName(), 'obj 2', collide.getNode1().getName()

			self._tankWorld.taskMgr.remove(taskName)
			self._tankWorld.taskMgr.doMethodLater(.01, self.deleteAfter, 'deleteAfter')

		else:
			print "Projectile.handleCollision Failed to have _nodepath"
			self._tankWorld.taskMgr.remove(taskName)
		#pdb.set_trace()
		#del self
	def getName(self):
		return self._nodePath.getName()
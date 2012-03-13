from Projectile import *
import TaskList

class Blast(Projectile):

	'''Class Blast - Dynamic World Object fired by Blaster'''

	def __init__(self, weapon, power):
		

		#Parameters to be set
		speed = 10 * power
		damage = 1 #Blast should be weakest, base damage
		mass = .1 

		direction = weapon.getTank()._nodePath.getHpr()		
		shape = BulletSphereShape(.2)
		name = weapon.getTank()._nodePath.node().getName() + ' blast'

		pos = weapon.getTank().getPos()
		pos = Point3(pos[0], pos[1], pos[2] + 5)

		#print direction

		direction.normalize()
		vel = direction * speed #LVecBase3f
		vel = Vec3(vel[0], vel[1], vel[2])

		#print direction, vel

		Projectile.__init__(self, weapon, pos, name, shape, vel, mass, damage)
		self._collisionCounter = 0

	def handleCollision(self, collide, taskName):
		self._collisionCounter += 1

		#Always in called twice in succession

		if (self._collisionCounter % 2 == 0):
			#print self._tankWorld.taskMgr.getTasks()
			self._tankWorld.taskMgr.remove(taskName)
			x = self._nodePath.node()
			#print type(x)
			self._tankWorld.removeRigidBody(x)
			self._nodePath.removeNode()
import sys
sys.path.append("..")

from Projectile import *
import TaskList
from panda3d.core import Quat

class Blast(Projectile):

	'''Class Blast - Dynamic World Object fired by Blaster'''

	def __init__(self, weapon, speed):		

		#Parameters to be set
		
		damage = 1 #Blast should be weakest, base damage
		mass = .1 

		hpr = weapon.getHpr()
		h = (hpr[0] + 0) * math.pi / 180
		p = hpr[1] * math.pi / 180

		direction = Vec3(math.cos(h) * math.cos(p), math.sin(h) * math.cos(p), math.sin(p))

		shape = BulletSphereShape(.5)
		self.name = weapon.getTank()._nodePath.node().getName() + ' blast'

		pos = weapon.getAbsPos()
		pos = Point3(pos[0], pos[1], pos[2] + 1)

		vel = direction * speed #LVecBase3f
		vel = Vec3(vel[0], vel[1], vel[2])

		np  = loader.loadModel('media/bullet.x')
		np.setScale(Vec3(1.5,1.5,1.5))
		Projectile.__init__(self, weapon, pos, self.name, shape, vel, mass, damage)
		self._collisionCounter = 0

		np.reparentTo(self._nodePath)
	
		


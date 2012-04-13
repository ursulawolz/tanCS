from panda3d.bullet import BulletBoxShape
from StaticWorldObject import StaticWorldObject
from CubeObject import CubeObject
from panda3d.core import *
class Turret(CubeObject):
	def __init__(self, world, attach, position, orientation, name):
		shape = BulletBoxShape(Vec3(2,2,2))
		#StaticWorldObject.__init__(self, world, attach, name, position, shape, orientation)
		CubeObject.__init__(self, world, attach, name, position, scale = Vec3(2,2,2), texture='test.png' )
		self._tankWorld = world
		world.taskMgr.doMethodLater(3,self.fireTask, 'fire task')
		self.orientation = orientation

	def fireTask(self, task):

		self._weapon.aimAt(self._tankWorld.getUserTank().getPos(), False)
		self._weapon.fire(1)
		return task.again
	

	def setWeapon(self, weapon):
		self._weapon = weapon
		self._weapon._nodePath.setPos(self._weapon._nodePath, Vec3(1,1,1))
		self._weapon.setHp(self.orientation[0],self.orientation[1])
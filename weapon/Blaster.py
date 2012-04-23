import sys
sys.path.append("..")
from Weapon import *
from projectile.Blast import Blast

class Blaster(Weapon):
	'''
	A blaster class
	'''
	def __init__(self, tank):

		maxVel = 100  #Condition ??
		maxVel = 50  #Condition ??
		posDelta = Vec3(0,0,0) #Incorrect currently
		barrelLength = 2 # Incorrect currently
		self.canFire = True;
		self.reloadTimer = .5;

		#Graphics
		self._np1  = loader.loadModel('media/tanktop.x')
		self._np2  = loader.loadModel('media/turret.x')

		Weapon.__init__(self, tank, posDelta, barrelLength, maxVel)

		self._nodePath.setHpr(180,0,0)
		self._newNp = self._nodePath.attachNewNode('base')
		self._newNp.setPos(0,0,0)
		self._newNp.setHpr(0,0,0)
		#self._np1.reparentTo(self._nodePath)
		self._np1.reparentTo(self._newNp)
		self._np2.reparentTo(self._np1)

		self._np1.setPos(Vec3(0,1,0))
		self._np1.setHpr(Vec3(-90,0,0))
		self._np2.setPos(Vec3(0,0,0))

	def setCanFire(self, task):
		self.canFire = True

	def getBulletName(self):
		return self.tank.getNodePath().getName() + ' blast'

	def fire(self, amt = 1):
		'''
		Fires a blaster bullet
		'''
		if self.canFire == True:
			self.canFire = False
			x = Blast(self, amt * self.maxVel)
			self._tankWorld.taskMgr.doMethodLater(self.reloadTimer, self.setCanFire, 'can fire reload')
			return x
		

	def getHpr(self):
		return self._np2.getHpr(render) - Vec3(180, 0,0) #LINE THAT WILL PROBABLY BREAK	


	def setRelHp(self, heading, pitch):
		self._nodePath.setHpr(heading - 90, 0, 0)
		self._np2.setHpr(0,pitch,0)
		
	def getAbsPos(self):
		return self._nodePath.getPos(render) + Vec3(0,0,0)
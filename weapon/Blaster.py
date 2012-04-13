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
		posDelta = Vec3(0,0,1) #Incorrect currently
		barrelLength = 2 # Incorrect currently
		self.canFire = True;
		self.reloadTimer = .5;
		Weapon.__init__(self, tank, posDelta, barrelLength, maxVel)
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
		

import sys
sys.path.append("..")

from TankWorld import *

class Weapon(object):

	def __init__(self, tank, pos, length, vel):
		'''
		Base class for weapons
		'''

		name = tank._nodePath.node().getName() + " Blaster"
		self._nodePath = tank._nodePath.attachNewNode(PandaNode(name))
		self._nodePath.setPos(pos[0], pos[1], pos[2])
		self._nodePath.setHpr(-90,0,0)
	
		self.tank = tank
		self._tankWorld = self.tank._tankWorld
		self.barrel = length
		self.maxVel = vel

	def fire(self, power = 1):
		'''
		fire using the current turret direction
		'''
		pass

	def setRelHp(self, heading, pitch):
		'''
		Aims the turret to the direction, relative to tank's direction
		float heading
		float pitch
		'''
		self._nodePath.setHpr(heading, pitch, 0)

	def setHp(self, heading, pitch):
		'''Uses absolute hpr to aim the weapon in a direction
		'''
		tankHpr = self.tank.getHpr()

		deltaHpr = Vec3(heading, pitch, 0) - self.tank.getHpr()
		self.setRelHp(deltaHpr[0], deltaHpr[1])


	def getDirection(self):
		'''
		Gets the direction that the turret
		Returns Vec3 of direction
		'''
		return self._nodePath.getHpr(render) #LINE THAT WILL PROBABLY BREAK	

	def getRelPos(self):
		return self._nodePath.getPos()

	def getAbsPos(self):
		return self._nodePath.getPos(render)

	def getTank(self):
		return self.tank

	def setPitch(self,goal):
		self.setHp(self.direction[0], goal)

	def getHpr(self):
		return self._nodePath.getHpr(render) #LINE THAT WILL PROBABLY BREAK	

	def getHp(self):
		hpr = self.getHpr()
		hp = (hpr[0], hpr[1])
		return hp

	def setHeading(self,goal):
		self.setHp(goal, self.direction[1])

	def aimAt(self, pointAim, amt = 1, aimLow = True):
		pos = self.getAbsPos()

		point = Point3(pointAim[0] - pos[0], pointAim[1] - pos[1], pointAim[2] - pos[2]) #Blast collides at 1.1?

		angle1 = math.atan2(point[1], point[0])

		x = math.sqrt(point[0]**2 + point[1]**2)
		y = point[2]

		v = self.maxVel * amt
		tanks = self.tank
		gravity = self.tank._tankWorld.getPhysics().getGravity() #Vector
		g = abs(gravity[2])	
		print "Weapon.aimAt: ", v**4
		discriminant = v**4 - g * (g * x**2 + 2 * y * v**2)

		if discriminant < 0:
			print "Weapon.aimAt: ", discriminant
			return False
		if x == 0:
			return False
		
		if aimLow:
			angle2 = math.atan((v**2 - math.sqrt(discriminant))/(g * x))
		else:
			angle2 = math.atan((v**2 + math.sqrt(discriminant))/(g * x))

		angle1 = angle1 * 180 / math.pi
		angle2 = angle2 * 180 / math.pi

		self.setHp(angle1, angle2)

		return True


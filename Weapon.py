from TankWorld import *

class Weapon(object):

	def __init__(self, tank, pos, length, vel):
		'''
		Base class for weapons
		'''

		name = tank._nodePath.node().getName() + " Blaster"
		self._nodePath = tank._nodePath.attachNewNode(PandaNode(name))
		self._nodePath.setPos(pos[0], pos[1], pos[2])
		self._nodePath.setHpr(0,0,0)
		
		self.tank = tank

		self.barrel = length
		self.maxVel = vel

	def fire(self, power = 1):
		'''
		fire using the current turret direction
		'''
		pass

	def setHp(self, heading, pitch):
		'''
		Aims the turret to the direction
		float heading
		float pitch
		'''
		self._nodePath.setHpr(heading, pitch, 0)
		

	def getDirection(self):
		'''
		Gets the direction that the turret
		Returns Vec3 of direction
		'''
		return self._nodePath.getHpr()	

	def getRelPos(self):
		return self._nodePath.getPos()

	def getAbsPos(self):
		return self._nodePath.getPos() + self.tank._nodePath.getPos()

	def getTank(self):
		return self.tank

	def setPitch(self,goal):
		self.setHp(self.direction[0], goal)

	def setHeading(self,goal):
		self.setHp(goal, self.direction[1])

	def aimAt(self, pointAim, aimLow):
		pos = self.tank.getPos()

		point = Point3(pointAim[0] - pos[0], pointAim[1] - pos[1], pointAim[2] - pos[2])

		angle1 = math.atan2(point[0], point[1])

		x = math.sqrt(point[0]**2 + point[1]**2)
		y = point[2]
		v = self.maxVel
		tanks = self.tank
		gravity = self.tank._tankWorld.getPhysics().getGravity() #Vector
		g = gravity[2]	

		discriminant = v**4 - g * (g * x**2 + 2 * y * v**2)

		if discriminant < 0:
			return False

		if aimLow:
			angle2 = math.atan((v**2 - math.sqrt(discriminant))/(g * x))
		else:
			angle2 = math.atan((v**2 + math.sqrt(discriminant))/(g * x))

		self.setHp(angle1, angle2)

		return True


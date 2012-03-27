from TankWorld import *

class Weapon(object):

	def __init__(self, tank):
		'''
		Base class for weapons
		'''
		self._direction = Vec3(0,0,0);
		self.tank = tank

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
		self._direction = Vec3(heading, pitch, 0)


	def getDirection(self):
		'''
		Gets the direction that the turret
		Returns Vec3 of direction
		'''
		return self._direction;	

	def getTank(self):
		return self.tank

	def setPitch(self,goal):
		self.setHp(self.direction[0], goal)

	def setHeading(self,goal):
		self.setHp(goal, self.direction[1])

	def aimAt(self, pointAim):
		pos = self.tank.getPos()

		point = Point3(pointAim[0] - pos[0], pointAim[1] - pos[1], pointAim[2] - pos[2])

		angle1 = math.atan2(point[0], point[2])

		x = math.sqrt(point[0]**2 + point[1]**2)
		y = point[3]
		v = self._maxVel
		gravity = self.tank._bulletWorld.getGravity() #Vector
		g = gravity[2]	

		discriminant = v**4 - g * (g * x**2 + 2 * y * v**2)

		if discriminant < 0:
			return False

		angle2 = math.atan((v**2 - sqrt(discriminant))/(g * x))

		self.setHp(angle1, angle2)

		return True


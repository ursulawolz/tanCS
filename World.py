from panda3d.core import Vec3, Point3, BitMask32
from pandac.PandaModules import PandaNode
from direct.showbase.ShowBase import ShowBase
from panda3d.bullet import BulletRigidBodyNode, BulletBoxShape, BulletWorld, BulletCapsuleShape
import math

class TankWorld(ShowBase):

#	"""Main runner class. Runs user scripts and manages objects in the world"""

	def __init__(self, physics = BulletWorld()):
		ShowBase.__init__(self)
		self.__bullet = physics	

	def getPhysics(self):
		return self.__bullet

	#def record(index):	#Record state variables in some location
	




class WorldObject:
	"""Parent Class for all physical objects present in TankWorld. 
Variables: 	.__node > BulletRigidBodyNode for physics simulation
		.__nodePath > Panda NodePath for rendering. Includes some state variables.		
"""

	def __init__(self, world, attach, name = '', xCoord = 0, yCoord = 0, zCoord = 0, shape = BulletBoxShape(Vec3(.1, .1, .1)), heading = 0, pitch = 0, roll = 0, xVel = 0, yVel = 0, zVel = 0, mass = 0.1):
	#@param world: A BulletWorld for this to be simulated in
	#@param attach: a NodePath to attach this WorldObject to. By default send some ShowBase.render		

		self.nodePath = attach.attachNewNode(BulletRigidBodyNode(name)) 	#Bullet node for rendering and physics - this is what this class manipulates
		self.world = world
		self.nodePath.node().setMass(mass)		
		
		#The NodePath holds rendering state variables	
		self.nodePath.setPos(xCoord, yCoord, zCoord) 
 		self.nodePath.setHpr(heading, pitch, roll)		

		#Bullet's Node holds other physics-based state variables
		self.nodePath.node().setLinearVelocity(Vec3(xVel, yVel, zVel))
		self.nodePath.node().addShape(shape)
		world.attachRigidBody(self.nodePath.node())



	def setVel(self, xVel, yVel, zVel):
		self.nodePath.node().setLinearVelocity(Vec3(xVel, yVel, zVel))
		
	def getVel(self):
		return self.nodePath.node().getLinearVelocity()

	def getPos(self):
		return self.nodePath.getPos() 	

	
class Tank(WorldObject):

	def __init__(self, world, attach, name = '', xCoord = 0, yCoord = 0, zCoord = 0, heading = 0, pitch = 0, roll = 0):
		
		tankSide = 7
		shape = BulletBoxShape(Vec3(tankSide, tankSide, tankSide)) #Create the tank's shape here
		WorldObject.__init__(self, world, attach, name, xCoord, yCoord, zCoord, shape, heading, pitch, roll, 0, 0, 0, mass = 800.0) #Initial velocity must be 0
		
		self.nodePath.node().setFriction(.3) 	
		
		#Set up turret		
		self.TurretNP = self.nodePath.attachNewNode(PandaNode(name + "Turret"))
		self.TurretNP.setPos(0, 0, 0)
		self.TurretNP.setHpr(0, 1, 0)
		
		#Make collide mask (What collides with what?)
		self.nodePath.setCollideMask(0xFFFF0000)

	def setVel(self, xVel, yVel):
		velLimit = 20.0 #m/s, what should this be?
		currentVel = self.getVel()		
		maxForce = 5000 #N, gives 2.5m.s^2 accel
		pos = self.nodePath.getPos()
		if math.sqrt(xVel**2 + yVel**2) <= velLimit:
			diff = Vec3(xVel, yVel, 0) - currentVel
			print diff
			normDiff = diff/math.sqrt(diff[0]**2 + diff[1]**2)
			
			self.nodePath.node().applyForce(Vec3(maxForce*normDiff[0], maxForce*normDiff[1], 0), pos)
		else:
			raise ValueError("Magnitude of velocity must be below " + str(velLimit))

	
	def attachNewNode(self, otherNode):
		return self.nodePath.attachNewNode(otherNode)

	def setTurretAngle(pitch):
		self.TurretNP.setHpr(0, pitch, 0)

	def stop():
		setVel(0, 0)




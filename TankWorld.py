#General Open Questions:
"""
How do we store game data in an accessible way? Probably through the TankWorld
How do we move the Tank? Set Velocity directly, apply accel/braking forces, what is friction...

"""

from panda3d.core import Vec3, Point3, BitMask32
from pandac.PandaModules import PandaNode
from direct.showbase.ShowBase import ShowBase
from panda3d.bullet import BulletRigidBodyNode, BulletBoxShape, BulletWorld, BulletCapsuleShape
import math

class TankWorld(ShowBase):

	"""Main runner class. Runs user scripts and manages objects in the world"""

	def __init__(self, physics = BulletWorld()):
		ShowBase.__init__(self)
		self.__bullet = physics	

	def getPhysics(self):
		return self.__bullet




class WorldObject:
	"""Parent Class for all physical objects present in TankWorld. 
Variables: 	.node > BulletRigidBodyNode for physics simulation
		.nodePath > Panda NodePath for rendering. Includes some state variables.		
"""

	def __init__(self, world, attach, name = '', xCoord = 0, yCoord = 0, zCoord = 0, shape = BulletBoxShape(Vec3(.1, .1, .1)), heading = 0, pitch = 0, roll = 0, xVel = 0, yVel = 0, zVel = 0, mass = 0.1):
	#@param world: A BulletWorld for this to be simulated in
	#@param attach: a NodePath to attach this WorldObject to. By default send some ShowBase.render		

		self.nodePath = attach.attachNewNode(BulletRigidBodyNode(name)) 	#Bullet node for rendering and physics - this is what this class manipulates
		self.world = world
		self.nodePath.node().setMass(mass)					#Only static objects should have 0 mass
		
		#The NodePath holds rendering state variables	
		self.nodePath.setPos(xCoord, yCoord, zCoord) 
 		self.nodePath.setHpr(heading, pitch, roll)		

		#Bullet's Node holds other physics-based state variables
		self.nodePath.node().setLinearVelocity(Vec3(xVel, yVel, zVel))
		self.nodePath.node().addShape(shape)
		self.world.attachRigidBody(self.nodePath.node())


	def getVel(self):
		return self.nodePath.node().getLinearVelocity()

	def getPos(self):
		return self.nodePath.getPos() 	

	
class Tank(WorldObject):

"""Child of WorldObject, with all of the things that makes a Tank a tank.

Includes a Turret and whatever Bullets it fires and are still alive. (Bullets not written yet.)

"""
	def __init__(self, world, attach, name = '', xCoord = 0, yCoord = 0, zCoord = 0, heading = 0, pitch = 0, roll = 0, turretPitch = 0):
		
		#Constant Relevant Instatiation Parameters
		tankSideLength = 7
		friction = .3
		turretRelPos = (0, 0, 0) #Relative to tank

		shape = BulletBoxShape(Vec3(tankSideLength, tankSideLength, tankSideLength)) #Create the tank's shape here
		WorldObject.__init__(self, world, attach, name, xCoord, yCoord, zCoord, shape, heading, pitch, roll, 0, 0, 0, mass = 800.0) #Initial velocity must be 0
		
		self.nodePath.node().setFriction(friction)		
		
		#Set up turret nodepath - nodepaths are how objects are managed in Panda3d
		self.TurretNP = self.nodePath.attachNewNode(PandaNode(name + "Turret"))
		self.TurretNP.setPos(turretRelPos[0], turretRelPos[1], turretRelPos[2])
		self.TurretNP.setHpr(0, turretPitch, 0) #Turret does not have heading or roll relative to Tank
		
		#Make collide mask (What collides with what)
		self.nodePath.setCollideMask(0xFFFF0000)

	def setTurretAngle(pitch):
		
		#Note: currently instantaneous - we need to figure out how to move continuously (or not, Turrets don't collide...)
		self.TurretNP.setHpr(0, pitch, 0)



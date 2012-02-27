from panda3d.core import Vec3, Point3, BitMask32
from pandac.PandaModules import PandaNode
from direct.showbase.ShowBase import ShowBase
from panda3d.bullet import BulletRigidBodyNode, BulletBoxShape, BulletWorld, BulletCapsuleShape
from WorldObject import WorldObject
import math
from DynamicWorldObject import *
class Tank(DynamicWorldObject):

	'''Child of WorldObject, with all of the things that makes a Tank a tank.

	Includes a Turret and whatever Bullets it fires and are still alive. (Bullets not written yet.)

	'''
	def __init__(self, world, attach, name = '', xCoord = 0, yCoord = 0, zCoord = 0, heading = 0, pitch = 0, roll = 0, turretPitch = 0):
		
		#Constant Relevant Instatiation Parameters
		tankSideLength = 7
		friction = .3
		turretRelPos = (0, 0, 0) #Relative to tank
		
		shape = BulletBoxShape(Vec3(tankSideLength, tankSideLength, tankSideLength)) #Create the tank's shape here
		
		
		WorldObject.__init__(self, world, attach, name, xCoord, yCoord, zCoord, shape, heading, pitch, roll, 0, 0, 0, mass = 800.0) #Initial velocity must be 0
		
		self.nodePath.node().setFriction(friction)		
		
		#Set up turret nodepath - nodepaths are how objects are managed in Panda3d
		self._turret = self.nodePath.attachNewNode(PandaNode(name + "Turret"))
		
		self.setTurretHp(0,turretPitch) #set up the initial conditions
		#Make collide mask (What collides with what)
		self.nodePath.setCollideMask(0xFFFF0000)

	
	def setTurretHp(heading, pitch):
		'''
		float heading
		float pitch
		'''
		
		#Note: currently instantaneous - we need to figure out how to move continuously (or not, Turrets don't collide...)
		self._turret.setHp(heading,pitch)


from panda3d.core import Vec3, Point3, BitMask32
from pandac.PandaModules import PandaNode
from direct.showbase.ShowBase import ShowBase
from panda3d.bullet import BulletRigidBodyNode, BulletBoxShape, BulletWorld, BulletCapsuleShape
from WorldObject import WorldObject
import math
	
class Tank(WorldObject):

"""Child of WorldObject, with all of the things that makes a Tank a tank.

Includes a weapon that can fire projectiles

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



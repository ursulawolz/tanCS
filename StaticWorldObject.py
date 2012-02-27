from panda3d.core import Vec3, Point3, BitMask32
from pandac.PandaModules import PandaNode
from direct.showbase.ShowBase import ShowBase
from panda3d.bullet import BulletRigidBodyNode, BulletBoxShape, BulletWorld, BulletCapsuleShape
import math

class StaticWorldObject(WorldObject):
	"""Child Class for physical objects that do not move in TankWorld. These objects include walls.
Variables: 	.node > BulletRigidBodyNode for physics simulation
		.nodePath > Panda NodePath for rendering. Includes some state variables.		
"""

	def __init__(self, world, attach, name = '', xCoord = 0, yCoord = 0, zCoord = 0, shape = BulletBoxShape(Vec3(.1, .1, .1)), heading = 0, pitch = 0, roll = 0):

		WorldObject.__init__(self, world, attach, name, xCoord, yCoord, zCoord, shape, heading, pitch, roll, 0, 0, 0, mass = 0) ##Mass must be zero.

	def getVel(self):
		return Vec3(0,0,0)


from WorldObject import *

class StaticWorldObject(WorldObject):
	"""Child Class for physical objects that do not move in TankWorld. These objects include walls.
Variables: 	.node > BulletRigidBodyNode for physics simulation
		.nodePath > Panda NodePath for rendering. Includes some state variables.		
"""

	def __init__(self, world, attach, name = '', position = Vec3(0,0,0), shape = BulletBoxShape(Vec3(.1, .1, .1)), orientation = Vec3(0,0,0)):

		WorldObject.__init__(self, world, attach, name, position, shape, orientation, Vec3(0,0,0), mass = 0) ##Mass must be zero.
		
	def getVel(self):
		return Vec3(0,0,0)


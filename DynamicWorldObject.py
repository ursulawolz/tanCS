from WorldObject import *

class DyanmicWorldObject(WorldObject):

	"""Class DynamicWorldObject: This is a child of WorldObject that can move. This object must have a positive mass, and can be moved by BulletWorld.

	"""
	def __init__(self, world, attach, name = '', xCoord = 0, yCoord = 0, zCoord = 0, shape = BulletBoxShape(Vec3(.1, .1, .1)), heading = 0, pitch = 0, roll = 0, xVel = 0, yVel = 0, zVel = 0, mass = 0.1):
		
		if (mass <=0):
			raise ValueError("Mass of DynamicWorldObject must be greater than 0.")
	
		WorldObject.__init__(self, world, attach, name, xCoord, yCoord, zCoord, shape, heading, pitch, roll, xVel, yVel, zVel, mass)

from WorldObject import *

class DynamicWorldObject(WorldObject):

	"""Class DynamicWorldObject: This is a child of WorldObject that can move. This object must have a positive mass, and can be moved by BulletWorld.

	"""
	def __init__(self, world, attach, name = '', position = Point3(0,0,0), shape = BulletBoxShape(Vec3(.1, .1, .1)), orientation = Vec3(0,0,0), 
		velocity = Vec3(0,0,0), mass = 0.1):
		
		if (mass <=0):
			raise ValueError("Mass of DynamicWorldObject must be greater than 0.")
		WorldObject.__init__(self, world, attach, name, position, shape, orientation, velocity, mass)
		TaskList.setCollision(self, self._tankWorld)


	def handleCollision(self, contact, task):
		'''Must remove task, as specified in TaskList.setCollision'''
		#print contact.getNode0()
		#self._tankWorld.taskMgr.remove(self._nodePath.node().getName() + 'collide')


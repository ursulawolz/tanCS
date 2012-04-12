import sys
sys.path.append("..")

from State import State
from panda3d.core import *

import TaskList

from CubeObject import CubeObject


class CollisionState(State, CubeObject):
	def __init__(self, tankWorld, tracking_name, position=Vec3(0,0,0), name='collisionShape'):
		'''
			TrackingObject is the world object that we are tracking
			Position trigger has a representation needs to be added.

		'''


		self.position = position
		self.tracking_name = tracking_name
		print "PositionTrigger.__init__: Trigger created"

		

		State.__init__(self,tankWorld)
		CubeObject.__init__(self, tankWorld, tankWorld.render, name = name, position = position, orientation = Vec3(0,0,0), scale = VBase3(2,2,2), texture='trigger.png' )
		#must be after the cubeobject instantiator
		TaskList.setCollision(self, tankWorld)


	def checkConditions(self, task):
		'''try:
			pos2 = self.tracking_object.getPos()
			#print self.position
			#print "Checking?"
			#print (self.position-pos2).length()
			if (self.position-pos2).length() < self.radius:
				self.win()
				pass
		except:
			print "error in positiontrigger.checkConditions" , sys.exc_info()[0]
		'''
		return task.cont


	

	def handleCollision(self, collide, taskName):

		print 'CollisionState self name:::',self.tracking_name,'other:::',collide.getNode0().getName(),'final:::',collide.getNode1().getName()
		
		if collide.getNode0().getName() == self.tracking_name or collide.getNode1().getName()== self.tracking_name:
			self.triggered=True
			#pass
		#self.tankWorld.taskMgr.remove(taskName)
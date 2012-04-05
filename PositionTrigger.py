from Trigger import Trigger
from panda3d.core import *
import sys

class PositionTrigger(Trigger):
	def __init__(self, tankWorld, tracking_object, radius, position=Vec3(0,0,0) ):
		'''
			TrackingObject is the world object that we are tracking
			Position trigger has a representation needs to be added.
			
		'''

		self.position = position
		self.radius = radius
		self.tracking_object = tracking_object
		print self.tracking_object
		print "PositionTrigger.__init__: Trigger created"

		super(PositionTrigger,self).__init__(tankWorld)

	def checkConditions(self, task):
		try:
			pos2 = self.tracking_object.getPos()
			#print self.position
			#print "Checking?"
			#print (self.position-pos2).length()
			if (self.position-pos2).length() < self.radius:
				self.win()
				pass
		except:
			print "error in positiontrigger.checkConditions" , sys.exc_info()[0]
		return task.cont


	

import sys
sys.path.append("..")

from State import State
from panda3d.core import *

import TaskList

from CubeObject import CubeObject


class PadState(State):
	def __init__(self, tankWorld, tracking_name, position=Vec3(0,0,0), name='PadState', size=Vec3(2,2,2)):
		'''
			TrackingObject is the world object that we are tracking
			Position trigger has a representation needs to be added.

		'''
		State.__init__(self,tankWorld)

		#grab the object with this name
		for child in tankWorld.render.getChildren():
			if child.getName() == tracking_name:
				self.tracking_object = child

		self.position = position+Vec3(0,0,.01)
		self.tracking_name = tracking_name
		self.size = size
		#print "PositionTrigger.__init__: Trigger created"
		assert(self.tracking_object, "No tracking object")

		cm=CardMaker('')
		cm.setFrame(0,1,0,1)
		self.floor = render.attachNewNode(PandaNode("padCollision"))
		self.floor.setPos(self.position)

		tex = loader.loadTexture('media/'+'trigger.png')
		tex.setMagfilter(Texture.FTNearest)
		tex.setMinfilter(Texture.FTNearest)
		for y in range(int(size.getX())):
			for x in range(int(size.getY())):
				nn = self.floor.attachNewNode(cm.generate())
				nn.setP(-90)
				nn.setPos((x), (y), 0)
		self.floor.setTexture(tex)
		#self.floor.flattenStrong()


	def setTexture(self, texturename):

		tex = loader.loadTexture('media/'+texturename)
		tex.setMagfilter(Texture.FTNearest)
		tex.setMinfilter(Texture.FTNearest)
		self.floor.setTexture(tex)
		#self.floor.flattenStrong()

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
		#simple 2d collision, currently using shpere
		#print (self.position+self.size/2-self.tracking_object.getPos()).length(),
		#print ((self.size.getX()/2)**2+(self.size.getY()/2)**2)**.5*4
		if (self.position+self.size/2-self.tracking_object.getPos()).length() < ((self.size.getX()/2)**2+(self.size.getY()/2)**2)**.5-.5:
			#print "PAdState triggered"
			self.triggered=True
			self.setTexture('activated.png')

		return task.done


	
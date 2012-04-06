from panda3d.core import *

from panda3d.bullet import BulletRigidBodyNode, BulletWorld

from TankWorld import TankWorld
from MeshWorldObject import MeshWorldObject
from Tank import Tank
from DynamicWorldObject import DynamicWorldObject
import TaskList

from runFile import runFile

import xmlParse
import sys, os
from direct.interval.IntervalGlobal import *
from direct.showbase.InputStateGlobal import inputState
from direct.task import Task


class testLevel():
	def __init__(self,filename):
		self.filename = filename
		self.t = xmlParse.createLevel(self.filename)
		self.oldtime = os.stat(self.filename).st_mtime
		taskMgr.add(self.fileHasUpdate,"fileUpdate") 

	def fileHasUpdate(self,task):
		#try:
		if self.oldtime != os.stat(self.filename).st_mtime:

			for child in self.t.render.getChildren():
				name = child.getName()
				print child
				if child.node().getClassType() == BulletRigidBodyNode.getClassType():

					self.t.getPhysics().removeRigidBody(child.node())
					print "rigid body removed"

				if name != 'camera' and name != 'Spot' and name != 'Debug' and name != 'Ambient':
					child.detachNode()
				pass
			xmlParse.createLevel(self.filename, self.t)
			self.oldtime = os.stat(self.filename).st_mtime
		#except:
		#	print "error in testLevel.upate"
		return task.cont



t = testLevel(sys.argv[1])
run()





#shape = BulletPlaneShape(Vec3(0, 0, 1), 1)

#node = BulletRigidBodyNode('Ground')
#node.setFriction(1)
#node.addShape(shape)

#np = render.attachNewNode(node)
#np.setPos(0,0,-4)
#t.getPhysics().attachRigidBody(node)

#print "asdfasdfasdf"
#np.setPos(0, 0, 0)


#runFile('user.py',t)

#TaskList.setCollision(ta, t)


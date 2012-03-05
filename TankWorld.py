#General Open Questions:
"""
How do we store game data in an accessible way? Probably through the TankWorld
How do we move the Tank? Set Velocity directly, apply accel/braking forces, what is friction...

"""
import sys, os
from panda3d.core import Vec3, Point3, BitMask32, Spotlight, AmbientLight
from pandac.PandaModules import PandaNode
from direct.showbase.ShowBase import ShowBase
from panda3d.bullet import BulletRigidBodyNode, BulletBoxShape, BulletWorld, BulletCapsuleShape, BulletDebugNode
from direct.interval.IntervalGlobal import *
from direct.showbase.InputStateGlobal import inputState
from direct.task import Task
import math

from Tank import Tank
	
class TankWorld(ShowBase):

	"""Main runner class. Runs user scripts and manages objects in the world"""

	def __init__(self, physics = BulletWorld()):
		ShowBase.__init__(self)
		self.__bulletWorld = physics	
				
		self.__setupLighting()
		
		base.cam.setPos(30,30,30);
		base.cam.lookAt(0,0,0);
		
		self.__setupUserInput() #set up user input
		base.disableMouse() #disable the mouse

		taskMgr.add(self.__update,"update") #This creates a task named update and runs every frame
		
		self.drawDebugNode()
					
	def __setupLighting(self):
		'''
		Sets up lighting
		'''
		#set up spotlighti
		self.light= render.attachNewNode(Spotlight("Spot"));
		self.light.setPos(-15,10,15);
		self.light.lookAt(0,0,0);
		self.light.node().setScene(render)
		self.light.node().setShadowCaster(True)
		
		self.light.node().getLens().setFov(40)
		render.setLight(self.light)
		
		self.alight = render.attachNewNode(AmbientLight("Ambient"))
		render.setLight(self.alight);
		
		render.setShaderAuto() #shader generation on
		
	def __setupUserInput(self):
		'''
		Sets up user input
		'''
		#print "setupinput"
		self.accept('escape-up',sys.exit)
		self.mf = inputState.watch('foward','w','w-up')#note self.mf has to be released	
		self.bw = inputState.watch('backward','s','s-up')
		self.left = inputState.watch('left','a','a-up')
		self.right = inputState.watch('right','d','d-up')
			
	def __update(self, task):
		'''
		Task task: Time since last frame	
		'''
		dt = globalClock.getDt();
		moveAmount = 50*dt;
		changeY =  (inputState.isSet('foward')-inputState.isSet('backward'))*moveAmount
		changeX = (inputState.isSet('right')-inputState.isSet('left'))*moveAmount;
		self.__bulletWorld.doPhysics(dt)
		base.cam.setPos(base.cam,changeX,changeY,0);	
		hpr = base.cam.getHpr();
		if base.mouseWatcherNode.hasMouse():	
			hpr.x = -100*base.mouseWatcherNode.getMouseX()
			hpr.y = 100*base.mouseWatcherNode.getMouseY();

		base.cam.setHpr(hpr);	

		return Task.cont
	
	def getPhysics(self):
		return self.__bulletWorld

	def attachRigidBody(self, node):
		self.__bulletWorld.attachRigidBody(node)


	
	def drawDebugNode(self):
		debugNode = BulletDebugNode('Debug')
		debugNode.showWireframe(True)
		debugNode.showConstraints(True)
		debugNode.showBoundingBoxes(False)
		debugNode.showNormals(False)
		debugNP = render.attachNewNode(debugNode)
		debugNP.show()
		print "debug node activated" 
		
		self.__bulletWorld.setDebugNode(debugNode)

	def makeTeapot(self):
		'''
		Test function to test to see of camera movement is working
		'''

		self.tank=loader.loadModel('teapot')
		self.tank.reparentTo(render)
		
		self.base = loader.loadModel('box')
		self.base.reparentTo(render)
		self.base.setScale(100,100,.2)
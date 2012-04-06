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
import pdb

from Tank import Tank
	
class TankWorld(ShowBase):

	"""Main runner class. Runs user scripts and manages objects in the world"""

	def __init__(self, physics = BulletWorld()):
		ShowBase.__init__(self)

		self.__bulletWorld = physics	
				
		self.__setupLighting()
		base.cam.setPos(-10,-10,30);
		base.cam.lookAt(10,10,0);
		self.drawDebugNode()
		self.__setupUserInput() #set up user input
		base.disableMouse() #disable the mouse

		#This creates a task named update and runs every frame
		taskMgr.add(self.stepTasks,'SOME NAME')
		self.add(self.__update,"update")
		self._deltaTimeAccumulator = 0;

		self.tanks = []
		self.isDead = False

	def __del__(self):
		#self.shutdown()
		#del self
		pass
	
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
		
		self.taskList =[]

	def __setupUserInput(self):
		'''
		Sets up user input
		'''
		#print "setupinput"
		self.doMouseStuff = False
		def toggleMouse():
			self.doMouseStuff = not self.doMouseStuff 
		
		self.accept('m', toggleMouse)
		self.accept('escape-up',self.close)
		self.mf = inputState.watch('foward','w','w-up')#note self.mf has to be released	
		self.bw = inputState.watch('backward','s','s-up')
		self.left = inputState.watch('left','a','a-up')
		self.right = inputState.watch('right','d','d-up')

	def close(self):
		self.taskMgr.removeTasksMatching("*")
		self.isDead = True
		self.shutdown()
		
		#pdb.set_trace()
		self.exitfunc()
		self.destroy()
		#sys.exit()

	def __update(self, task):
		'''
		Task task: Time since last frame	
		'''
		try:
			dt = globalClock.getDt();
			if dt > .1:
				return Task.cont
			moveAmount = 50*dt;
			changeY =  (inputState.isSet('foward')-inputState.isSet('backward'))*moveAmount
			changeX = (inputState.isSet('right')-inputState.isSet('left'))*moveAmount;

			stepSize = 1.0 / 60.0

			#set up a fixed time constant step for more accurate physics.
			#We need to test more with the vehicle class to see if it plays nice. 
			self._deltaTimeAccumulator += globalClock.getDt()
			while self._deltaTimeAccumulator> stepSize :
				self.__bulletWorld.doPhysics(stepSize)
				self._deltaTimeAccumulator -= stepSize;
			
			base.cam.setPos(base.cam,changeX,changeY,0);	
			hpr = base.cam.getHpr();
			if base.mouseWatcherNode.hasMouse() and self.doMouseStuff:	
				hpr.x = -100*base.mouseWatcherNode.getMouseX()
				hpr.y = 100*base.mouseWatcherNode.getMouseY();

			base.cam.setHpr(hpr);	
		except:
			print "error tankworld.__update"

		return task.cont
	def getUserTank(self):
		'''
			Gets the user tank. Currently not implemented for multiple tanks.
		'''
		return self.tanks[0]
	def registerTank(self, tank):
		self.tanks.append(tank)

	def getPhysics(self):
		return self.__bulletWorld

	def attachRigidBody(self, node):
		self.__bulletWorld.attachRigidBody(node)

	def removeRigidBody(self, node):
		self.__bulletWorld.removeRigidBody(node)

	
	def drawDebugNode(self):
		debugNode = BulletDebugNode('Debug')
		debugNode.showWireframe(True)
		debugNode.showConstraints(True)
		debugNode.showBoundingBoxes(False)
		debugNode.showNormals(False)
		self.debugNP = render.attachNewNode(debugNode)

		print "TankWorld.drawDebugNode: debug node activated" 
		self.accept('9', self.debugNP.show)
		self.accept('8', self.debugNP.hide)

		self.__bulletWorld.setDebugNode(debugNode)

	#Victory conditions

	def victory(self):
		'''
			Called when a victory condition has been met
		'''
		print "YOU HAVE WON THE GAME"
		#pdb.set_trace()
		self.close()

	def lose(self):
		'''
			Called when a loss condition has been met
		'''
		print "YOU HAVE LOST THE GAME"
		sys.exit()



	#functions for our taskManager
	def add(self,functionptr,name='asd',upondeath=None):
		self.taskList.append([functionptr, name, upondeath])

	def stepTasks(self, task):
		try:
			removeTasks = []
			count =0
			#print self.taskList[0]()
			for taskz in self.taskList:
				ret = taskz[0](task) #call the death function
				if(ret == task.done or ret == None):
					removeTasks.append(count)
					pass
				count += 1
			removeTasks.reverse()
			for t in removeTasks:
				self.taskList[t][2]() #call the upon death function
				self.taskList.pop(t)
		except:
			print "error in tankworld.stepTasks",  sys.exc_info()[0],sys.exc_info()[1]
		return task.cont


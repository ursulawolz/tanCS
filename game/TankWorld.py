#General Open Questions:
"""
How do we store game data in an accessible way? Probably through the TankWorld
How do we move the Tank? Set Velocity directly, apply accel/braking forces, what is friction...

"""
import sys, os
from panda3d.core import Vec3, Point3, BitMask32, Spotlight, AmbientLight, VBase4
from pandac.PandaModules import PandaNode
from direct.showbase.ShowBase import ShowBase
from panda3d.bullet import BulletRigidBodyNode, BulletBoxShape, BulletWorld, BulletCapsuleShape, BulletDebugNode
from direct.interval.IntervalGlobal import *
from direct.showbase.InputStateGlobal import inputState
from direct.task import Task
import math
from array import array
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
		self.taskMgr.add(self.__update,"bullet-update")
		self.realTime = True
		self._deltaTimeAccumulator = 0;

		self.tanks = []
		self.isDead = False
		self.levelData = {}
		self.victoryState = 0 # 1 = win, 2 = lose


		#This is all new, to run in non-realtime
		globalClock.setDt(1.0/60.0)		
		self.numFrames = 0
		self.dynamics = [] 
		self.gameData = [] #Will be huge eventually
		self.debugTime = 0 #Prints every integer second
		self.laterTasks = []
		self._afterStarts = []
		self.isOver = False #Tells Tank to stop
		self.displaySpeed = 1

	def __display(self):
		'''Must be called after preCalc. Sets the stage for the display of the performance'''
		self.taskMgr.add(self.igLoop, 'igLoop')
		self._displayTime = 0
		self._lastTime = 0
		self.frameTime = 0
		#print "TankWorld.__dusplay: ", self.taskMgr.getAllTasks()
		self.taskMgr.removeTasksMatching('*tank*')
		self.taskMgr.removeTasksMatching('*NAME*')
		self.taskMgr.removeTasksMatching('*Name*')
		self.taskMgr.removeTasksMatching('*name*')
		self.taskMgr.removeTasksMatching('*collide*')
		self.taskMgr.removeTasksMatching('*bullet*')
		self.taskMgr.removeTasksMatching('*Tank*')
		self.taskMgr.add(self._updatePositions, 'gameDataDisplay')
		#print self.taskMgr.getAllTasks()
		
		def setSpeed(num):
			#print "Heyo displaySpeed"
			self.displaySpeed = num 

		self.accept('1', setSpeed, [1])
		self.accept('2', setSpeed, [2])
		self.accept('3', setSpeed, [4])
		self.accept('4', setSpeed, [8])
		self.accept('0', setSpeed, [0])
		self.accept('5', setSpeed, [-1])
		self.accept('6', setSpeed, [-2])
		self.accept('7', setSpeed, [-4])

		self.frame = 0
		self.startTime = globalClock.getRealTime()

		while self.frame < len(self.gameData) - 1:
			self.taskMgr.step()
			globalClock.tick()

		self.taskMgr.removeTasksMatching('*Positions*')

		#Pause for two seconds at end: Probably launch victory/defeat screen here
		victory = ''

		if self.victoryState == 0:
			victory = 'Time Out'
		elif self.victoryState == 1:
			victory = 'Victory'
		elif self.victoryState == 2:
			victory = 'Defeat'

		#print victory
		from direct.gui.OnscreenText import OnscreenText
		textObject = OnscreenText(text = victory, 
			pos = (0, 0), scale = 0.3, bg=VBase4(.6,.6,.6,.1), fg=VBase4(0,0,0,95))
		
		self._endTime = globalClock.getRealTime()
		
		while globalClock.getRealTime() < self._endTime + 2:
			self.taskMgr.step()
			globalClock.tick()
			#print textObject

	def _updatePositions(self, task):

		try:
			dt = 1.0/60			
			if dt > .1:
				return Task.cont
			moveAmount = 50*dt;
			changeY =  (inputState.isSet('foward')-inputState.isSet('backward'))*moveAmount
			changeX = (inputState.isSet('right')-inputState.isSet('left'))*moveAmount;

			base.cam.setPos(base.cam,changeX,changeY,0)	
			hpr = base.cam.getHpr()
			if base.mouseWatcherNode.hasMouse() and self.doMouseStuff:	
				hpr.x = -100*base.mouseWatcherNode.getMouseX()
				hpr.y = 100*base.mouseWatcherNode.getMouseY()

			base.cam.setHpr(hpr)

		except:
			print "error in TankWorld._updatePositions"
		
		self._lastTime = self._displayTime
		self._displayTime = globalClock.getRealTime() - self.startTime
		self.frameTime += self.displaySpeed * (self._displayTime - self._lastTime)
		self.frame = int(60 * self.frameTime)
		#print self.frame, (self._displayTime - self._lastTime)
		if self.frame < len(self.gameData) - 1:
			frameData = self.gameData[self.frame]

			#print 'TankWorld._updatePositions: ', self._displayTime, self.frame, len(self.gameData)

			for i in range(len(self.dynamics)):	
				dynamic = self.dynamics[i]
				if i < len(frameData):
					dynamic.show()
					dynData = frameData[i]
					if (len(dynData) == 6):
						dynamic.setPos(Point3(dynData[0], dynData[1], dynData[2]))
						dynamic.setHpr(Point3(dynData[3], dynData[4], dynData[5]))
					else:
						dynamic.hide()
				else:
					dynamic.hide()



		return task.cont

	def preCalc(self):
		if self.taskMgr.hasTaskNamed('igLoop'):
			self.igLoop = self.taskMgr.getTasksNamed('igLoop')[0]

		self.realTime = False
		self.taskMgr.removeTasksMatching('*bullet*')
		self.taskMgr.add(self.__update2,"bullet-update")

		for i in self._afterStarts:
			self.doMethodLater(i[0], i[1], i[2])

		#Exits when win. lose, or more than 1 minute(s)
		while self.victoryState == 0 and len(self.gameData) < 60 * 60:
			self.taskMgr.remove('igLoop')
			self.updateLaterTasks()
			self.taskMgr.step()
			globalClock.tick()

		self.isOver = True
		#print self.dynamics
		self.__display()

	def doMethodLater(self, time, task, name = ''):
		if self.realTime:
			ShowBase.doMethodLater(self, time, task, name)
		else:
			self.laterTasks.append([time, task, name])

	def doMethodAfterStart(self, time, task, name = ''):
		self._afterStarts.append([time, task, name])

	def updateLaterTasks(self, time = 1.0/60.0):
		for i in range(len(self.laterTasks)):
			if i < len(self.laterTasks):
				self.laterTasks[i][0] -= time #Reduces time until run
				while i < len(self.laterTasks) and self.laterTasks[i][0] < 0:
					self.taskMgr.add(self.laterTasks[i][1], self.laterTasks[i][2])
					self.laterTasks.pop(i)
					if i < len(self.laterTasks):
						self.laterTasks[i][0] -= time

	def __update2(self, task):
		'''
		Task task: Time since last frame	
		'''
		try:
			stepSize = 1.0 / 60.0

			#set up a fixed time constant step for more accurate physics.
			
			self.__bulletWorld.doPhysics(stepSize)

			self.gameData.append([])
			numFrames = len(self.gameData) - 1

			for i in range(len(self.dynamics)):
				self.gameData[numFrames].append(array('f'))
				dynamic = self.dynamics[i]
				if not dynamic._nodePath.is_empty() and not dynamic._nodePath.isHidden():
					pos = dynamic.getPos()
					hpr = dynamic.getHpr()
					self.gameData[numFrames][i].extend(pos)
					self.gameData[numFrames][i].extend(hpr)
				else:
					x = 1
		
			if len(self.gameData) % 60 == 0:
				self.debugTime += 1
				#print self.debugTime

		except:
			print "error tankworld.__update2	"

		return task.cont

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

	def close(self, task=None):
		self.taskMgr.removeTasksMatching("*")
		self.isDead = True
		self.shutdown()
		
		#pdb.set_trace()
		self.exitfunc()
		self.destroy()
		sys.exit()
		#sys.exit()

	def run(self):
		for i in self._afterStarts:
			self.taskMgr.doMethodLater(i[0], i[1], i[2])
		ShowBase.run(self)

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
	def getUserTank(self, n=0):
		'''
			Gets the user tank. Currently not implemented for multiple tanks.
		'''
		return self.tanks[n]

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

		#print "TankWorld.drawDebugNode: debug node activated" 
		self.accept('9', self.debugNP.show)
		self.accept('8', self.debugNP.hide)

		self.__bulletWorld.setDebugNode(debugNode)

	#Victory conditions

	def victory(self):
		'''
			Called when a victory condition has been met
		'''
		#print "YOU HAVE WON THE GAME"
		#pdb.set_trace()
		self.victoryState = 1

#		from direct.gui.OnscreenText import OnscreenText
#		textObject = OnscreenText(text = 'Victory',
#			pos = (0, 0), scale = 0.3, bg=VBase4(.6,.6,.6,.1), fg=VBase4(0,0,0,95))
		self.taskMgr.remove('bullet-update')
		self.taskMgr.doMethodLater(2, self.close, 'close Task Name')

	def lose(self):
		'''
			Called when a loss condition has been met
		'''
		#print "YOU HAVE LOST THE GAME"
		self.victoryState = 2
		self.taskMgr.remove('bullet-update')
		self.taskMgr.doMethodLater(2, self.close, 'close Task Name')



	#functions for our taskManager
	def add(self,functionptr,name='asd',upondeath=None):
		self.taskList.append([functionptr, name, upondeath])

	def stepTasks(self, task):
		try:
			removeTasks = []
			count =0	
			#print self.taskMgr.getAllTasks()
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

	def setLevelData(self,level):
		self.levelData = level

	def getLevelData(self):
		return self.levelData

	def registerDynamic(self, dynamic):
		#print dynamic
		self.dynamics.append(dynamic)

	def isRealTime(self):
		return self.realTime
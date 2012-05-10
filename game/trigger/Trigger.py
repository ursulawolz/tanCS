import sys
sys.path.append("..")

import pdb

class Trigger(object):
	
	def __init__(self, tankWorld, function=None, numTriggers=-1):
		#print tankWorld.taskMgr
		#tankWorld.add(self.checkConditions,"asddff") #This creates a task named update and runs every frame
		self.tankWorld = tankWorld
		self.states = []
		tankWorld.add(self.checkConditions,0)
		self.numTriggers = numTriggers
		if function == None:
			self.function = self.win
		else:
			self.function = function

		#print "Trigger.__init__ : Method added"
		pass

	def addState(self, state):
		self.states.append(state)

	def checkConditions(self, task):
		'''Override me. Use this to check to see if the player has won or lost.''' 
		for s in self.states:
			s.checkConditions(task)
		triggeredCount = 0
		for s in self.states:
			triggeredCount += s.hasTriggered()

		if triggeredCount >= self.numTriggers and self.numTriggers >= 0:
			self.function()

		if triggeredCount ==  len(self.states) and self.numTriggers == -1:
			self.function()
		return task.cont
		

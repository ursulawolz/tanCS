import sys
sys.path.append("..")

import pdb
class State(object):

	def __init__(self, tankWorld):
		#print tankWorld.taskMgr
		#tankWorld.add(self.checkConditions,"asddff") #This creates a task named update and runs every frame
		self.tankWorld = tankWorld
		self.states = []
		tankWorld.add(self.checkConditions,0)

		self.triggered = False

	def checkConditions(self, task):
		'''Override me. To check for a state''' 

		pass

	def hasTriggered(self):
		return self.triggered


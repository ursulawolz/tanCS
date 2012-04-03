import pdb
class Trigger(object):

	def __init__(self, tankWorld):
		#print tankWorld.taskMgr
		#tankWorld.add(self.checkConditions,"asddff") #This creates a task named update and runs every frame
		self.tankWorld = tankWorld
		tankWorld.add(self.checkConditions,0)
		print "Method added"
		pass

	def checkConditions(self, task):
		'''Override me. Use this to check to see if the player has won or lost.''' 

		pass

		
	def win(self):
		print self.tankWorld
		#pdb.set_trace()
		self.tankWorld.victory()

	def lose(self):
		self.tankWorld.lose()

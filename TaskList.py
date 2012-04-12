from direct.task import Task

def setCollision(worldObject, tankWorld):
	'''Creates a task named collide, that will call handleCollision on the 
	worldObject that setCollion is called with. 

	handleCollision must deal with ending the task. The task name is:
		worldObject.getNodePath().node().getName() + 'collide'
	'''
	bulletWorld = tankWorld.getPhysics()
	bulletNode = worldObject.getNodePath().node()
	taskName = bulletNode.getName() + 'collide'

	#Nested functions? are legit
	def collide(task):

		result = bulletWorld.contactTest(bulletNode)
		for i in range(result.getNumContacts()):
			worldObject.handleCollision(result.getContact(i), taskName)

		return task.cont

	tankWorld.taskMgr.add(collide, taskName)
	

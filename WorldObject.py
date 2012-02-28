from TankWorld import *

class WorldObject:
	"""Parent Class for all physical objects present in TankWorld. 
Variables: 	.node > BulletRigidBodyNode for physics simulation
		.nodePath > Panda NodePath for rendering. Includes some state variables.		
"""

	def __init__(self, world, attach, name = '', xCoord = 0, yCoord = 0, zCoord = 0, shape = BulletBoxShape(Vec3(.1, .1, .1)), heading = 0, pitch = 0, roll = 0, xVel = 0, yVel = 0, zVel = 0, mass = 0.1):
	#@param world: A BulletWorld for this to be simulated in
	#@param attach: a NodePath to attach this WorldObject to. By default send some ShowBase.render		

		self._nodePath = attach.attachNewNode(BulletRigidBodyNode(name)) 	#Bullet node for rendering and physics - this is what this class manipulates
		self._world = world
		self._nodePath.node().setMass(mass)					#Only static objects should have 0 mass
		
		#The NodePath holds rendering state variables	
		self._nodePath.setPos(xCoord, yCoord, zCoord) 
 		self._nodePath.setHpr(heading, pitch, roll)		

		#Bullet's Node holds other physics-based state variables
		self._nodePath.node().setLinearVelocity(Vec3(xVel, yVel, zVel))
		self._nodePath.node().addShape(shape)
		self._world.attachRigidBody(self._nodePath.node())


	def getVel(self):
		return self._nodePath.node().getLinearVelocity()

	def getPos(self):
		return self._nodePath.getPos()

	def getHpr(self):
		return self._nodePath.setHpr()

	def getShape(self):
		return self.shape ##I'm not sure this is the correct implimentation.

	def getMass(self):
		return self._nodePath.node().getMass()
	

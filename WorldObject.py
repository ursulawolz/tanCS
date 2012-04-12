from panda3d.core import Vec3, Point3, BitMask32, TransformState
from pandac.PandaModules import PandaNode
from direct.showbase.ShowBase import ShowBase
from panda3d.bullet import BulletRigidBodyNode, BulletBoxShape, BulletWorld, BulletDebugNode
import TaskList
import math


class WorldObject(object):
    """Parent Class for all physical objects present in TankWorld. 
    Variables:
    .node > BulletRigidBodyNode for physics simulation
    .nodePath > Panda NodePath for rendering. Includes some state variables.
    """

    def __init__(self, tankWorld, attach, name = '', position = Point3(0,0,0), shape = BulletBoxShape(Vec3(.1, .1, .1)), orientation = Vec3(0,0,0), velocity = Vec3(0,0,0), mass = 0.1):
	#@param world: A BulletWorld for this to be simulated in
	#@param attach: a NodePath to attach this WorldObject to. By default send some ShowBase.render		

        self._nodePath = attach.attachNewNode(BulletRigidBodyNode(name)) 	#Bullet node for rendering and physics - this is what this class manipulates
        self._tankWorld = tankWorld
        self._nodePath.node().setMass(mass)					#Only static objects should have 0 mass


        #The NodePath holds rendering state variables	
        self._nodePath.setPos(position[0], position[1], position[2]) 
        self._nodePath.setHpr(orientation[0], orientation[1], orientation[2])		

        #Bullet's Node holds other physics-based state variables
        self._nodePath.node().setLinearVelocity(velocity)
        self._transformState = getattr(self, '_transformState',TransformState.makePos(Point3(0, 0, 0)))
        
        self._nodePath.node().addShape(shape,self._transformState)
        self._tankWorld.attachRigidBody(self._nodePath.node())
        
        #self._nodePath.setCollideMask(BitMask32.allOn())

    def getVel(self):
        return self._nodePath.node().getLinearVelocity()
    def getName(self):
        return self._nodePath.getName()
        
    def getPos(self):
        return self._nodePath.getPos()

    def getTankWorld(self):
        return self._tankWorld

    def getHpr(self):
        return self._nodePath.getHpr()

    def getShape(self):
        return self.__shape ##I'm not sure this is the correct implimentation.

    def getMass(self):
        return self._nodePath.node().getMass()
	
    def getNodePath(self):
        return self._nodePath

    def fixAngle(self, angle):
        if angle < 0:
            angle += 360
        elif angle > 360:
            angle -= 360
        return angle
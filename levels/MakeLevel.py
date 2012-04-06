import sys
sys.path.append("..")

from TankWorld import TankWorld
from panda3d.core import *

from CubeObject import CubeObject
from trigger.PositionTrigger import PositionTrigger
from FloorStaticObject import FloorStaticObject
from Tank import Tank
t = None #globnal cube object
def vec(val):
	return VBase3(val[0],val[1],val[2])

def makeCubeObject(position=(0,0,0), size=(1,1,1), name='cubeobject', orientation=(0,0,0)):
	return CubeObject(t, t.render, position=vec(position), orientation=vec(orientation), name=name, scale = vec(size))

def makeFloor(position=(0,0,0), name='cubeobject', orientation=(0,0,0)):	
	return FloorStaticObject(t,t.render, position=vec(position), orientation=vec(orientation), name=name)

def makePositionTrigger(target = None, position=(0,0,0)):
	return PositionTrigger(t,target, position=vec(position))

def makeTank(position=(0,0,0), orientation=(0,0,0), name='tank'):
	return Tank(t,t.render, position=vec(position), orientation=vec(orientation), name=name)



def makeLevel(fileName, tankWorld= None):
	global t
	if tankWorld == None:
		tankWorld = TankWorld()
		tankWorld.getPhysics().setGravity(Vec3(0,0,-9.81))
	t = tankWorld
	execfile('levels/'+fileName+'.py')
	return t


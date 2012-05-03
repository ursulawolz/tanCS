import sys
sys.path.append("..")

from TankWorld import TankWorld
from panda3d.core import *

from CubeObject import CubeObject
from trigger.CollisionState import CollisionState
from trigger.PadState import PadState
from trigger.Trigger import Trigger
from FloorStaticObject import FloorStaticObject
from Tank import Tank
from weapon.Blaster import Blaster
from weapon.TurretBlaster import TurretBlaster
from UserTank import UserTank
from Turret import Turret
t = None #global cube object

def vec(val):
	return VBase3(val[0],val[1],val[2])

def makeCubeObject(position=(0,0,0), size=(1,1,1), name='cubeobject', orientation=(0,0,0)):
	return CubeObject(t, t.render, position=vec(position), orientation=vec(orientation), name=name, scale = vec(size))

def makeFloor(position=(0,0,0), name='floor', orientation=(0,0,0), size=(32, 32)):	
	return FloorStaticObject(t,t.render, position=vec(position), orientation=vec(orientation), name=name, size=size)

def makeTrigger(target = None, function=None, position=(0,0,0)):
	global t
	if function == None:
		function = t.victory
	return Trigger(t,function=function)

def makeCollisionState(trigger, tracking_object=None, tracking_name='tank', position=(0,0,0), orientation=(0,0,0), name='collisionState', size=(2,2,2) ):
	if tracking_object != None:
		tracking_name = tracking_object.getName()
		
	s = CollisionState(t,tracking_name, position=vec(position), name=name, size=vec(size))
	trigger.addState(s)
def makeTurret(position=(0,0,0), orientation=(0,0,0), name='turret'):
	return Turret(t, t.render, position=vec(position), orientation=vec(orientation), name=name)

def makePadState(trigger, tracking_object=None, tracking_name='tank', position=(0,0,0), orientation=(0,0,0), name='PadState', size=(2,2,2) ):
	if tracking_object != None:
		tracking_name = tracking_object.getName()
		
	s = PadState(t,tracking_name, position=vec(position), name=name, size=vec(size))
	trigger.addState(s)


def makeTank(position=(0,0,0), orientation=(0,0,0), name='tank'):
	
	tank = Tank(t,t.render, position=vec(position), orientation=vec(orientation), name=name)
	usertank = UserTank(tank)
	return tank

def makeBlaster(obj):
	b = Blaster(obj)
	obj.setWeapon(b)
	return b

def makeTurretBlaster(obj):
	b = TurretBlaster(obj)
	obj.setWeapon(b)
	return b

def addLevelData(data):
	t.setLevelData(data)

def makeLevel(fileName, tankWorld= None):
	global t
	if tankWorld == None:
		tankWorld = TankWorld()
		tankWorld.getPhysics().setGravity(Vec3(0,0,-9.81))
	t = tankWorld
	execfile('../game/'+'levels/'+fileName+'.py')
	return t



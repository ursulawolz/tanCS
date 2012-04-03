try:
	import lxml.etree as ElementTree
except ImportError:
	try:
		import xml.etree.cElementTree as ElementTree
	except ImportError:
		import xml.etree.ElementTree as ElementTree


from panda3d.core import *
from TankWorld import TankWorld
from MeshWorldObject import MeshWorldObject
from FloorStaticObject import FloorStaticObject
from Tank import Tank
from DynamicWorldObject import DynamicWorldObject
import TaskList

from panda3d.bullet import BulletPlaneShape
from panda3d.bullet import BulletRigidBodyNode
from runFile import runFile

from Blaster import Blaster
from PositionTrigger import PositionTrigger

def parseVec3(string):
	'''
		Converts '1,2,3' to a vec3
	'''
	st = string.split(',')
	return Vec3(float(st[0]),float(st[1]),float(st[2]))


def readWorldObject(element, tankWorld):
	'''
		Helper to get position and rotation of world objects. 
	'''
	pos = Vec3(0,0,0)
	rot = Vec3(0,0,0)
	name = element.attrib.get('name','No name given')
	print element.attrib
	for at in element.attrib:
		
		if at == 'pos':
			pos = parseVec3(element.attrib[at])

	return pos,rot, name
def readTrigger(element, tankWorld):
	triggerType = element.attrib.get('type', 'default').lower()

	pos,rot,name = readWorldObject(element, tankWorld)
	targetName = element.attrib.get('target')
	radius = int(element.attrib.get('radius',5))

	if triggerType == 'position':
		potentialNPs = tankWorld.render.getChildren()

	target = None
	for np in potentialNPs:
		print np.node().getClassType()
		#if np.node().getClassType() == BulletRigidBodyNode.getClassType():

		if np.getName() == targetName:
			target = np
			break

	PositionTrigger(tankWorld,target, radius=radius)



def readStaticObject(element, tankWorld):
	'''
		Reads a static object. and creates it.
	'''
	(pos, rot, name) = readWorldObject(element, tankWorld)
	filename = element.attrib.get('mesh','rock1.egg')

	for shape in  element:
		if shape.attrib.get('type','mesh').lower() == 'mesh':
			static = MeshWorldObject(tankWorld,render, filename, position=pos, orientation=rot, name=name)
			break
		if shape.attrib.get('type','mesh').lower() == 'floor':
			static = FloorStaticObject(tankWorld,render, filename, position=pos, orientation=rot, name=name)
			break

		#Do other types of shapes here

def readTankObject(element, tankWorld):
	'''
	Reads a tank object from xml
	'''
	print element
	(pos, rot, name) = readWorldObject(element, tankWorld)
	#tank = Tank(tankWorld,	 tankWorld.render, )
	tank = Tank(tankWorld,render,position=pos, orientation=rot, name=name)
	weapon = ''
	weaponClasses = {'blaster':Blaster}

	#reads the weapon class and creates it
	for w in element:
		#grab wepon
		if w.tag == 'weapon':
			weapon = w.attrib.get('type','blaster').lower()
	if weapon != '':
		tank.setWeapon(weaponClasses[weapon](tank))


def createLevel(file, tankWorld = None):
	'''
		Creates the level. THis is the main function that goes through and calls other functions to parse the xml file.
	'''
	if tankWorld == None:
		tankWorld = TankWorld()
		tankWorld.getPhysics().setGravity(Vec3(0,0,-9.81))

	doFunctions = {'staticobject': readStaticObject, 'tank':readTankObject, 'trigger':readTrigger}
	f = open(file)

	element =ElementTree.XML(f.read())

	for level in element:
		#This is going to be each section
		doFunctions[level.tag.lower()](level, tankWorld)
	
	return tankWorld
	




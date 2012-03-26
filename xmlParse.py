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


def parseVec3(string):
	'''
		Converts '1,2,3' to a vec3
	'''
	st = string.split(',')
	return Vec3(int(st[0]),int(st[1]),int(st[2]))


def readWorldObject(element, tankWorld):
	'''
		Helper to get position and rotation of world objects. 
	'''
	pos = Vec3(0,0,0)
	rot = Vec3(0,0,0)
	print element.attrib
	for at in element.attrib:
		
		if at == 'pos':
			pos = parseVec3(element.attrib[at])

	return pos,rot
def readStaticObject(element, tankWorld):
	'''
		Reads a static object. and creates it.
	'''
	(pos, rot) = readWorldObject(element, tankWorld)
	filename = element.attrib.get('mesh','rock1.egg')

	for shape in  element:
		if shape.attrib.get('type','mesh').lower() == 'mesh':
			static = MeshWorldObject(tankWorld,render, filename, position=pos, orientation=rot)
			break
		if shape.attrib.get('type','mesh').lower() == 'floor':
			static = FloorStaticObject(tankWorld,render, filename, position=pos, orientation=rot)
			break
		#Do other types of shapes here

def readTankObject(element, tankWorld):
	'''
	Reads a tank object from xml
	'''
	print element
	(pos, rot) = readWorldObject(element, tankWorld)
	#tank = Tank(tankWorld,	 tankWorld.render, )

	tank = Tank(tankWorld,render,'TankName',position=pos, orientation=rot)
	weapon = ''
	weaponClasses = {'blaster':Blaster}

	#reads the weapon class and creates it
	for w in element:
		#grab wepon
		if w.tag == 'weapon':
			weapon = w.attrib.get('type','blaster').lower()
	if weapon != '':
		tank.setWeapon(weaponClasses[weapon](tank))


def createLevel(file):
	'''
		Creates the level. THis is the main function that goes through and calls other functions to parse the xml file.
	'''
	tankWorld = TankWorld()
	tankWorld.getPhysics().setGravity(Vec3(0,0,-9.81))

	doFunctions = {'staticobject': readStaticObject, 'tank':readTankObject}
	f = open(file)

	element =ElementTree.XML(f.read())

	for level in element:
		#This is going to be each section
		doFunctions[level.tag.lower()](level, tankWorld)
	
	return tankWorld
	




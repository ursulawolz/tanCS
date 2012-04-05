from StaticWorldObject import StaticWorldObject
from panda3d.core import * 
from panda3d.bullet import BulletBoxShape

class CubeObject(StaticWorldObject):
	def __init__(self, world, attach, mesh, name = '', position = Vec3(0,0,0), orientation = Vec3(0,0,0), scale = Vec3(1,1,1) ):
		shape = BulletBoxShape(scale)
		
		super(self, CubeObject).__init__(world, attach, mesh, name, position=position, orientation=orientation, scale=scale)


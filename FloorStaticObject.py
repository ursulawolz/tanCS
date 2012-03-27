from StaticWorldObject import *
from Imports import *
from panda3d.core import Quat, Mat4, CardMaker, Material, VBase4
from panda3d.bullet import BulletPlaneShape


class FloorStaticObject(StaticWorldObject):
	"""
		Object for testing. Creates a plane with a plain texture.
	"""
	
	def __init__(self, world, attach, mesh, name = '', position = Vec3(0,0,0), orientation = Vec3(0,0,0)):

		cm=CardMaker('')
		cm.setFrame(-20,20,-20,20)
		floor = render.attachNewNode(PandaNode("floor"))

		nn = floor.attachNewNode(cm.generate())
		nn.setPos(0,0,0)
		nn.setP(-90)

		myMaterial = Material()
		myMaterial.setShininess(0) #Make this material shiny
		myMaterial.setAmbient(VBase4(0.5,.5,.5,1)) #Make this material blue
		myMaterial.setDiffuse(VBase4(.5,.5,.5,1))
		nn.setMaterial(myMaterial)
		shape = BulletPlaneShape(Vec3(0, 0, 1), 1)

		StaticWorldObject.__init__(self, world, attach, name, position, shape, orientation) ##Mass must be zero.

		self._nodePath.node().setFriction(1)

		#geo.reparentTo(self._nodePath)
from StaticWorldObject import *
from Imports import *
from panda3d.core import Quat, Mat4, CardMaker, Material, VBase4, CardMaker, Texture
from panda3d.bullet import BulletPlaneShape


class FloorStaticObject(StaticWorldObject):
	"""
		Object for testing. Creates a plane with a plain texture.
	"""
	
	def __init__(self, world, attach, name = '', position = Vec3(0,0,0), orientation = Vec3(0,0,0), size = 32):
		cm=CardMaker('')
		cm.setFrame(0,1,0,1)
		floor = render.attachNewNode(PandaNode("floor"))
		tex = loader.loadTexture('media/'+'ground.png')
		tex.setMagfilter(Texture.FTNearest)
		tex.setMinfilter(Texture.FTNearest)
		for y in range(size):
			for x in range(size):
				nn = floor.attachNewNode(cm.generate())
				nn.setP(-90)
				nn.setPos((x), (y), 0)
		floor.setTexture(tex)
		floor.flattenStrong()



		myMaterial = Material()
		myMaterial.setShininess(0) #Make this material shiny
		myMaterial.setAmbient(VBase4(0.5,.5,.5,1)) #Make this material blue
		myMaterial.setDiffuse(VBase4(.5,.5,.5,1))
		nn.setMaterial(myMaterial)
		shape = BulletPlaneShape(Vec3(0, 0, 1), 0)

		StaticWorldObject.__init__(self, world, attach, name, position, shape, orientation) ##Mass must be zero.

		self._nodePath.node().setFriction(1)

		#geo.reparentTo(self._nodePath)

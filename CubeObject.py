from StaticWorldObject import StaticWorldObject
from panda3d.core import * 
from panda3d.bullet import BulletBoxShape

class CubeObject(StaticWorldObject):
	def __init__(self, world, attach, name = '', position = Vec3(0,0,0), orientation = Vec3(0,0,0), scale = Vec3(1,1,1), texture='test.png' ):
		shape = BulletBoxShape(scale/2)
		self._transformState = TransformState.makePos(Point3(scale.x/2,scale.y/2,scale.z/2)) #offset
			
		self.geo = loader.loadModel('media/'+'cube.x')
		
		
		tex = loader.loadTexture('media/'+texture)
		tex.setMagfilter(Texture.FTNearest)
		tex.setMinfilter(Texture.FTNearest)
		self.geo.setTexture(tex)

		for x in range(int(scale[0])):
			for y in range(int(scale[1])):
				for z in range(int(scale[2])):

					newNode = render.attachNewNode('node')
					#geo.setScale(scale)
					newNode.setPos(position+VBase3(x,y,z))
					#geo.setHpr(orientation)
					self.geo.instanceTo(newNode)
					


		#geo.setTexGen(TextureStage.getDefault(), TexGenAttrib.MWorldPosition)
		#geo.setTexTransform(TextureStage.getDefault(), TransformState.makeScale(scale*2))
		
		
		StaticWorldObject.__init__(self, world, attach, name, position, shape, orientation) 

	def setTexture(self, texture):
		tex = loader.loadTexture('media/'+texture)
		tex.setMagfilter(Texture.FTNearest)
		tex.setMinfilter(Texture.FTNearest)
		self.geo.setTexture(tex)

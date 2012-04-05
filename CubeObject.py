from StaticWorldObject import StaticWorldObject
from panda3d.core import * 
from panda3d.bullet import BulletBoxShape

class CubeObject(StaticWorldObject):
	def __init__(self, world, attach, name = '', position = Vec3(0,0,0), orientation = Vec3(0,0,0), scale = Vec3(1,1,1), texture='test.png' ):
		shape = BulletBoxShape(scale/2)
		self._transformState = TransformState.makePos(Point3(scale.x/2,scale.y/2,scale.z/2)) #offset
		
		tex = loader.loadTexture(texture)
		tex.setMagfilter(Texture.FTNearest)
		tex.setMinfilter(Texture.FTNearest)
		
		for x in range(int(scale[0])):
			for y in range(int(scale[1])):
				for z in range(int(scale[2])):

					geo = loader.loadModel('cube.x')
					#geo.setScale(scale)
					geo.setPos(position+VBase3(x,y,z))
					#geo.setHpr(orientation)
					geo.reparentTo(render)
					geo.setTexture(tex)


		#geo.setTexGen(TextureStage.getDefault(), TexGenAttrib.MWorldPosition)
		#geo.setTexTransform(TextureStage.getDefault(), TransformState.makeScale(scale*2))
		
		
		StaticWorldObject.__init__(self, world, attach, name, position, shape, orientation) 


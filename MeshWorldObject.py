from StaticWorldObject import *
from Imports import *
from panda3d.core import Quat, Mat4
from panda3d.bullet import BulletTriangleMeshShape
from panda3d.bullet import BulletTriangleMesh

class MeshWorldObject(StaticWorldObject):
	"""
	Class that Allows the user to load up a static mesh and add a physics collider to it. DO NOT USE ME unless there is no alternative. Really slows down with high polygon models.
	"""
	
	#DO NOT USE ME 
	def __init__(self, world, attach, mesh, name = '', position = Vec3(0,0,0), shape = BulletBoxShape(Vec3(.1, .1, .1)), orientation = Vec3(0,0,0)):

		geo = loader.loadModel(mesh)
		geo.reparentTo(render)
		rotation = Vec3(0,0,0)
		geo.setHpr(rotation)
		
		mesh = BulletTriangleMesh()
		geomNodes = geo.findAllMatches('**/+GeomNode')
		for np in  geomNodes:
			#geomNode = geomNodes.getPath(0).node()
			geomNode = np.node()
			geom = geomNode.getGeom(0)
			mesh.addGeom(geom)

		q = Quat()
		q.setHpr(rotation)
		#mat = Mat4.identMat()
		mat = Mat4.yToZUpMat ()
		#mat[2][2] = 0
		#mat[2][1] = 1
		#mat[1][1] = 0
		#mat[1][2] = 1

		self._transformState = TransformState.makeMat(mat)
		#self._transformState
		#self._transformState = TransformState.makeQuat(q) 

		shape = BulletTriangleMeshShape(mesh, dynamic=False)
		StaticWorldObject.__init__(self, world, attach, name, position, shape, orientation) ##Mass must be zero.
		geo.reparentTo(self._nodePath)
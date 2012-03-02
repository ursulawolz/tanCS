from panda3d.core import *
import TankWorld
from DynamicWorldObject import DynamicWorldObject

from panda3d.bullet import BulletPlaneShape
from panda3d.bullet import BulletRigidBodyNode

print("asdf")
t = TankWorld.TankWorld()
t.getPhysics().setGravity(Vec3(0,0,-9.81))
 
shape = BulletPlaneShape(Vec3(0, 0, 1), 1)
 
node = BulletRigidBodyNode('Ground')
node.addShape(shape)
 
np = render.attachNewNode(node)
np.setPos(0, 0, -2)

t.getPhysics().attachRigidBody(node)

print t.getPhysics().getNumRigidBodies(), "before"
dynamic = DynamicWorldObject(t.getPhysics(),render)
print t.getPhysics().getNumRigidBodies(), "after"
run()


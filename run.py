from panda3d.core import *
from TankWorld import TankWorld
from Tank import Tank
from DynamicWorldObject import DynamicWorldObject
import TaskList

from panda3d.bullet import BulletPlaneShape
from panda3d.bullet import BulletRigidBodyNode

print("asdf")
t = TankWorld()
t.getPhysics().setGravity(Vec3(0,0,-9.81))

shape = BulletPlaneShape(Vec3(0, 0, 1), 1)

node = BulletRigidBodyNode('Ground')
node.setFriction(1);
node.addShape(shape)

np = render.attachNewNode(node)
np.setPos(0, 0, -4)

t.getPhysics().attachRigidBody(node)

print t.getPhysics().getNumRigidBodies(), "before"
#dynamic = DynamicWorldObject(t.getPhysics(),render)
ta = Tank(t.getPhysics(),render)
ta.setTankWorld(t)
print t.getPhysics().getNumRigidBodies(), "after"

TaskList.setCollision(ta, t)

run()


from panda3d.core import *
from TankWorld import TankWorld
from MeshWorldObject import MeshWorldObject
from Tank import Tank
from DynamicWorldObject import DynamicWorldObject
import TaskList

from panda3d.bullet import BulletPlaneShape
from panda3d.bullet import BulletRigidBodyNode
from runFile import runFile
print("asdf")
t = TankWorld()
t.getPhysics().setGravity(Vec3(0,0,-9.81))


static = MeshWorldObject(t,render, 'rock1.egg', position=Vec3(0,10,0))
static = MeshWorldObject(t,render, 'tree.egg', position=Vec3(4,4,4))

shape = BulletPlaneShape(Vec3(0, 0, 1), 1)

node = BulletRigidBodyNode('Ground')
node.setFriction(1);
node.addShape(shape)

np = render.attachNewNode(node)
np.setPos(0, 0, -4)

t.getPhysics().attachRigidBody(node)

print t.getPhysics().getNumRigidBodies(), "before"
#dynamic = DynamicWorldObject(t.getPhysics(),render)

runFile('user.py',t)
print t.getPhysics().getNumRigidBodies(), "after"

#TaskList.setCollision(ta, t)

run()

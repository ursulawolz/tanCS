from panda3d.core import *
from TankWorld import TankWorld
from MeshWorldObject import MeshWorldObject

from runFile import runFile

import xmlParse

print("asdf")

#orion says hello
t = xmlParse.createLevel('testLevel.xml')

#shape = BulletPlaneShape(Vec3(0, 0, 1), 1)

#node = BulletRigidBodyNode('Ground')
#node.setFriction(1)
#node.addShape(shape)

#np = render.attachNewNode(node)
#np.setPos(0,0,-4)
#t.getPhysics().attachRigidBody(node)

#print "asdfasdfasdf"
#np.setPos(0, 0, 0)


runFile('user.py',t)

#TaskList.setCollision(ta, t)

t.run()
print "done?"
sys.exit()

from TankWorld import *
from Tank import Tank
from panda3d.bullet import BulletPlaneShape


t = TankWorld()
t.getPhysics().setGravity(Vec3(0,0,-9.8))
bulletWorld = t.getPhysics()
ground = BulletRigidBodyNode('ground')
ground.addShape(BulletPlaneShape(Vec3(0,0,1), 1))

 
gNP = render.attachNewNode(ground)
gNP.setPos(0,0,-1)
t.attachRigidBody(ground)


for i in range(100):
	seek = Tank(t, render, None, 'Hide' + str(i), 2000 * int(i/10) , 2000 * (i%10), 7)


seek = Tank(t, render, None, 'Seek', 250, -700, 10)
seek.setTankWorld(t)

x = seek.scan(360*100)
y = seek.distanceScan()

print x, y, len(x), len(y)

t.run()


import random
x = random.randint(6,13)
#x= 50

tank = makeTank(position=(3,3.5,2), orientation=(90,0,0), name="tank")
makeFloor()
	
makeCubeObject(size=(x*2+8,1,3), position=(0,0,0), name="wall1")
makeCubeObject(size=(x,1,3), position=(0,6,0), name="wall1")
makeCubeObject(size=(x-3,1,3), position=(x+5,6,0), name="wall1")

makeCubeObject(size=(1,5,3), position=(0,1,0), name="wall1")
makeCubeObject(size=(1,26,3), position=(x*2+5+2,0,0), name="wall1")
makeCubeObject(size=(1,20,3), position=(x*2+2,6,0), name="wall1")
makeCubeObject(size=(6,1,3), position=(x*2+2,26,0), name="wall1")


makeCubeObject(size=(1,20,3), position=(x+5,6,0), name="wall1")
makeCubeObject(size=(1,20,3), position=(x,6,0), name="wall1")
makeCubeObject(size=(6,1,3), position=(x,26,0), name="wall1")


b = makeBlaster(tank)

trigger = makeTrigger(function=tankWorld.victory)
makeCollisionState(trigger, position=(x+1,23,0), tracking_name=b.getBulletName(), size=(4,3,4))
makeCollisionState(trigger, position=(x*2+3,23,0), tracking_name=b.getBulletName(),size=(4,3,4))


#set up the level data

addLevelData({'x':x})

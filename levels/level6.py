
import random
x = random.randint(6,13)
x = 5

tank = makeTank(position=(3,3.5,.6), orientation=(90,0,0), name="tank")
makeFloor(size=(26,31))
	
h1 = x*5
makeCubeObject(size=(x*6,1,3), position=(0,0,0), name="wall1")
makeCubeObject(size=(x*6-5,1,3), position=(0,6,0), name="wall1")

makeCubeObject(size=(1,5,3), position=(0,1,0), name="wall1")

makeCubeObject(size=(1,x*4+5,3), position=(x*6,0,0), name="wall1")
makeCubeObject(size=(1,x*4-6,3), position=(x*6-5,6,0), name="wall1")

makeCubeObject(size=(x*5,1,3), position=(x*1+1,x*4+5,0), name="wall1")
makeCubeObject(size=(x*5-5*2,1,3), position=(x*1+5+1,x*4-1,0), name="wall1")

makeCubeObject(size=(1,x*4-1,3), position=(x*1+1,7,0), name="wall1")
makeCubeObject(size=(1,x*3-10,3), position=(x*1+6,x*1+9,0), name="wall1")

makeCubeObject(size=(x*2, 1,3), position=(x*1+6,x*1+8,0), name="wall1")

#makeCubeObject(size=(1,x*4-5,3), position=(x*6-5,6,0), name="wall1")
#makeCubeObject(size=(x-3,1,3), position=(x+5,6,0), name="wall1")



b = makeBlaster(tank)

trigger = makeTrigger(function=tankWorld.victory)
#makeCollisionState(trigger, position=(x+1,23,0), tracking_name=b.getBulletName(), size=(4,3,4))
makePadState(trigger, position=(x*6-4,1,0), tracking_name='tank',size=(5,5,1))
makePadState(trigger, position=(1,1,0), tracking_name='tank',size=(5,5,3))
makePadState(trigger, position=(x*6-4,x*4,0), tracking_name='tank',size=(5,5,1))
makePadState(trigger, position=(x*2-4,x*4,0), tracking_name='tank',size=(5,5,1))
makePadState(trigger, position=(x*2-4+1,7,0), tracking_name='tank',size=(6,5,1))
makePadState(trigger, position=(x*4+1,7,0), tracking_name='tank',size=(6,4,1))

makeCollisionState(trigger, position=(x*2+2,x*3,0), tracking_name='tank', size=(3,3,3))


#set up the level data

addLevelData({'data':[x*5, x*4, x*3+3, x*3-3, x*2+3, x*1,x*2]})

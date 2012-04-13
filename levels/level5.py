
x = 11
tank = makeTank(position=(3,3.5,2), orientation=(90,0,0), name="tank")
makeFloor()
	
makeCubeObject(size=(x*3-3,1,3), position=(0,0,0), name="wall1")
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
makeCollisionState(trigger, position=(x+2,23,0), tracking_name=b.getBulletName())
makeCollisionState(trigger, position=(x*2+4,23,0), tracking_name=b.getBulletName())


#set up the level data

addLevelData({'x':x})

makeFloor()
n = 30
makeCubeObject(size=(n,1,3), position=(0,0,0), name='wall1')
makeCubeObject(size=(n,1,3), position=(0,n,0), name='wall2')
makeCubeObject(size=(1,n,3), position=(0,1,0), name='wall3')
makeCubeObject(size=(1,n,3), position=(n-1,1,0), name='wall4')

tank = makeTank(position=(3,3.5,2), orientation=(90,0,0), name="tank")
makeBlaster(tank)

tank2 = makeTank(position=(n-3,n-3.5,2), orientation=(-90,0,0), name="tank2")
makeBlaster(tank2)

#trigger = makeTrigger(function=tankWorld.victory)
#makeCollisionState(trigger, position=(16,2.5,0), tracking_object=tank)


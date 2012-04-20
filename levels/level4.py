makeFloor(size=(10,20))
makeCubeObject(size=(20,1,3), position=(0,0,0), name='wall1')
makeCubeObject(size=(20,1,3), position=(0,10,0), name='wall2')
makeCubeObject(size=(1,9,3), position=(0,1,0), name='wall3')
makeCubeObject(size=(1,9,3), position=(19,1,0), name='wall4')

tank = makeTank(position=(4,3.5+2+1,.6), orientation=(90,0,0), name="tank")
b = makeBlaster(tank)

trigger = makeTrigger(function=tankWorld.victory)
makeCollisionState(trigger, position=(16 - 2,2.5+1,0), tracking_name=b.getBulletName(), size=(4,4,4))


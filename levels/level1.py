makeFloor(size=(14,30))
makeCubeObject(size=(30,1,3), position=(0,0,0), name='wall1')
makeCubeObject(size=(30,1,3), position=(0,14,0), name='wall2')
makeCubeObject(size=(1,14,3), position=(0,1,0), name='wall3')
makeCubeObject(size=(1,14,3), position=(29,1,0), name='wall4')

tank = makeTank(position=(3,3.5+4,.6), orientation=(90,0,0), name="tank")
makeBlaster(tank)
def nothing():
	print  "wined"

trigger = makeTrigger(function=tankWorld.victory)
makeCollisionState(trigger, position=(26,2.5+4,0), tracking_object=tank)


makeFloor()
makeCubeObject(size=(20,1,3), position=(0,0,0), name='wall1')
makeCubeObject(size=(20,1,3), position=(0,6,0), name='wall2')
makeCubeObject(size=(1,5,3), position=(0,1,0), name='wall3')
makeCubeObject(size=(1,5,3), position=(19,1,0), name='wall4')

tank = makeTank(position=(3,3.5,2), orientation=(90,0,0), name="tank")
makeBlaster(tank)
def nothing():
	print  "wined"

trigger = makeTrigger(function=nothing)
makeCollisionState(trigger, position=(16,2.5,0), tracking_object=tank)




tank = makeTank(position=(3,3.5,2), orientation=(90,0,0), name="tank")
makeFloor()
	
makeCubeObject(size=(26,1,3), position=(0,0,0), name="wall1")
makeCubeObject(size=(20,1,3), position=(0,6,0), name="wall1")
makeCubeObject(size=(1,5,3), position=(0,1,0), name="wall1")
makeCubeObject(size=(1,26,3), position=(26,0,0), name="wall1")
makeCubeObject(size=(1,20,3), position=(20,6,0), name="wall1")
makeCubeObject(size=(7,1,3), position=(20,26,0), name="wall1")

makePositionTrigger(target = tank, position=(22.5,23,0))


makeFloor()

tank = makeTank(position=(0,4,2), orientation=(90,0,0), name="tank")
makeBlaster(tank)
levelData = {'test':34}
turret = makeTurret(position=(0,0,0), orientation=(90,0,0), name='turret')
makeBlaster(turret)

makeCubeObject(size=(16,1,5), position=(0,5,0), name='wall1')

addLevelData(levelData)


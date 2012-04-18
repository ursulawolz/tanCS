

tank = tankWorld.getUserTank()
levelData = tankWorld.getLevelData()

def userFun(tank, levelData):
    print levelData
    yield()
    
    
    tank.move(30)
    yield()

x = userFun(tank, levelData)
tank.setGenerator(x)
tank.runTasks()
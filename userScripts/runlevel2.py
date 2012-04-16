

tank = tankWorld.getUserTank()
levelData = tankWorld.getLevelData()

def userFun(tank, levelData):
    tank.move(20)
    yield()
    tank.left()
    yield()
    tank.move(20)
    yield()
    
    

x = userFun(tank, levelData)
tank.setGenerator(x)
tank.runTasks()
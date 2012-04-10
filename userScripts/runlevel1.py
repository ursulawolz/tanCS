

tank = tankWorld.getUserTank()

def userFun(tank):
    tank.move(30)
    yield()

x = userFun(tank)
tank.setGenerator(x)
tank.runTasks()
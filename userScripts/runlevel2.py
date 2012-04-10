

tank = tankWorld.getUserTank()

def userFun(tank):
    def running():
        tank.move(19)
        yield()
        tank.left()
        yield()
        running()
        yield()
    
    running()
    yield()
    
    

x = userFun(tank)
tank.setGenerator(x)
tank.runTasks()
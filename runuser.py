

tank = tankWorld.getUserTank()

def userFun(tank):
    while 1==1:
    	tank.moveTime(2)
        yield()
    	tank.rotateTime(2)
        yield()
    	tank.fire(1)
        yield()

x = userFun(tank)
tank.setGenerator(x)
tank.runTasks()
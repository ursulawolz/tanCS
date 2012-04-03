

tank = tankWorld.getUserTank()

def userFun(tank):
    while 1==1:
    	print tank.getPos()
        yield()
    	tank.moveTime(1)
        yield()
    	tank.fire()
        yield()
    	tank.rotateTime(1)
        yield()

x = userFun(tank)
tank.setGenerator(x)
tank.runTasks()


tank = tankWorld.getUserTank()

def userFun(tank):
    while 1==1:
    	tank.moveTime(1)
        yield()
    	tank.fire()
        yield()
    	tank.rotateTime(1)
        yield()
    	results = tank.pingPoints()
        yield()
    	for item in results:
    	    print item
            yield()
    	print ""
        yield()

x = userFun(tank)
tank.setGenerator(x)
tank.runTasks()
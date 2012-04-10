

tank = tankWorld.getUserTank()

def userFun(tank):
    
    	tank.waitTime(5)
        yield()
    	print tank.aimAt(Point3(25,25,1), False)
        yield()
    	tank.fire()
        yield()

x = userFun(tank)
tank.setGenerator(x)
tank.runTasks()
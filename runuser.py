

tank = tankWorld.getUserTank()

def userFun(tank):
    while 1==1:
    
    	tank.move(10)
        yield()
    	tank.rotateTime(1.3)
        yield()
    	

x = userFun(tank)
tank.setGenerator(x)
tank.runTasks()
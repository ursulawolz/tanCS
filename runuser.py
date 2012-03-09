

tank = Tank(tankWorld,	 tankWorld.render)

def userFun(tank):
    while 1==1:
    	tank.moveTime(2)
        yield()
    	tank.rotateTime(2)
        yield()

x = userFun(tank)
tank.setGenerator(x)
tank.runTasks()
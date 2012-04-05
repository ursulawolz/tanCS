

tank = tankWorld.getUserTank()

def userFun(tank):
    while 1==1:
<<<<<<< HEAD
    	tank.move(10)
=======
    	
    	print tank.getPos()
        yield()
    	tank.fire()
        yield()
    	tank.rotateTime(1)
        yield()
    	tank.moveTime(2)
>>>>>>> 4ece7dc50167e0419925ead66daffeaa377c24a5
        yield()
    	tank.rotateTime(1.3)
        yield()
    	tank.getPos() #look Ma, comments
        yield()

x = userFun(tank)
tank.setGenerator(x)
tank.runTasks()
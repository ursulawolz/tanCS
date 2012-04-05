

tank = tankWorld.getUserTank()

def userFun(tank):
    while 1==1:
    
    	tank.move(10)
        yield()
<<<<<<< HEAD
    	tank.move(2)
        yield()
    	results = tank.pingPoints()
        yield()
    	for item in results:
    	    print item
            yield()
    	print ""
=======
    	tank.rotateTime(1.3)
>>>>>>> 687adcabb7252aaad790d26e87c17d6952374d19
        yield()
    	

x = userFun(tank)
tank.setGenerator(x)
tank.runTasks()
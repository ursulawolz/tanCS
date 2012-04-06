

tank = tankWorld.getUserTank()

def userFun(tank):
    while 1==1:
    
    	tank.move(30)
        yield()
    	#tank.rotateTime(1.3)
    
    	#print tank.getPos()
    
    

x = userFun(tank)
tank.setGenerator(x)
tank.runTasks()
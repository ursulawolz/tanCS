while 1==1:
	
	print tank.getPos()
	tank.fire()
	tank.rotateTime(1)
	tank.move(2)
	results = tank.pingPoints()
	for item in results:
	    print item
	print ""

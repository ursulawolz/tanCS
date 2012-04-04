while 1==1:
	tank.moveTime(1)
	tank.fire()
	tank.rotateTime(1)
	results = tank.pingPoints()
	for item in results:
	    print item
	print ""

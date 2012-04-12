print levelData


#tank.move(30)
for k in range(190):
	tank.aimAt(Vec3(16,2.5,2))
	tank.waitTime(2)
	tank.fire()
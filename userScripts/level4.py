print levelData


#tank.move(30)
for k in range(190):
	tank.aim_at((16,2.5,2))
	tank.wait(2)
	tank.fire()
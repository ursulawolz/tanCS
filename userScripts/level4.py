print level_data

tank.wait(4)
#tank.move(30)
for k in range(190):
    tank.aim_at((16,4.5,1.5))
    tank.wait(2)
    tank.fire()
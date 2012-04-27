

tank = tankWorld.getUserTank()
level_data = tankWorld.getLevelData()

def user_fun(tank, level_data):
    
    tank.move(10)
    yield()
    tank.fire()
    yield()
    tank.rotate(90)
    yield()
    tank.aimAt((0,0,0))
    yield()
    tank.fire()
    yield()
    tank.wait(1)
    yield()
    tank.move(10)
    yield()

x = user_fun(tank, level_data)
tank.set_generator(x)
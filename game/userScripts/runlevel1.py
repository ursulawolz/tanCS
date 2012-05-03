

tank = tankWorld.getUserTank(0)
level_data = tankWorld.getLevelData()

def user_fun(tank, level_data):
    tank.move(40)
    yield()

x = user_fun(tank, level_data)
tank.set_generator(x)
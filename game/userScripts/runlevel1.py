

tank = tankWorld.getUserTank(0)
level_data = tankWorld.getLevelData()

def user_fun(tank, level_data):
    print level_data
    yield()
    
    tank.move(30)
    yield()

x = user_fun(tank, level_data)
tank.set_generator(x)
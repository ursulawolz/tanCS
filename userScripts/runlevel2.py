

tank = tankWorld.getUserTank(0)
level_data = tankWorld.getLevelData()

def user_fun(tank, level_data):
    tank.move(20)
    yield()
    tank.left()
    yield()
    tank.move(20)
    yield()
    
    

x = user_fun(tank, level_data)
tank.set_generator(x)
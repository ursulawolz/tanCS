

tank = tankWorld.getUserTank(0)
level_data = tankWorld.getLevelData()

def user_fun(tank, level_data):
    tank.move(4)
    yield()
    for l in range(30):
    	tank.move(3)
        yield()
    	tank.left()
        yield()
    	tank.fire()
        yield()
    
    
    #bad way to solve this
    '''tank.move(x*5)
    yield()
    print 'pre left'
    yield()
    tank.left()
    yield()
    tank.move(x*4)
    yield()
    print 'post left'
    yield()
    tank.left()
    yield()
    tank.move(x*3+3)
    yield()
    
    tank.left()
    yield()
    tank.move(x*3-3)
    yield()
    
    tank.left()
    yield()
    tank.move(x*2+3)
    yield()
    
    tank.left()
    yield()
    tank.move(x*1)
    yield()
    tank.left()
    yield()
    tank.move(x*2)'''
    yield()

x = user_fun(tank, level_data)
tank.set_generator(x)

tankWorld = TankWorld()
tank = Tank(tankWorld,	 tankWorld.render)

def userFun():
    print tank.scan()
    yield()
    
    tank.dickAround()
    yield()
    
    if (1 == 0):
        tank.killAllTheThings()
        yield()
        while(x):
            tank.yellAtGreg(loudly)
            yield()

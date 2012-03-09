
tankWorld = TankWorld()
tank = Tank(tankWorld, tankWorld.render)

def userFun():
    print tank.scan()
    yield()
    
    tank.dickAround()
    yield()
    
    tank.killAllTheThings()
    yield()
    
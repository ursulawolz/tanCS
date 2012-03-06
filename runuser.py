tankWorld = TankWorld()

tank = Tank(tankWorld.getPhysics(), tankWorld.render)

tank.setTankWorld(tankWorld)
print tank.scan()
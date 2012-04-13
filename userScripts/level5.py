x = levelData['x']
tank.move(x)
print 'pre left'
tank.fire()
tank.left()
print 'post left'
tank.fire()
tank.right()
tank.move(x)
tank.left()
tank.fire()
tank.right()



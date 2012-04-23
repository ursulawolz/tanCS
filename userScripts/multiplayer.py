import random

tank.move(4)
while 1:
    for l in range(2):
        tank.move(random.randint(0,10))
        tank.rotate(random.randint(0,180))
        tank.fire()
    for l in range(2):
        tank.move(-random.randint(0,10))
        tank.rotate(random.randint(0,180))
        tank.fire()



#bad way to solve this
'''tank.move(x*5)
print 'pre left'
tank.left()
tank.move(x*4)
print 'post left'
tank.left()
tank.move(x*3+3)

tank.left()
tank.move(x*3-3)

tank.left()
tank.move(x*2+3)

tank.left()
tank.move(x*1)
tank.left()
tank.move(x*2)'''
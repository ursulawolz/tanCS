data = level_data['data']

for l in data:
	tank.move(l)
	tank.left()


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
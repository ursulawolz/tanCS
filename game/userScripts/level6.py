data = level_data['data']

direction = 90

for l in data:
	direction += 90
	tank.move(l)
	tank.turn_to(direction)


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
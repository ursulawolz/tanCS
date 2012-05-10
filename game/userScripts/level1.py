data = level_data['data']

print data

direction = 90

for l in data:
	direction += 90
	tank.move(l)
	tank.turn_to(direction)

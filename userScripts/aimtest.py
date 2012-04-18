print level_data
x = 7
tank.move(100)

while True:
    p = tank.get_pos()
    d = tank.distance_scan()
    
    friendly = tank.get_projectile_name()
    for b in d:
        if b[1] != friendly and 'blast' in b[1]:            

            #Calculates distance to object
            total = 0
            for i in range(3):
                total += (b[0][i] - p[i])**2
            distance = math.sqrt(total)

            if (b[0][2] > 3 and distance < 50):
                print "GO",
                tank.fire_at(b[0])
                print "GO"
    print "asdf"




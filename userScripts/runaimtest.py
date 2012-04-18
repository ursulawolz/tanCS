

tank = tankWorld.getUserTank()
level_data = tankWorld.getLevelData()

def user_fun(tank, level_data):
    print level_data
    yield()
    x = 7
    yield()
    tank.move(100)
    yield()
    
    while True:
        p = tank.get_pos()
        yield()
        d = tank.distance_scan()
        yield()
        
        friendly = tank.get_projectile_name()
        yield()
        for b in d:
            if b[1] != friendly and 'blast' in b[1]:            
    
                #Calculates distance to object
                total = 0
                yield()
                for i in range(3):
                    total += (b[0][i] - p[i])**2
                    yield()
                distance = math.sqrt(total)
                yield()
    
                if (b[0][2] > 3 and distance < 50):
                    print "GO",
                    yield()
                    tank.fire_at(b[0])
                    yield()
                    print "GO"
                    yield()
        print "asdf"
        yield()
    
    
    

x = user_fun(tank, level_data)
tank.set_generator(x)
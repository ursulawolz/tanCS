print levelData
x = 7
tank.move(17)
tank.rotate(58)
tank.move(10)
while 1:
    #tank.move(x)
    d = tank.distanceScan()
    friendly = tank._weapon.getBulletName()
    for b in d:
        if b[1] != friendly:
            print b[0], b[1]
            tank.aimAt(b[0])
            tank.fire(1)



    print "asdf"


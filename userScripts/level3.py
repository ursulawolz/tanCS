r=8
c=2*3.14*r
x=10
for i in range(x+2):
    if i==0:
        tank.move(c/x-5)
    else:
        tank.move(c/x-1)
    tank.rotate(360/x)

# for i in range(360):
#     tank.move(1)
#     tank.rotate(2)


# r=8

#     x=math.sqrt(abs(r1**2-y**2))

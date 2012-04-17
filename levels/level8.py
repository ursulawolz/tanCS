import math
makeFloor()
r1=12
r2=r1-8
x=r1
y=0
posx=[x]
posy=[y]
i=1

while y<=r1:
    y+=.1
    x=math.sqrt(abs(r1**2-y**2))
    #make so that it adds the next block to the side where the circle exits the block
    posx.append(x)
    posy.append(y)
    makeCubeObject(size=(1,1,3),position=(int(posx[i])+r1,int(posy[i])+r1,0), name='wall1')
    makeCubeObject(size=(1,1,3),position=(-int(posx[i])+r1,int(posy[i])+r1,0), name='wall1')
    makeCubeObject(size=(1,1,3),position=(-int(posx[i])+r1,-int(posy[i])+r1,0), name='wall1')
    #makeCubeObject(size=(1,1,3),position=(int(posx[i])+r1,-int(posy[i])+r1,0), name='wall1')
    # print posx[i]
    # print posy[i]
    i+=1

x=r2
y=0
while y<=r2:
    y+=.1
    x=math.sqrt(abs(r2**2-y**2))
    #make so that it adds the next block to the side where the circle exits the block
    posx.append(x)
    posy.append(y)
    makeCubeObject(size=(1,1,3),position=(int(posx[i])+r1,int(posy[i])+r1,0), name='wall2')
    makeCubeObject(size=(1,1,3),position=(-int(posx[i])+r1,int(posy[i])+r1,0), name='wall2')
    makeCubeObject(size=(1,1,3),position=(-int(posx[i])+r1,-int(posy[i])+r1,0), name='wall2')
    #makeCubeObject(size=(1,1,3),position=(int(posx[i])+r1,-int(posy[i])+r1,0), name='wall2')
    # print posx[i]
    # print posy[i]
    i+=1

makeCubeObject(size=(r1-r2,1,3),position=(posx[0]+r1-(r1-r2),r1,0), name='wall3')
makeCubeObject(size=(1,r1-r2,3),position=(posx[0],posy[0]+r2/2,0), name='wall3')

tank = makeTank(position=(posx[0]+r1-5,r1+3,2), orientation=(180,0,0), name='tank')

#makeCubeObject(size=(5,7,5),position=(1,0,0),name='testobject')
def nothing():
    print  "win"

makeBlaster(tank)
trigger = makeTrigger(function=nothing)
makeCollisionState(trigger, position=(posx[0]-r2/2,posy[0]+r2/2+3,0), tracking_object=tank)

#makePositionTrigger(target = tank, position=(posx[0]+r1-5,r1-3,0))
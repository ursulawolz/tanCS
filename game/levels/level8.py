import math
makeFloor()
x=30
d=6

makeCubeObject(size=(x,1,3),position=(0,0,0),name='wall1')
makeCubeObject(size=(x-d,1,3),position=(0,d,0),name='wall1')
makeCubeObject(size=(1,x,3),position=(0,0,0),name='wall1')
makeCubeObject(size=(1,x,3),position=(x,0,0),name='wall1')
makeCubeObject(size=(1,x-2*d,3),position=(x-d,d,0),name='wall1')
makeCubeObject(size=(x+1,1,3),position=(0,x,0),name='wall1')
makeCubeObject(size=(x-2*d+1,1,3),position=(d,x-d,0),name='wall1')
makeCubeObject(size=(1,x-2*d,3),position=(d,d,0),name='wall1')

tank = makeTank(position=(d/2,2.5,2), orientation=(90,0,0), name='tank')

#makeCubeObject(size=(5,7,5),position=(1,0,0),name='testobject')
def nothing():
    print  "win"

makeBlaster(tank)
trigger = makeTrigger(function=nothing)
makeCollisionState(trigger, position=(d/2,d+1,0), tracking_object=tank)

#makePositionTrigger(target = tank, position=(posx[0]+r1-5,r1-3,0))
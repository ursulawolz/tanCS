makeFloor()
tank = makeTank(position=(40,40,2), orientation=(90,0,0), name="tank")
makeBlaster(tank)
levelData = {'test':34}
turret = makeTurret(position=(0,0,0), orientation=(90,0,0), name='turret')
b= makeBlaster(turret)
b.maxVel = 60
#makeCubeObject(size=(16,1,5), position=(0,15,0), name='wall1')

addLevelData(levelData)



#from direct.gui.OnscreenText import OnscreenText
#textObject = OnscreenText(text = 'TEsting the on screen text. \n this is goign to tell some of the story.',
#	 pos = (-1+.4, 1-.4), scale = 0.08, bg=VBase4(.6,.6,.6,.6), fg=VBase4(0,0,0,95))
from TankWorld import TankWorld
from runFile import runFile
import sys
#import xmlParse
import levels.MakeLevel
def runGame(userfile):
	
	f = open("gui/saved.data")
	#worldNum = int(f.readline().strip().split('orld')[1])
	f.readline()
	level = f.readline().strip().lower()
	t = levels.MakeLevel.makeLevel(level) #level is name of level.
	runFile(userfile,t) #user file is path to user file
	t.preCalc()
	


import sys
sys.path.append("../game")
sys.path.append("..")
sys.path.append("game")
from TankWorld import TankWorld
from runFile import runFile
import sys
#import xmlParse
import levels.MakeLevel

import sys
print sys.argv[1]
userfile = sys.argv[1]

f = open("../game/gui/saved.data")
#worldNum = int(f.readline().strip().split('orld')[1])
f.readline()
level = f.readline().strip().lower()
t = levels.MakeLevel.makeLevel(level) #level is name of level.

runFile(userfile,t) #user file is path to user file
t.preCalc()


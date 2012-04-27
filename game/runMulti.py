from TankWorld import TankWorld
from runFile import runFile
import sys
#import xmlParse
import levels.MakeLevel
level = 'multiplayer'
userfile = 'userScripts/multiplayer.py'
userfile2 = 'userScripts/multiplayer.py'
#t = xmlParse.createLevel(level)
t = levels.MakeLevel.makeLevel(level)
runFile(userfile,t, tankNum =0)
runFile(userfile2,t, tankNum =1)
t.run()

sys.exit()

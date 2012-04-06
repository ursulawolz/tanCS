from TankWorld import TankWorld
from runFile import runFile
import sys
import xmlParse
import levels.MakeLevel
level = 'levels/testLevel.xml'
userfile = 'userScripts/user.py'
if len(sys.argv) == 3:
	level = sys.argv[1]
	userfile = 'userScripts/'+sys.argv[2]

if len(sys.argv)==2:
	level = sys.argv[1]
	userfile =  'userScripts/'+sys.argv[1]+'.py'

#t = xmlParse.createLevel(level)
t = levels.MakeLevel.makeLevel(level)
runFile(userfile,t)
t.run()
print "done?"

sys.exit()

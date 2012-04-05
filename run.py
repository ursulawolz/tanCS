from TankWorld import TankWorld
from runFile import runFile

import xmlParse

t = xmlParse.createLevel('testLevel.xml')

runFile('user.py',t)

t.run()
print "done?"

sys.exit()
from TankWorld import TankWorld
from runFile import runFile

import xmlParse

t = xmlParse.createLevel('levels/testLevel.xml')

runFile('userScripts/user.py',t)

t.run()
print "done?"

sys.exit()
